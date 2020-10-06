from django.contrib.auth import login, logout
from django.contrib.auth import models
from django.shortcuts import redirect
from django.http import HttpResponse

from ldap3 import Server, Connection, ALL_ATTRIBUTES
from authlib.integrations.django_client import OAuth
from passlib.hash import ldap_salted_sha1 as lss
from datetime import datetime, timedelta
from tzlocal import get_localzone
from json import dumps, loads
import logging

from .models.database import GoogleToken, HubspotToken, Account, Cache
from .models.requests import GoogleAPI, HubspotAPI, OAuth2API
from .models.thread import requestThread
from .models.auth0 import *
from .models.constants import *
from .models.auth0 import *

logging.basicConfig(filename='deals_server.log', level=logging.DEBUG)

# Initiate OAuth2 session
oauth = OAuth()

# Register service
oauth.register('google')
oauth.register('hubspot')

class User:
	'''Contain a set of user API request handler'''
	
	@classmethod
	def authorize(cls, request):
		'''Handle backend user login process'''
		
		if request.method == 'POST':			
			# Extract authenticate infomation
			user_id = request.POST.get('user_id')
			password = request.POST.get('password')
			
	    	# Connect to LDAP server
			server = Server(host=LDAP_HOST)
			conn = Connection(server, user='cn=ldap-ro,dc=DIROX,dc=ldap', password=LDAP_PWD)
			conn.start_tls()
			conn.bind()
	        
			# Searching for user data
			if '@' in user_id:
				conn.search('ou=users,dc=DIROX,dc=ldap', f'(mail={user_id})', attributes=[ALL_ATTRIBUTES])
			else:
				conn.search('ou=users,dc=DIROX,dc=ldap', f'(uid={user_id})', attributes=[ALL_ATTRIBUTES])
			
			
			if conn.entries == []: #if  user not found
				user = Account.find_user(user_id)
				
				#Clean cache data of a invalid user user
				if user is not None:
					user.delete()
					
				return HTTP_400_USER_NOT_FOUND
				
			# if conn.entries[0].title not in ALLOWED_ACCESS_TITLE
			# 	return HTTP_403_USER_FORBIDDEN

			user = Account.find_user(user_id)
			
			# Auto create new user
			if user is None:
				models.User.objects.create_user(username=conn.entries[0].uid.value, email=conn.entries[0].mail.value, password='')
				user = Account.find_user(user_id)
				
			# Verify password
			if not lss.verify(password, conn.entries[0].userPassword.value):
				return HTTP_400_WRONG_PASSWORD
				
			conn.unbind() # disconnect LDAP server
			# login(request, user) # Create new session
							
			token = {
				'access_token': Auth0.jwt_token_generator(request, user).decode(encoding='UTF-8', errors='strict'),
				'token_type': 'Bearer',
				'expired_in': 3600,
				'expiration_time': (datetime.utcnow() + timedelta(hours=1)).isoformat()
			}			
			
			return HttpResponse(content=dumps(token), content_type='application/json')

		return HTTP_405

	@classmethod
	def profile(cls, request):
		'''Handle backend user logout process'''
		user = Auth0.verify_identity(request)
		
		if user is None:
			return HTTP_400_LOGIN_REQUIRE
					
		if request.method == 'GET':
			# Generate profile
			profile = Account.generate_profile(user)
						
			return HttpResponse(content=dumps(profile), content_type='application/json')
		
		return HTTP_405
		
	@classmethod
	def fetch_access_token(cls, user, service):
		'''
			Fetch access token from credential that store in database
			- request {HTTPRequest} - request that client make
			- service {str} - either 'google' or 'hubspot'
			Return:
			- empty dict if temporary error occur
			- None if permanent error occur
			- token dictonary if success
		'''
		
		# get creadential from database
		if service == 'hubspot':
			token = HubspotToken.fetch_credential(user=user)
		else:
			token = GoogleToken.fetch_credential(user=user)
			
		if token is None:
			return None
		
		if token.expires_at <= datetime.now(get_localzone()) + timedelta(minutes=5): #if token expired
			response = OAuth2API.fetch_access_token(request=request, refresh_token=token.refresh_token, 
																	service=oauth.create_client(service))
			if response.status_code == 400: # if refresh token didn't work
				token.delete() # delete invalid credential
				return None
				
			if response.status_code != 200: # if recieve temporary error
				return {}
				
			token = response.json()
			
			# update credential
			if service == 'hubspot':
				HubspotToken.register_credential(user=user, token=token)
			else:
				GoogleToken.register_credential(user=user, token=token)
		else:
			token = token.to_json() # transfer to dictionary
			token.pop('refresh_token') # remove refresh_token attribute
		
		return token
	
	@classmethod
	def cache_deal_setting(cls, request):
		'''Cache deal's drive folder setting and working status'''
		
		if request.method == 'POST':
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
				
			# extract data
			deal_status = request.POST.get('status')
			folder_id = request.POST.get('folder_id')
			deal_id = request.POST.get('deal_id')
			
			if deal_status is None or folder_id is None or deal_id is None:
				return HTTP_400_CACHE_REQUEST_FAIL
				
			cache = Cache.get_deal_cache(user=user, deal_id=deal_id)
				
			if cache is None:
				Cache.objects.create(user=user, deal_id=deal_id, status=deal_status, folder_id=folder_id)
				return HTTP_200
				
			cache.folder_id = folder_id
			cache.status = deal_status
			cache.save()
				
			return HTTP_200
				
		return HTTP_405
			
