from django.http import HttpRequest

from requests import post, put, get, delete
from json import loads, dumps
from datetime import datetime

import os
import re

from .thread import requestThread
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
		
		payload = {
			'client_id': service.client_id,
			'client_secret': service.client_secret,
			'refresh_token': refresh_token,
			'grant_type': 'refresh_token'
		}

		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded'
		}
		
		url = 'https://oauth2.googleapis.com/token'
		
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
				
		# # upload template
		with open('template/ENG_INIT_Lead_YYYY_MM_DD.pptx', 'rb') as f:
			return put(response.headers.get('Location'), data=f)
						
	@classmethod
	def retrieve_token_info(cls, access_token):
		'''Retrieve access token infomation from google server'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')

		return get('https://gmail.googleapis.com/gmail/v1/users/me/profile', 
					headers={'Authorization': 'Bearer ' + access_token})

	@classmethod
	def revoke_credential(cls, refresh_token):
		'''Revoke unused creadential'''
		if not isinstance(refresh_token, str):
			raise TypeError('refresh_token must be a string')

		return post('https://oauth2.googleapis.com/revoke', params={'token': refresh_token},
				    headers = {'content-type': 'application/x-www-form-urlencoded'})
	
	@staticmethod
	def get_presentation_revision_id(access_token, slide_id):
		'''Retrieve revision id from google server'''
		
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(slide_id, str):
			raise TypeError('slide_id must be a string')
		
		return get(url='https://slides.googleapis.com/v1/presentations/' + slide_id,
					headers={'Authorization': 'Bearer ' + access_token})
	
	@classmethod
	def fill_out_the_template(cls, access_token, deal, company, notes, slide_id): # need to be refactored
		'''Retrieve revision id from google server'''
		
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(slide_id, str):
			raise TypeError('slide_id must be a string')
		if not isinstance(deal, dict):
			raise TypeError('deal must be a dict')
		if not isinstance(company, (dict, type(None))):
			raise TypeError('company must be a dict')
		if not isinstance(notes, dict):
			raise TypeError('notes must be a dict')

		response = cls.get_presentation_revision_id(access_token, slide_id)
		
		if response.status_code != 200:
			return response
		
		revision_id = response.json()['revisionId']
				
		payload = { # need to refactor
			'requests': [
				# can add more object to commit serveral text replacement in the whole slide
				# {
				# 	'replaceAllText': {
				# 		'replaceText': ,
				# 		'pageObjectIds': [],
				# 		'containsText': {
				# 			'text': , # put replacement text here
				# 			'matchCase': True
				# 		}
				# 	}
				# },
				{
					'replaceAllText': {
						'replaceText': notes['attachments'], # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Attachment>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': notes['urls'], # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Link>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['technology'].replace(';', ', ') if deal['properties']['technology'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Technology>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['technologies'].replace(';', ', ') if deal['properties']['technologies'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Technologies>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['os'].replace(';', ', ') if deal['properties']['os'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<OS>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['database'].replace(';', ', ') if deal['properties']['database'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Database>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['cms'].replace(';', ', ') if deal['properties']['cms'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<CMS>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['browsers'].replace(';', ', ') if deal['properties']['browsers'] is not None else '', # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Browsers>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['new_renew'], # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<New/Renew>', # put replacement text here
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['dev_'], # put infomation here
						'pageObjectIds': [],
						'containsText': {
							'text': '<Dev#>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['duration'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Duration>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['amount'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Amount>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['dealname'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Proposal Name>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['description'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Shortdescription>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['lead_overview_1'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Lead overview 1>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': deal['properties']['lead_overview_2'],
						'pageObjectIds': [],
						'containsText': {
							'text': '<Lead overview 2>',
							'matchCase': True
						}
					}
				},
				{
					'replaceAllText': {
						'replaceText': datetime.now().strftime("%d/%m/%Y"), #retrieve current date
						'pageObjectIds': [],
						'containsText': {
							'text': '<DD_MM_YYYY>',
							'matchCase': True
						}
					}
				}
			],
			'writeControl': {
				'requiredRevisionId': revision_id
			}
		}
		
		if company is not None:
			payload['requests'].append({
				'replaceAllText': {
					'replaceText': company['properties']['name'],
					'pageObjectIds': [],
					'containsText': {
						'text': '<Customer Name>',
						'matchCase': True
					}
				}
			})
				
		return post(url='https://slides.googleapis.com/v1/presentations/' + slide_id + ':batchUpdate',
					headers={'Authorization': 'Bearer ' + access_token}, data=dumps(payload))
		
class HubspotAPI:
	@classmethod
	def fetch_make_offer_deals(cls, access_token, properties):
		'''Fetch make offer deals from Hubspot API server'''
		
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		
		# properties = ['dealname','description','deal_summary','lead_overview_1','lead_overview_2','start_date','closedate'\
		# 				'ambassador', 'dev_', 'os', 'amount', 'pipeline', 'deal_currency_code', 'hubspot_owner_id', \
		# 				'amount_in_home_currency', 'technologies', 'technology', 'notes_last_contacted', 'notes_last_updated',\
		# 				'duration', 'new_renew', 'browsers', 'cms', 'database']
		
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
		return post(url='https://api.hubapi.com/crm/v3/objects/deals/search', headers=headers, data=dumps(payload))
	
	@staticmethod
	def fetch_assosiation_object_info_from_deal_ID(access_token, dealID, assosiation_object):
		'''fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		
		return get(url='https://api.hubapi.com/crm/v3/objects/deals/' + dealID + '/associations/' + assosiation_object,\
			 		headers={'Authorization': 'Bearer ' + access_token })
		
	@classmethod
	def fetch_company_info(cls, access_token, dealID):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(dealID, str):
			raise TypeError('dealID must be a string')

		response = cls.fetch_assosiation_object_info_from_deal_ID(access_token, dealID, 'companies')
		
		if response.status_code != 200:
			return response
			
		return get(url='https://api.hubapi.com/crm/v3/objects/companies/' + response.json()['results'][0]['id'],
					 headers={'Authorization': 'Bearer ' + access_token})
	
	@classmethod
	def retrieve_token_info(cls, access_token):
		'''Retrieve access token infomation from hubspot server'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		
		return get('https://api.hubapi.com/oauth/v1/access-tokens/' + access_token)
	
	@classmethod
	def revoke_credential(cls, refresh_token):
		'''Revoke unused creadential'''
		if not isinstance(refresh_token, str):
			raise TypeError('refresh_token must be a string')
		
		return delete('https://api.hubapi.com/oauth/v1/refresh-tokens/' + refresh_token)
		
	@staticmethod
	def fetch_engagement_info(access_token, engagement_id):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(engagement_id, str):
			raise TypeError('engagement_id must be a string')
		
		return get(url='https://api.hubapi.com/engagements/v1/engagements/' + engagement_id,
				headers={'Authorization': 'Bearer ' + access_token})
	
	@staticmethod
	def fetch_attachment_info(access_token, attachment_id):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(attachment_id, str):
			raise TypeError('attachment_id must be a string')
		
		return get(url='https://api.hubapi.com/filemanager/api/v2/files/' + attachment_id,
					 headers={'Authorization': 'Bearer ' + access_token})
					 
	@classmethod
	def fetch_owner_info(cls, access_token, owner_id):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(owner_id, str):
			raise TypeError('dealID must be a string')
		
		return get(url='https://api.hubapi.com/crm/v3/owners/' + owner_id,
					 headers={'Authorization': 'Bearer ' + access_token})
	
	@classmethod
	def fetch_deal_info(cls, access_token, deal_id):
		'''Fetch from hubspot'''
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(deal_id, str):
			raise TypeError('deal_id must be a string')
		
		properties = ['dealname','description','deal_summary','lead_overview_1','lead_overview_2','start_date','closedate'\
					'ambassador', 'dev_', 'os', 'amount', 'pipeline', 'deal_currency_code', 'hubspot_owner_id', \
					'amount_in_home_currency', 'technologies', 'technology', 'notes_last_contacted', 'notes_last_updated',\
					'duration', 'new_renew', 'browsers', 'cms', 'database'] # need to be refactored

		urlencoded = '?' 

		for prop in properties:
			urlencoded += '&properties='
			urlencoded += prop
				 
		return get(url='https://api.hubapi.com/crm/v3/objects/deals/' + deal_id + urlencoded,
					 headers={'Authorization': 'Bearer ' + access_token})
					 
	@classmethod
	def fetch_notes(cls, access_token, deal_id):
		'''Prepare notes data'''
		
		if not isinstance(access_token, str):
			raise TypeError('access_token must be a string')
		if not isinstance(deal_id, str):
			raise TypeError('dealID must be a string')

		res = cls.fetch_assosiation_object_info_from_deal_ID(access_token, deal_id, 'engagements')

		if res.status_code != 200:
			return res
		
		threads = []
		notes = []
		
		for item in res.json()['results']:
			thread = requestThread(target=cls.fetch_engagement_info, kwargs={'access_token': access_token, 'engagement_id': item['id']})
			threads.append(thread)
			thread.start()

		for thread in threads:
			notes.append(thread.join())
		
		attachments_id = []
		urls = ''
		
		for note in notes:
			if note.status_code != 200:
				return note
				
			if note.json()['attachments'] != []:
				attachments_id.extend(note.json()['attachments'])
				
			try:
				note.json()['engagement']['bodyPreview']
			except:
				pass
			else:
				if re.match(r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", note.json()['engagement']['bodyPreview']):
					if urls != '':
						urls += ' '
						
					urls += note.json()['engagement']['bodyPreview']
		
		attachments = []
		threads = []
		
		for item in attachments_id:
			thread = requestThread(target=cls.fetch_attachment_info, kwargs={'access_token': access_token, 'attachment_id': str(item['id'])})
			threads.append(thread)
			thread.start()
		
		for thread in threads:
			attachments.append(thread.join())

		attachments_url = ''
		
		for item in attachments:
			if item.status_code != 200:
				return item
				
			if attachments_url != '':
				attachments_url += ' '
				
			attachments_url += item.json()['url']
			
		return {
			'attachments': attachments_url,
			'urls': urls,
		}