from requests import post, put, get, delete
from json import loads, dumps
from django.http import HttpRequest

from .constants import MAKE_OFFER

class OAuth2API:
	@classmethod
	def fetch_access_token(cls, request, refresh_token, service):
		'''
			Handle create or update token in database
			- token {str} -- a Credential instance
			- service {DjangoRemoteApp} -- a DjangoRemoteApp instance generate from Authlib
		'''
		
		if not isinstance(refresh_token, str):
			raise TypeError('refresh_token must be a string')
		if not isinstance(service, object):
			raise TypeError('service must be a string')
		if not isinstance(request, HttpRequest):
			raise TypeError('request must be a Django HttpRequest instance')
		
		url = 'https://oauth2.googleapis.com/token'

		payload = {
			'client_id': service.client_id,
			'client_secret': service.client_secret,
			'refresh_token': refresh_token,
			'grant_type': 'refresh_token'
		}

		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded'
		}
		
		if service.name == 'hubspot':
			url = 'https://api.hubapi.com/oauth/v1/token'
			payload['redirect_uri'] = request.scheme + '://' + request.get_host() + '/accounts/hubspot/auth/callback'

		# fetch data
		return post(url=url, headers=headers, data=payload)

class GoogleAPI:	
	@classmethod
	def upload_init_lead_template(cls, access_token, name, parentID=None):
		'''
			Create a new initLead template in user's 
			- access_token {str} -- google Bearer access token
			- parentID {str} -- identity value of user's Drive folder
			- name {str} -- name of the file
		'''
		if not isinstance(name, str):
			raise TypeError('name MUST be string')
		if not isinstance(parentID, str) and parentID is not None:
			raise TypeError('parentID MUST be string')
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')

				
		url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable"

		payload = {
		    'name': name,
		    'mimeType': 'application/vnd.google-apps.presentation',
		    'parents': []
		}
		
		if parentID is not None:
			payload['parents'].append(parentID)
		
		headers = {
			'Content-Type': 'application/json',
			'Content-Length': '0',
			'Authorization': 'Bearer ' + access_token
		}
		
		# request for a upload session
		response = post(url=url, headers=headers, data=dumps(payload))
		
		if response.status_code != 200:
			return response
			
		# upload template
		with open('template/ENG_INIT_Lead_2020_MM_DD.pptx', 'rb') as f:
		    return put(response.headers.get('Location'), data=f)
			
	@classmethod
	def retrieve_token_info(cls, access_token):
		'''Retrieve access token infomation from google server'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')

		return get('https://gmail.googleapis.com/gmail/v1/users/me/profile', 
					headers={'Authorization': 'Bearer ' + access_token}).json()

	@classmethod
	def revoke_credential(cls, refresh_token):
		'''Revoke unused creadential'''
		if not isinstance(refresh_token, str):
			raise TypeError('refresh_token must be a string')

		return post('https://oauth2.googleapis.com/revoke', params={'token': refresh_token},
				    headers = {'content-type': 'application/x-www-form-urlencoded'})
class HubspotAPI:
	@classmethod
	def fetch_make_offer_deals(cls, access_token):
		'''Fetch make offer deals from Hubspot API server'''
		
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')

		url = 'https://api.hubapi.com/crm/v3/objects/deals/search'
		
		properties = ['dealname','description','deal_summary','lead_overview_1','lead_overview_2','start_date','closedate']
		
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
		return post(url=url, headers=headers, data=dumps(payload)).json()
	
	@staticmethod
	def fetch_company_id_from_deal_ID(access_token, dealID):
		'''fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')

		url = 'https://api.hubapi.com/crm/v3/objects/deals/' + dealID + '/associations/companies'
		
		headers = {
			'Authorization': 'Bearer ' + access_token
		}
		
		return get(url=url, headers=headers).json()
		
	@classmethod
	def fetch_company_info(cls, access_token, dealID):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(dealID, str):
			raise TypeError('dealID must be a string')

		companyInfo = cls.fetch_company_id_from_deal_ID(access_token, dealID)
		
		url = 'https://api.hubapi.com/crm/v3/objects/companies/' + companyInfo['results'][0]['id']
		
		headers = {
			'Authorization': 'Bearer ' + access_token
		}
		
		return get(url=url, headers=headers).json()
	
	@classmethod
	def retrieve_token_info(cls, access_token):
		'''Retrieve access token infomation from hubspot server'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		
		return get('https://api.hubapi.com/oauth/v1/access-tokens/' + access_token).json()
	
	@classmethod
	def revoke_credential(cls, refresh_token):
		'''Revoke unused creadential'''
		if not isinstance(refresh_token, str):
			raise TypeError('refresh_token must be a string')
		
		return delete('https://api.hubapi.com/oauth/v1/refresh-tokens/' + refresh_token)
		