class OAuth2:
	'''Oauth2 API request handler'''
	@staticmethod
	def build_redirect_url(request, service):
		'''Method use to generate redirect URL of this server'''
		return 'http://' + request.get_host() + '/accounts/'+ service + '/auth/callback'
	
	@classmethod
	def authorize(cls, request, service):
		'''Handle 3rd service OAuth2.0 authentication'''
		user = Auth0.verify_identity(request)
		
		if user is None:
			return HTTP_400_LOGIN_REQUIRE
		
		# Validate request
		if service not in ['google', 'hubspot']:
			return HTTP_404
			
		if request.method == 'GET':
			# Instantiate google service  
			service_ = oauth.create_client(service)
			# create redirect uri
			redirect_uri = cls.build_redirect_url(request=request, service=service)
			# set cookie for the request
			login(request, user)
			# Lead user to Authentication page
			return service_.authorize_redirect(request, redirect_uri)
			
		return HTTP_405
		
	@classmethod
	def callback(cls, request, service):
		'''Handle retrieving 3rd OAuth2.0 authentication credential'''	
		if service not in ['google', 'hubspot']: # Validate request
			return HTTP_404
			
		if request.method == 'GET':
			if request.user.is_authenticated:
				return HTTP_400_LOGIN_REQUIRE
			
			# clean the session
			user = request.user
			logout(user)
						
			# Instantiate google service  
			service_ = oauth.create_client(service)
			
			if service == 'google':
				token = service_.authorize_access_token(request) # Get credential
				# Save token into database
				status = GoogleToken.register_credential(user=user, token=token)
				
			else: # for hubspot service
				# Get credential
				token = service_.authorize_access_token(request, grant_type='authorization_code', 
						client_id=service_.client_id, client_secret=service_.client_secret)
						
				# Save token into database
				status = HubspotToken.register_credential(user=user, token=token)
				
			if status == 'fail':
				return HTTP_400_INVALID_SERVICE
				
			if 'refresh_token' in list(token.keys()):
				token.pop('refresh_token') # remove refresh_token attribute
				
			return redirect('https://deal.dirox.dev')
			
		return HTTP_405
		
	@classmethod
	def retrieve_access_token(cls, request, service):
		'''Return google access token from database'''
				# Validate request
		if service not in ['google', 'hubspot']:
			return HTTP_404

		if request.method == 'GET':
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
					
			token = User.fetch_access_token(user=user, service=service)
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if token == {}:
				return HTTP_408
				
			if 'refresh_token' in list(token.keys()):
				token.pop('refresh_token') # remove refresh_token attribute

			return HttpResponse(content=dumps(token), content_type='application/json')
					
		return HTTP_405

