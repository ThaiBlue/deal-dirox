from requests import request
from json import loads

from .constants import MAKE_OFFER

class GoogleAPI:
	@classmethod
	def fetch_access_token(cls, refresh_token, service):
		'''
			Handle create or update token in database
			- token {str} -- a Credential instance
			- service {DjangoRemoteApp} -- a DjangoRemoteApp instance generate from Authlib
		'''
		url = 'https://oauth2.googleapis.com/token'
		
		payload = {
				'client_id': service.client_id,
				'client_secret': service.client_secret,
				'refresh_token': refresh_token,
				'grant_type': 'refresh_token'
		}
				
		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded',
		}
		
		# fetch data
		return loads(request('POST', url=url, headers=headers, data=payload).content.decode('UTF-8'))

class HubSpotAPI:
	@classmethod
	def fetch_access_token(cls, request, refresh_token, service):
		'''
			Handle create or update token in database
			- token {str} -- a Credential instance
			- service {DjangoRemoteApp} -- a DjangoRemoteApp instance generate from Authlib
		'''
		url = 'https://api.hubapi.com/oauth/v1/token'
		
		payload = {
				'client_id': service.client_id,
				'client_secret': service.client_secret,
				'redirect_uri': request.scheme + '://' + request.get_host() + '/accounts/hubspot/auth/callback',
				'refresh_token': refresh_token,
				'grant_type': 'refresh_token'
		}
				
		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded',
		}
		
		# fetch data
		return request('POST', url=url, headers=headers, data=payload)

	@classmethod
	def fetch_make_offer_deals(cls, access_token):
		'''Fetch make offfer deals from Hubspot API server'''
		url = 'https://api.hubapi.com/crm/v3/objects/deals/search' # + '?hapikey=325cadcb-2526-4d69-befc-e0faa744726a'
		
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
					'value': MAKE_OFFER #Make Offer ID
				}]
			}],
			'properties': properties,
			'limit': 20
		}
				
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': 'Bearer ' + access_token
		}
		
		# fetch data
		return loads(request('POST', url=url, headers=headers, data=dumps(payload)).content.decode('UTF-8'))
