from django.contrib.auth import login, logout
from django.http import HttpResponse

from authlib.integrations.django_client import OAuth
from tzlocal import get_localzone
from datetime import datetime, timedelta
from json import dumps, loads
import logging

from .models import GoogleToken, HubspotToken, Account
from .requests import GoogleAPI, HubspotAPI, OAuth2API
from .constants import *


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
		
		if request.method == 'POST':			
			# Extract authenticate infomation
			user_id = request.POST.get('user_id')
			password = request.POST.get('password')
			
			# Verify user
			user = Account.authenticate(user_id=user_id, password=password)
				
			if user is None: # if no user found
				return HTTP_400_AUTHENTICATION_FAIL
				
			login(request, user) # Create new session
			
			# Generate profile
			profile = Account.generate_profile(user)
						
			return HttpResponse(content=dumps(profile), content_type='application/json')
		
		return HTTP_405

	@classmethod
	def _logout(cls, request):
		'''Handle backend user logout process'''
		if not request.user.is_authenticated: # Verify authenticate status
			return HTTP_400_LOGIN_REQUIRE
			
		if request.method == 'GET':
			logout(request) # End session
			return HTTP_200		
		
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
		token = None
		 
		if service == 'hubspot':
			token = HubspotToken.fetch_credential(user=request.user)
		else:
			token = GoogleToken.fetch_credential(user=request.user)
			
		if token is None:
			return None
		
		if token.expires_at <= datetime.now(get_localzone()) + timedelta(minutes=5): #if token expired
			response = OAuth2API.fetch_access_token(request=request, refresh_token=token.refresh_token, service=oauth.create_client(service))
			
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
		
class OAuth2:
	'''Oauth2 API request handler'''
	@staticmethod
	def build_redirect_url(request, service):
		'''Method use to generate redirect URL of this server'''
		return 'https://' + request.get_host() + '/accounts/'+ service + '/auth/callback'
	
	@classmethod
	def authorize(cls, request, service):
		'''Handle 3rd service OAuth2.0 authentication'''
		if not request.user.is_authenticated: # Authenication check
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
		'''Handle retrieving 3rd OAuth2.0 authentication credential'''	
		if service not in ['google', 'hubspot']: # Validate request
			return HTTP_404
			
		if request.method == 'GET':
			# Authenication check
			if not request.user.is_authenticated:
				return HTTP_400_LOGIN_REQUIRE		
				
			# Instantiate google service  
			service_ = oauth.create_client(service)
			
			if service == 'google':
				token = service_.authorize_access_token(request) # Get credential
				# Save token into database
				GoogleToken.register_credential(user=request.user, token=token)
				
			else: # for hubspot service
				# Get credential
				token = service_.authorize_access_token(request, grant_type='authorization_code', 
						client_id=service_.client_id, client_secret=service_.client_secret)
				# Save token into database
				HubspotToken.register_credential(user=request.user, token=token)
				
			if 'refresh_token' in list(token.keys()):
				token.pop('refresh_token') # remove refresh_token attribute
				
			return HttpResponse(content=dumps(token), content_type='application/json')
			
		return HTTP_405
		
	@classmethod
	def retrieve_access_token(cls, request, service):
		'''Return google access token from database'''
				# Validate request
		if service not in ['google', 'hubspot']:
			return HTTP_404

		if request.method == 'GET':
			if not request.user.is_authenticated: # Authenication check
				return HTTP_400_LOGIN_REQUIRE
			
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
		
		if request.method == 'POST':
			if not request.user.is_authenticated: # Authenication check
				return HTTP_400_LOGIN_REQUIRE
			#retrieve token from database
			token = User.fetch_access_token(request=request, service='google')
			
			#handle error
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if token == {}:
				return HTTP_408
			
			name = request.POST.get('name')
			if name is None:
				name = f'ENG_INIT_Lead_2020_{datetime.now().strftime("%d")}_{datetime.now().strftime("%m")}.pptx'
				
			#Upload template
			response = GoogleAPI.upload_init_lead_template(access_token=token['access_token'], 
								name=name, parentID=request.POST.get('parentID'))
			
			return HttpResponse(content=response.text, content_type='application/json')
				
		return HTTP_405
				
class HubspotService:
	'''Hubspot service API request handler'''
	@classmethod
	def get_makeoffer_deals(cls, request):
		'''Handle Hubspot API call to fetch all "Make Offer" deals'''
				
		if request.method == 'GET':			
			if not request.user.is_authenticated: # Authentication check
				return HTTP_400_LOGIN_REQUIRE
			
			token = User.fetch_access_token(request=request, service='hubspot')
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			if token == {}:
				return HTTP_408
				
			deals = HubspotAPI.fetch_make_offer_deals(access_token=token['access_token'])
				
			return HttpResponse(content=dumps(deals), content_type='application/json')

		return HTTP_405
	
	@classmethod
	def get_company_info(cls, request, dealID):
		'''Retrieve company ID from Hubspot'''
		if request.method == 'GET':			
			if not request.user.is_authenticated: # Authentication check
				return HTTP_400_LOGIN_REQUIRE
				
			token = User.fetch_access_token(request=request, service='hubspot')
			
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
				
			if token == {}:
				return HTTP_408
				
			companyInfo = HubspotAPI.fetch_company_info(access_token=token['access_token'], dealID=dealID)
				
			return HttpResponse(content=dumps(companyInfo), content_type='application/json')	
			
		return HTTP_405

def test(request):
	# Authentication check
	if not request.user.is_authenticated:
		return HTTP_400_LOGIN_REQUIRE
	return HttpResponse('Hello World')