class GoogleService:
	'''Google service API request handler'''		
	@classmethod
	def create_init_lead(cls, request):
		'''Create a new InitLead document on Drive'''
		
		user = Auth0.verify_identity(request)
		
		if user is None:
			return HTTP_400_LOGIN_REQUIRE
				
		if request.method == 'POST':
			#retrieve token from database
			google_token = User.fetch_access_token(user=user, service='google')
			hubspot_token = User.fetch_access_token(user=user, service='hubspot')
			
			#handle error
			if google_token is None or hubspot_token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if google_token == {} or hubspot_token == {}:
				return HTTP_408
			
			name = request.POST.get('name')
			deal_id = request.POST.get('deal_id')
			
			if name is None:
				name = f'ENG_INIT_Lead_{datetime.now().strftime("%Y")}_{datetime.now().strftime("%d")}_{datetime.now().strftime("%m")}.pptx'	
						
			notesThread = requestThread(target=HubspotAPI.fetch_notes, kwargs={'access_token': hubspot_token['access_token'], 'deal_id': deal_id})
			companyThread = requestThread(target=HubspotAPI.fetch_company_info, kwargs={'access_token': hubspot_token['access_token'], 'dealID': deal_id})
			dealThread = requestThread(target=HubspotAPI.fetch_deal_info, kwargs={'access_token': hubspot_token['access_token'], 'deal_id': deal_id})
			initLeadThread = requestThread(target=GoogleAPI.upload_init_lead_template, kwargs={'access_token': google_token['access_token'], 'name': name, 'parentID': request.POST.get('parentID')})
			
			threads = [notesThread, companyThread, dealThread, initLeadThread]
			
			notesThread.start()
			companyThread.start()
			dealThread.start()
			initLeadThread.start()
			
			data = []
			
			for thread in threads:
				response = thread.join()
													
				if isinstance(response, dict):
					data.append(response)
					continue
					
				if response.status_code != 200:
					return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)

				data.append(response.json())
				
			response = GoogleAPI.fill_out_the_template(access_token=google_token['access_token'], deal=data[2], company=data[1], notes=data[0], slide_id=data[3]['id'])
								
			return HttpResponse(content=response.text, content_type='application/json', status=response.status_code)
				
		return HTTP_405

	@classmethod
	def retrieve_token_info(cls, request):
		'''Retrieve access_token info from google server'''
		
		if request.method == 'GET':			
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
						
			token = User.fetch_access_token(user=user, service='google')
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			if token == {}:
				return HTTP_408

			response = GoogleAPI.retrieve_token_info(access_token=token['access_token'])
			
			return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
						
		return HTTP_405
		
	@classmethod
	def revoke_credential(cls, request):
		'''Retrieve access_token info from google server'''
		
		if request.method == 'GET':			
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
						
			token = GoogleToken.fetch_credential(user=user)
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			response = GoogleAPI.revoke_credential(refresh_token=token.refresh_token)
			
			if response.status_code == 200:
				token.delete()
				
			return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
			
		return HTTP_405		
		
class HubspotService:
	'''Hubspot service API request handler'''
	@classmethod
	def get_makeoffer_deals(cls, request):
		'''Handle Hubspot API call to fetch all "Make Offer" deals'''
				
		if request.method == 'GET':			
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
					
			token = User.fetch_access_token(user=user, service='hubspot')
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			if token == {}:
				return HTTP_408
											
			response = HubspotAPI.fetch_make_offer_deals(access_token=token['access_token'], 
										properties=['dealname', 'start_date','closedate'])
			
			if response.status_code != 200:
				return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
			
			deals = response.json()
			deal_ids = []
			
			for deal in deals['results']:
				deal_ids.append(deal['id'])
			
			Cache.clean_cache(user=user, deal_id_list=deal_ids)
			
			deals['caches'] = Cache.caches_to_json(user=user)
			
			return HttpResponse(content=dumps(deals), content_type='application/json')

		return HTTP_405
		
	@classmethod
	def retrieve_token_info(cls, request):
		'''Retrieve access_token info from hubspot server'''
		
		if request.method == 'GET':			
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
						
			token = User.fetch_access_token(user=user, service='hubspot')
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			if token == {}:
				return HTTP_408

			response = HubspotAPI.retrieve_token_info(access_token=token['access_token'])
			
			return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
			
		return HTTP_405

	@classmethod
	def revoke_credential(cls, request):
		'''Retrieve access_token info from hubspot server'''
		
		if request.method == 'GET':			
			user = Auth0.verify_identity(request)
			
			if user is None:
				return HTTP_400_LOGIN_REQUIRE
						
			token = HubspotToken.fetch_credential(user=user)
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			response = HubspotAPI.revoke_credential(refresh_token=token.refresh_token)
			
			if response.status_code == 204 or response.status_code == 200:
				token.delete()
				
			return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
			
		return HTTP_405

def test(request):		
	token = Auth0.jwt_token_generator(request, uid='test')
	
	return HttpResponse(content=token)
	return HttpResponse('Hello World')