from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse

from authlib.integrations.django_client import OAuth
from tzlocal import get_localzone
from datetime import datetime
from json import dumps, loads
import logging

from .models import GoogleToken, HubspotToken, Account
from .constants import HTTP_200, HTTP_400_AUTHENTICATION_FAIL, HTTP_404, HTTP_405, HTTP_408, HTTP_400_NO_SERVICE_AVAILABLE
from .requests import GoogleAPI, HubspotAPI

logging.basicConfig(filename='API_server.log', level=logging.DEBUG)

# Initiate OAuth2 session
oauth = OAuth()

# Register service
oauth.register('google')
oauth.register('hubspot')

class User:
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
		
class OAuth2:
	@classmethod
	def build_redirect_url(cls, request, service):
		'''Method use to generate redirect URL of this server'''
		return 'http://' + request.get_host() + '/accounts/'+ service + '/auth/callback'
	
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
			redirect_uri = cls.build_redirect_url(request, service)
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
				
			return HttpResponse(content=dumps(token), content_type='application/json')
			
		return HTTP_405

class GoogleService:
	@classmethod
	def retrieve_access_token(cls, request):
		'''Return google access token from database'''
		if request.method == 'GET':
			if not request.user.is_authenticated: # Authenication check
				return HTTP_400_LOGIN_REQUIRE
			
			token = GoogleToken.fetch_credential(user=request.user) # get creadential from database
					
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if token.expires_at <= datetime.now(get_localzone()): #if token expired
				response = GoogleAPI.fetch_access_token(refresh_token=token.refresh_token, service=oauth.create_client('google'))
				if response.status_code == 400:
					token.delete() # delete invalid credential
				if response.status_code != 200:
					return HttpResponse(response.content, status=response.status_code)
				token = loads(response.content.decode('UTF-8'))
				GoogleToken.register_credential(token=token, user=request.user)
			else:
				token = token.to_json() # GoogleToken to dictionary
				token.pop('refresh_token') # remove refresh_token attribute
				
			return HttpResponse(content=dumps(token), content_type='application/json')
					
		return HTTP_405
						
class HubspotService:
	@classmethod
	def get_makeoffer_deals(cls, request):
		'''Handle Hubspot API call to fetch all "Make Offer" deals'''
				
		if request.method == 'GET':			
			if not request.user.is_authenticated: # Authentication check
				return HTTP_400_LOGIN_REQUIRE
			
			# get creadential from database
			token = HubspotToken.fetch_credential(user=request.user)
					
			if token is None:
				return HTTP_400_NO_SERVICE_AVAILABLE
			
			if token.expires_at <= datetime.now(get_localzone()): #if token expired
				response = HubspotAPI.fetch_access_token(_request=request, refresh_token=token.refresh_token, service=oauth.create_client('hubspot'))
				if response.status_code == 400:
					token.delete() # delete invalid credential
				if response.status_code != 200:
					return HttpResponse(response.content, status=response.status_code)
				token = loads(response.content.decode('UTF-8'))
				HubspotToken.register_credential(user=request.user, token=token)
			else:
				token = token.to_json()
											
			deals = HubspotAPI.fetch_make_offer_deals(access_token=token['access_token'])
				
			return HttpResponse(content=dumps(deals), content_type='application/json')

		return HTTP_405
		
def test(request):
	return HttpResponse(content='<h1>Hello world!!<h1/>')