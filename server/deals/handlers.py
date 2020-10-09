from django.contrib.auth import login, logout
from django.contrib.auth import models
from django.shortcuts import redirect
from django.http import HttpResponse

from ldap3 import Server, Connection, ALL_ATTRIBUTES
from authlib.integrations.django_client import OAuth
from passlib.hash import ldap_salted_sha1 as lss
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from tzlocal import get_localzone
from json import dumps, loads
import logging
import time

from .models.database import GoogleToken, HubspotToken, Account, Cache
from .models.requests import GoogleAPI, HubspotAPI, OAuth2API
from .models.thread import requestThread
from .models.constants import *

logging.basicConfig(filename='deals_server.log', level=logging.DEBUG)

# Initiate OAuth2 session
oauth = OAuth()

# Register service
oauth.register('google')
oauth.register('hubspot')

class User:
	'''Contain a set of user API request handler'''
	
	@classmethod
	def _login(cls, request):
		'''Handle backend user login process'''
		
		if request.method == 'GET':			
			# Extract authenticate infomation
			request_data = parse_qs(urlparse(request.get_full_path()).query)
			
			if 'user_id' not in list(request_data.keys()) or 'password' not in list(request_data.keys()):
				return HTTP_400_INVALID_QUERY
				
			user_id = request_data['user_id'][0]
			password = request_data['password'][0]
			
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
			
			profile = Account.generate_profile(user=user)
			
			login(request, user) # Create new session
										
			return HttpResponse(content=dumps(profile), content_type='application/json')

		return HTTP_405
		
	@classmethod
	def _logout(cls, request):
		'''Handle backend user logout process'''	
			
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
					
		if request.method == 'GET':
			logout(request) # end session
			return HttpResponse(content=dumps({'uid':request.user.username, 'status':'logout success'}), content_type='application/json')
		
		return HTTP_405

	@classmethod
	def profile(cls, request):
		'''Provide user information'''		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
					
		if request.method == 'GET':
			# Generate profile
			profile = Account.generate_profile(request.user)
						
			return HttpResponse(content=dumps(profile), content_type='application/json')
		
		return HTTP_405
		
	@classmethod
	def fetch_access_token(cls, request, service):
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
			token = HubspotToken.fetch_credential(user=request.user)
		else:
			token = GoogleToken.fetch_credential(user=request.user)
			
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
				HubspotToken.register_credential(user=request.user, token=token)
			else:
				GoogleToken.register_credential(user=request.user, token=token)
		else:
			token = token.to_json() # transfer to dictionary
			token.pop('refresh_token') # remove refresh_token attribute
		
		return token
	
	@classmethod
	def cache_deal_setting(cls, request):
		'''Cache deal's drive folder setting and working status'''
		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':			
									
			request_data = parse_qs(urlparse(request.get_full_path()).query)
			
			if 'status' not in list(request_data.keys()) or 'folder_id' not in list(request_data.keys())\
													or 'deal_id' not in list(request_data.keys()):
				return HTTP_400_CACHE_REQUEST_FAIL
				
			# extract data
			deal_status = request_data['status'][0]
			folder_id = request_data['folder_id'][0]
			deal_id = request_data['deal_id'][0] 
				
			cache = Cache.get_deal_cache(user=request.user, deal_id=deal_id)
				
			if cache is None:
				Cache.objects.create(user=request.user, deal_id=deal_id, status=deal_status, folder_id=folder_id)
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
		return 'https://' + request.get_host() + '/accounts/'+ service + '/auth/callback'
	
	@classmethod
	def authorize(cls, request, service):
		'''Handle 3rd service OAuth2.0 authentication'''
				
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
		
		# Validate request
		if service not in ['google', 'hubspot']:
			return HTTP_404
			
		if request.method == 'GET':
			# Instantiate google service  
			service_ = oauth.create_client(service)
			# create redirect uri
			redirect_uri = cls.build_redirect_url(request=request, service=service)
			# Lead user to Authentication page
			return service_.authorize_redirect(request, redirect_uri)
						
		return HTTP_405
		
	@classmethod
	def callback(cls, request, service):
		'''Handle retrieving 3rd OAuth 2.0 authentication credential'''	
		
		if service not in ['google', 'hubspot']: # Validate request
			return HTTP_404
			
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':						
			# Instantiate google service  
			service_ = oauth.create_client(service)
			
			if service == 'google':
				token = service_.authorize_access_token(request) # Get credential
				# Save token into database
				status = GoogleToken.register_credential(user=request.user, token=token)
				
			else: # for hubspot service
				# Get credential
				token = service_.authorize_access_token(request, grant_type='authorization_code', 
						client_id=service_.client_id, client_secret=service_.client_secret)
						
				# Save token into database
				status = HubspotToken.register_credential(user=request.user, token=token)
				
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

		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':			
					
			token = User.fetch_access_token(request=request, service=service)
			
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
				
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
				
		if request.method == 'GET':
			#retrieve token from database
			google_token = User.fetch_access_token(request=request, service='google')
			hubspot_token = User.fetch_access_token(request=request, service='hubspot')

			#handle error
			if google_token is None or hubspot_token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if google_token == {} or hubspot_token == {}:
				return HTTP_408
				
			request_data = parse_qs(urlparse(request.get_full_path()).query)
			
			if 'deal_id' not in list(request_data.keys()) or 'parentID' not in list(request_data.keys()):
				return HTTP_400_INVALID_QUERY

			deal_id = request_data['deal_id'][0]
			parent_id = request_data['parentID'][0] if request_data['parentID'][0] != 'null' else None
						
			if 'name' not in list(request_data.keys()):
				name = f'ENG_INIT_Lead_{datetime.now().strftime("%Y")}_{datetime.now().strftime("%d")}_{datetime.now().strftime("%m")}.pptx'	
			else:
				name = request_data['name'][0]
			
			notesThread = requestThread(target=HubspotAPI.fetch_notes, kwargs={'access_token': hubspot_token['access_token'], 'deal_id': deal_id})
			companyThread = requestThread(target=HubspotAPI.fetch_company_info, kwargs={'access_token': hubspot_token['access_token'], 'dealID': deal_id})
			dealThread = requestThread(target=HubspotAPI.fetch_deal_info, kwargs={'access_token': hubspot_token['access_token'], 'deal_id': deal_id})
			initLeadThread = requestThread(target=GoogleAPI.upload_init_lead_template, kwargs={'access_token': google_token['access_token'], 'name': name, 'parentID': parent_id})
			
			threads = [notesThread, companyThread, dealThread, initLeadThread]
			
			notesThread.start()
			companyThread.start()
			dealThread.start()
			initLeadThread.start()
			
			data = []
			
			for thread in threads:
				response = thread.join()
				
				if isinstance(response, (dict, type(None))):
					data.append(response)
					continue
												
				if response.status_code != 200:
					return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)

				data.append(response.json())
			
			retry_times = 0
			
			while True:
				response = GoogleAPI.fill_out_the_template(access_token=google_token['access_token'], deal=data[2], company=data[1], notes=data[0], slide_id=data[3]['id'])
				
				if response.status_code == 200:
					break
				
				if retry_time > RETRY_TIMES:
					break
				
				retry_times += 1
				time.sleep(1)
					
			return HttpResponse(content=response.text, content_type='application/json', status=response.status_code)
				
		return HTTP_405

	@classmethod
	def retrieve_token_info(cls, request):
		'''Retrieve access_token info from google server'''
		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':						
						
			token = User.fetch_access_token(request=request, service='google')
			
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
		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':						
						
			token = GoogleToken.fetch_credential(user=request.user)
			
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
				
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':						
					
			token = User.fetch_access_token(request=request, service='hubspot')
			
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
			
			Cache.clean_cache(user=request.user, deal_id_list=deal_ids)
			
			deals['caches'] = Cache.caches_to_json(user=request.user)
			
			return HttpResponse(content=dumps(deals), content_type='application/json')

		return HTTP_405
		
	@classmethod
	def retrieve_token_info(cls, request):
		'''Retrieve access_token info from hubspot server'''
		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':						
						
			token = User.fetch_access_token(request=request, service='hubspot')
			
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
		
		if not request.user.is_authenticated:
			return HTTP_400_LOGIN_REQUIRE
				
		if request.method == 'GET':						
						
			token = HubspotToken.fetch_credential(user=request.user)
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			response = HubspotAPI.revoke_credential(refresh_token=token.refresh_token)
			
			if response.status_code == 204 or response.status_code == 200:
				token.delete()
				
			return HttpResponse(content=dumps(response.json()), content_type='application/json', status=response.status_code)
			
		return HTTP_405

def test(request):		
	
	return HttpResponse(content=res)
	return HttpResponse('Hello World')