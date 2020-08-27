from django.shortcuts import render, redirect
from django.http import HttpResponse
from authlib.integrations.django_client import OAuth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from json import dumps
import requests
import logging
from .auth import authenticate

# logging.basicConfig(filename='server/debug/api.log', level=logging.DEBUG)

# Initiate Oauth2 session
oauth = OAuth() 

# Register service
oauth.register('google')
oauth.register('hubspot')

# User login
def _login(request):
		
	# Method verify
	if request.method == 'POST':
		if request.user.is_authenticated:
			return HttpResponse(content=dumps({'is_authenticated':True}), content_type='application/json')
			
		# Extract authenticate infomation
		user_id = request.POST.get('user_id')
		password = request.POST.get('password')
		
		user = authenticate(user_id=user_id, password=password)
		
		if user is not None:
			login(request, user)
			return HttpResponse(content=dumps({'is_authenticated':True}), content_type='application/json')
		
		return HttpResponse(content=dumps({'is_authenticated':False}), content_type='application/json')
	
	return HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')

# User logout	
def _logout(request):
		
	# Method verify
	if request.method == 'GET':
		# Verify authenticate statuss
		if not request.user.is_authenticated:
			return HttpResponse(dumps({'is_authenticated':False}),  content_type='application/json')
		
		# Update login status
		logout(request)
		
		return HttpResponse(dumps({'is_authenticated':False}),  content_type='application/json')
		
	
	return HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')

	
# Oauth2 session
def authorize(request, service):
	# Validate request
	if service not in ['google', 'hubspot']:
		return HttpResponse(content="<h1>Page Not Found<h1/>" , status=404, reason="Page Not Found")
		
	# Method verify
	if request.method == 'GET':
		# Instantiate google service  
		service_ = oauth.create_client(service)
		# create redirect uri
		redirect_uri = request.build_absolute_uri('auth/callback')
		# Lead user to Authentication page
		return service_.authorize_redirect(request, redirect_uri)
		
	return HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')

def callback(request, service):
	# Validate request
	if service not in ['google', 'hubspot']:
		return HttpResponse(content="<h1>Page Not Found<h1/>" , status=404, reason="Page Not Found")
		
	# Method verify
	if request.method == 'GET':
		# Instantiate google service  
		service_ = oauth.create_client(service)
		# Get credential
		token = service_.authorize_access_token(request)
		
		return HttpResponse(content=dumps(token), content_type='application/json')
		
	return HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')

# Hubspot fetch data session
def hubspot_get_makeoffer_deals(request):
	# Method verify
	if request.method == 'GET':
		HUBSPOT_TOKEN = ''
		
		API_KEY = '325cadcb-2526-4d69-befc-e0faa744726a'
		
		url = 'https://api.hubapi.com/crm/v3/objects/deals/search'+ '?hapikey=' + API_KEY
		
		properties = [
			'dealname',
			'description',
			'deal_summary',
			'lead_overview_1',
			'lead_overview_2',
			'start_date',
			'closedate'
		]
		
		payload = {
			'filterGroups': [{
				'filters': [{
					'propertyName': 'dealstage',
					'operator': 'EQ',
					'value': '2186805' #Make Offer ID
				}]
			}],
			'properties': properties,
			'limit': 20
		}
				
		headers = {
		  'Content-Type': 'application/json',
		#   'Authorization': 'Bearer ' + HUBSPOT_TOKEN
		}
		
		# fetch data
		response = requests.request('POST', url=url, headers=headers, data=dumps(payload))

		return HttpResponse(response.content, content_type='application/json')
		
	return HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')
