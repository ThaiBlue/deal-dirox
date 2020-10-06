from django.contrib.auth.models import User
from django.http import HttpRequest

from datetime import datetime, timedelta
from authlib.jose import jwt

from .database import Account
from .constants import ISO_TIME_FORMAT

import re

class Auth0:
	'''The module handle auth0 authentication process'''
	
	@classmethod
	def verify_identity(cls, request):
		'''Validate request's authorization'''
		
		if not isinstance(request, HttpRequest):
			raise TypeError('request must be a HttpRequest instance')
			
		credential = request.headers.get('Authorization')
		
		if credential is None:
			return None
		
		match = re.search(r'(?<=^Bearer ).+', credential)
		
		if match is None:
			return None
		
		token = match.group(0)
		
		try:
			jwt.decode(token, open('server/key/public.pem').read())
		except:
			return None
		else:
			claims = jwt.decode(token, open('server/key/public.pem').read())
			
		if datetime.utcnow() > datetime.strptime(claims.exp, ISO_TIME_FORMAT):
			return None
		
		user = Account.find_user(claims.sub)
		
		if user is None:
			return None
			
		return user
			
	@classmethod
	def jwt_token_generator(cls, request, user):
		'''Generate a jwt token'''
		
		if not isinstance(request, HttpRequest):
			raise TypeError('request must be a HttpRequest instance')
		if not isinstance(user, User):
			raise TypeError('user must be a User instance')
		
		return jwt.encode({'alg': 'RS256'}, {'iss': request.get_host(), 'sub': user.username, 'exp': (datetime.utcnow() + timedelta(hours=1)).isoformat()}, open('server/key/private.pem').read())