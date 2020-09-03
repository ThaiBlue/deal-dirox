from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse

from authlib.integrations.django_client import OAuth
from json import dumps
from datetime import datetime
import logging

from .models import GoogleToken, HubspotToken, Account
from .constants import HTTP_200, HTTP_401, HTTP_404, HTTP_405
from .requests import GoogleAPI, HubSpotAPI

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
			if request.user.is_authenticated: 
				return HTTP_200
			
			# Extract authenticate infomation
			user_id = request.POST.get('user_id')
			password = request.POST.get('password')
			
			# Verify user
			user = Account.authenticate(user_id=user_id, password=password)
				
			if user is not None:
				login(request, user) # Create new session
				return HTTP_200
			
			return HTTP_401
		
		return HTTP_405

	@classmethod
	def _logout(cls, request):
		'''Handle backend user logout process'''
		if not request.user.is_authenticated: # Verify authenticate status
			return HTTP_401
			
		if request.method == 'GET':
			logout(request) # End session
			return HTTP_200		
		
		return HTTP_405
		
	@classmethod
	def profile(cls, request):
		'''Provide user's account infomation'''
		pass
	
		return HTTP_405
		
class OAuth2:
	@classmethod
	def authorize(cls, request, service):
		'''Handle 3rd service OAuth2.0 authentication'''
		if not request.user.is_authenticated: # Authenication check
			return HTTP_401		

		# Validate request
		if service not in ['google', 'hubspot']:
			return HTTP_404
			
		if request.method == 'GET':
			# Instantiate google service  
			service_ = oauth.create_client(service)
			# create redirect uri
			redirect_uri = request.build_absolute_uri('auth/callback')
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
				return HTTP_401		
				
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
				return HTTP_401
			
			token = GoogleToken.fetch_credential(user=request.user) # get creadential from database
					
			if token is not None:
				if token.expiration_at <= datetime.utcoffset(): #if token expired
					token = GoogleAPI.fetch_access_token(refresh_token=token.refresh_token, service=oauth.create_client('google'))
					GoogleToken.register_credential(token=token, user=request.user)
				else:
					token = token.to_json()
					
				return HttpResponse(content=dumps(token.pop('refresh_token')), content_type='application/json')
		
			return HTTP_404
			
		return HTTP_405
						
class HubspotService:
	@classmethod
	def get_makeoffer_deals(cls, request):
		'''Handle Hubspot API call to fetch all "Make Offer" deals'''
				
		if request.method == 'GET':			
			if not request.user.is_authenticated: # Authentication check
				return HTTP_401
			
			# get creadential from database
			token = HubspotToken.fetch_credential(user=request.user)
					
			if token is not None:
				if token.expiration_at <= datetime.utcoffset(): #if token expired
					response = HubspotAPI.fetch_access_token(request=request, refresh_token=token.refresh_token, service=oauth.create_client('hubspot'))
					if status_code != 200:
						return response
					token = HubspotToken.fetch_credential(user=request.user)
					if token.expiration_at <= datetime.utcoffset():
						return HTTP_408
											
				deals = HubspotAPI.fetch_make_offer_deals(access_token=token.to_json()['access_token'])
				
				return HttpResponse(content=dumps(deals), content_type='application/json')
				
			return HTTP_404
						
		return HTTP_405
		
def test(request):
	return HttpResponse(content='<h1>Hello world!!<h1/>')
