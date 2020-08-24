from django.shortcuts import render, redirect
from django.http import HttpResponse
from authlib.integrations.django_client import OAuth
from json import dumps
import requests
import logging

logging.basicConfig(filename='system.log', level=logging.DEBUG)

# Initiate Oauth2 session
oauth = OAuth() 
# Register google service
oauth.register('google')
oauth.register('hubspot')

# Oauth2 session
def authorize(request, service):
	# Validate request
	if service not in ['google', 'hubspot']:
		return HttpResponse(content="<h1>Not Found!!<h1/>" ,status=404, reason="Not Found")
		
	# Instantiate google service  
	service = oauth.create_client(service)
	# create redirect uri
	redirect_uri = request.build_absolute_uri('auth/callback')
	# Lead user to Authentication page
	return service.authorize_redirect(request, redirect_uri)

def callback(request, service):
	# Validate request
	if service not in ['google', 'hubspot']:
		return HttpResponse(status=404, reason="Not Found")

	# Instantiate google service  
	service = oauth.create_client(service)
	# Get credential
	token = service.authorize_access_token(request)
	
	return HttpResponse(str(token))

# Hubspot fetch data session
def hubspot_get_makeoffer_deals(request):
	HUBSPOT_TOKEN = 'CJHM8ITCLhICAQEY1rSfAyC74cEFKOXsDTIZABsQ8wj_FSxpZPmKBaOzpnsdzjTdkC5p-joaAAoCQQAADIACAAgAAAABAAAAAAAAABjAABNCGQAbEPMIWClP8FmEt8805UvFmKLXX4NkwYM'
	
	url = 'https://api.hubapi.com/crm/v3/objects/deals/search'
	
	properties = [
		'dealname',
		'description',
		'deal_summary',
		'lead_overview_1',
		'lead_overview_2'
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
	  'Authorization': 'Bearer ' + HUBSPOT_TOKEN
	}

	response = requests.request('POST', url=url, headers=headers, data=dumps(payload))

	return HttpResponse(response.content, content_type='application/json')
	