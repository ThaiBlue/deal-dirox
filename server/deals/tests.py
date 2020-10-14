from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest

from authlib.integrations.django_client import OAuth
from urllib.parse import urlencode, urlparse, parse_qs
from tzlocal import get_localzone
from datetime import datetime
from random import randint
from json import dumps
import uuid

from .models.database import Account, GoogleToken, HubspotToken, Cache
from .handlers import User as UserAPI
from .models.constants import *

# Initiate OAuth2 session
oauth = OAuth()

# Register service
oauth.register('google')
oauth.register('hubspot')

# Test configuration
USERNAME = 'thaitc'
USER_EMAIl = 'thai.tran@dirox.net'
PASSWORD = 'Blueskull0219'
GOOGLE_TOKEN = '1//0ekgxL5BLTJhyCgYIARAAGA4SNwF-L9Irz130vK3fI-4ER5Dmt_ypKjG6MBrXLOQ1WssDTaRbgGEBUC5ADDisAisKvzWJw2VgVH0'
HUBSPOT_TOKEN = '47292441-c8b7-42cd-96f2-2ed6ecfd79c3'

class PseudoRequestObject:	
	def __init__(self, user):
		self.user = user
		self.session = {'sess_key': str(uuid.uuid4())}

class APITestCase(TestCase):
	'''A set of API test case'''
	
	login_url = '/accounts/user/login'
	logout_url = '/accounts/user/logout'
	profile_url = '/accounts/user/profile'
	google_auth_url = '/accounts/google/auth'
	hubspot_auth_url = '/accounts/hubspot/auth'
	google_callback_url = '/accounts/google/auth/callback'
	hubspot_callback_url = '/accounts/hubspot/auth/callback'
	cache_url = '/accounts/setting/cache'
	google_token_url = '/services/google/auth/token'
	hubspot_token_url = '/services/google/auth/token'
	google_info_url = '/services/google/info'
	google_token_revoke_url = '/services/google/auth/token/revoke'
	hubspot_info_url = '/services/hubspot/info'
	hubspot_token_revoke_url = '/services/hubspot/auth/token/revoke'
	initlead_create_url = '/services/google/drive/file/create/initlead'
	fetch_all_deals_url = '/services/hubspot/crm/deals/makeoffer/all'
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username=USERNAME, email=USER_EMAIl, password='')
		self.request = PseudoRequestObject(self.user)
		# self.google_token = GoogleToken.objects.create(user=self.user, access_token='empty', refresh_token=GOOGLE_TOKEN,\
		# 	 expires_in=60, expires_at=datetime.now(get_localzone()))
		# self.hubspot_token = HubspotToken.objects.create(user=self.user, access_token='empty', refresh_token=HUBSPOT_TOKEN,\
		# 	 expires_in=60, expires_at=datetime.now(get_localzone()))
			 		
	def __method_not_allowed_case(self, url):
		'''Test if Method not allowed protector still works'''
		for method in ['post', 'put', 'delete']:
			self.assertEqual(eval(f'self.client.{method}')(url).status_code, 405,\
				 msg='Method not allowed case failed')

	def __initial_login(self):
		'''Login request to gain API access permission'''
		self.client.get(f'{self.login_url}?user_id={USERNAME}&password={PASSWORD}')
		
	def __login_required_case(self, url):
		'''Test if authenticate protector still works'''
		msg='Login required case failed'
		res = self.client.get(url)
		self.assertEqual(res.status_code, 400, msg)
		self.assertJSONEqual(res.content, HTTP_400_LOGIN_REQUIRE.content.decode('utf-8'), msg)
		
	def __security_test_case(self, url):
		'''A set of test case that need to be test at the beginning of any API test excepts login API'''
		# Test if security protection mechanic still work
		self.__login_required_case(url)
		# Gain access right
		self.__initial_login()
		# Wrong method case
		self.__method_not_allowed_case(url)
		
	def test_login(self):
		'''Test login API'''
		# Wrong method case
		self.__method_not_allowed_case(self.login_url)
		
		# Wrong query format
		msg = 'Wrong query format case failed'
		for query in ['user_id=&password=', f'user_id={USERNAME}&pass={PASSWORD}', f'userid={USERNAME}&password={PASSWORD}', '']:
			res = self.client.get(f'{self.login_url}?{query}')
			self.assertEqual(res.status_code, 400, msg=msg)
			self.assertJSONEqual(res.content, HTTP_400_INVALID_QUERY.content.decode('utf-8'), msg)
		
		# Wrong username case
		msg='Wrong username case failed'
		for id_ in ['wrong_id', 123, 'email@yahoo.com']:
			res = self.client.get(f'{self.login_url}?user_id={id_}&password={PASSWORD}')
			self.assertEqual(res.status_code, 400, msg)
			self.assertJSONEqual(res.content, HTTP_400_USER_NOT_FOUND.content.decode('utf-8'), msg)
		
		# Wrong password case
		msg='Wrong password case failed'
		for pwd in ['wrong', 123, USERNAME]:
			res = self.client.get(f'{self.login_url}?user_id={USERNAME}&password={pwd}')
			self.assertEqual(res.status_code, 400, msg)
			self.assertJSONEqual(res.content, HTTP_400_WRONG_PASSWORD.content.decode('utf-8'), msg)

		# Login with username case
		msg='Login with username case failed'
		res = self.client.get(f'{self.login_url}?user_id={USERNAME}&password={PASSWORD}')
		self.assertEqual(res.status_code, 200, msg)
		self.assertJSONEqual(res.content, dumps(Account.generate_profile(self.user)), msg)

		# Login with enail case
		msg='Login with email case failed'
		res = self.client.get(f'{self.login_url}?user_id={USER_EMAIl}&password={PASSWORD}')
		self.assertEqual(res.status_code, 200, msg)
		self.assertJSONEqual(res.content, dumps(Account.generate_profile(self.user)), msg)
			
	def test_logout(self):
		'''Test logout API'''
		self.__security_test_case(self.logout_url)
				
		# Log out case
		msg='Log out case status code failed'
		res = self.client.get(self.logout_url)
		self.assertEqual(res.status_code, 200, msg)
		self.assertJSONEqual(res.content, dumps({'uid': self.user.username, 'status':'logout success'}), msg)
	
	def test_profile(self):
		'''Test profile retrieve API'''
		self.__security_test_case(self.profile_url)
		
		# Fetch profile case
		msg='Fetch profile case failed'
		res = self.client.get(self.profile_url)
		self.assertEqual(res.status_code, 200, msg)
		self.assertJSONEqual(res.content, dumps(Account.generate_profile(self.user)), msg)
	
	def test_fetch_google_token(self):
		'''Test google token provider API'''
		self.__security_test_case(self.google_token_url)
		
		# No service case
		msg='No service case failed'
		res = self.client.get(self.google_token_url)
		self.assertEqual(res.status_code, 400, msg)
		self.assertJSONEqual(res.content, HTTP_400_NO_SERVICE_AVAILABLE.content.decode('utf-8'), msg)
		
		# Add a service
		self.google_token = GoogleToken.objects.create(user=self.user, access_token='empty', refresh_token=GOOGLE_TOKEN,\
			expires_in=60, expires_at=datetime.now(get_localzone()))
		
		# Fetch token success case
		msg='Fetch success case failed'
		res = self.client.get(self.google_token_url)
		self.assertContains(response=res, text='access_token', count=1, status_code=200, msg_prefix=msg)

	def test_fetch_hubspot_token(self):
		'''Test hubspot token provider API'''
		self.__security_test_case(self.hubspot_token_url)
		# Other case need to be tested with a HTTPS host
								
	def test_cache(self):
		'''Test setting cache cache API'''
		self.__security_test_case(self.cache_url)
		
		# Cache request fail case
		msg='Cache request fail case failed'
		for query in ['status=&folder_id=123' , 'status=Create+Folder&folder=123&deal_id=22313423' , 'deal_id=123134']:
			res = self.client.get(f'{self.cache_url}?{query}')
			self.assertEqual(res.status_code, 400, msg)
			self.assertJSONEqual(res.content, HTTP_400_CACHE_REQUEST_FAIL.content.decode('utf-8'), msg)
			
		# First time cache case
		msg='First time cache case failed'
		for param in [{'status': 'Create Folder', 'folder_id': randint(0, 999999), 'deal_id': 123}, {'status': 'Any String', 'folder_id': randint(0, 999999), 'deal_id': 234}]:
			res = self.client.get(f'{self.cache_url}?{urlencode(param)}')
			self.assertEqual(res.status_code, 200, msg)
			# Verify cache data
			cache = Cache.get_deal_cache(user=self.user, deal_id=str(param['deal_id']))
			self.assertEqual(cache.status, param['status'], msg)
			self.assertEqual(cache.folder_id, str(param['folder_id']), msg)
						
		# Update cache case
		msg='Update cache case failed'
		for param in [{'status': 'Transfer to BA', 'folder_id': randint(0, 999999), 'deal_id': 123}, {'status': 'Some String', 'folder_id': randint(0, 999999), 'deal_id': 234}]:
			res = self.client.get(f'{self.cache_url}?{urlencode(param)}')
			self.assertEqual(res.status_code, 200, msg)
			# Verify cache data
			cache = Cache.get_deal_cache(user=self.user, deal_id=str(param['deal_id']))
			self.assertEqual(cache.status, param['status'], msg)
			self.assertEqual(cache.folder_id, str(param['folder_id']), msg)
			
	def test_google_authorize(self):
		'''Test google authorize oauth2 API'''
		self.__security_test_case(self.google_auth_url)

		service_ = oauth.create_client('google')
		
		# request success case
		msg = 'Authorize request success case failed'
		res = self.client.get(self.google_auth_url)
		self.assertEqual(res.status_code, 302, msg)
		
		res_url = urlparse(res.get('Location'))
		valid_url = urlparse(service_.authorize_redirect(self.request, 'https://testserver/accounts/google/auth/callback').get('Location'))
		
		self.assertEqual(response_url.scheme, valid_url.scheme, msg)
		self.assertEqual(response_url.netloc, valid_url.netloc, msg)
		self.assertEqual(response_url.path, valid_url.path, msg)
		
		res_query = parse_qs(response_url.query).pop('state')
		valid_query = parse_qs(valid_url.query).pop('state')
		
		self.assertDictEqual(res_query, valid_query, msg)

				
	def test_hubspot_authorize(self):
		'''Test hubspot authorize oauth2 API'''
		self.__security_test_case(self.hubspot_auth_url)
		# Other case need to be tested with a HTTPS host

	def test_google_callback(self):	
		'''Test google callback oauth2 API'''
		self.__security_test_case(self.google_callback_url)
		# Other case need to be tested on a browser

	def test_hubspot_callback(self):	
		'''Test hubspot callback oauth2 API'''
		self.__security_test_case(self.hubspot_callback_url)
		# Other case need to be tested with a HTTPS host
		
	def test_(self):
		'''Test '''