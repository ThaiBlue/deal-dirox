from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from tzlocal import get_localzone
from django.db import models

from .constants import FETCHING_TIME

class Account:
    @classmethod
    def authenticate(cls, user_id, password):
    	"""
    	Handle authenticate process
    	"""
    	user = None
    	
    	if '@' in user_id: # if user_id is an email
    		try: 
    			User.objects.get(email=user_id)
    		except:
    			return None
    		else:
    			user = User.objects.get(email=user_id)

    	else: # if user_id is a username
    		try:
    			User.objects.get(username=user_id)
    		except:
    			return None
    		else:
    			user = User.objects.get(username=user_id)

    	# Verify password
    	if check_password(password, user.password):
    		return user
    	
    	return None
    
    @classmethod
    def generate_profile(cls, user):
        '''Return user's profile in JSON format'''
        profile = {
        	'status': 'online',
        	'username': user.username,
        	'service': {
        		'google': {
        			'is_available': True
        		},
        		'hubspot': {
        			'is_available': True
        		}
        			
        	}
        }

        token = GoogleToken.fetch_credential(user=user)
        if token is None:
        	profile['service']['google']['is_available'] = False
        	
        token = HubspotToken.fetch_credential(user=user)
        if token is None:
        	profile['service']['huspot']['is_available'] = False
        
        return profile

# OAuth2 Credential model
class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.PositiveIntegerField()
    expires_at = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    
    @classmethod
    def fetch_credential(cls, user=None):
        '''Fetch credential of the user from database
        
            Arguments:
                - user {User} - django models Object
           
            Return:
                - None if no credential found
                - GoogleToken object if found
        '''
        try: # check if user had registered a google account yet
        	cls.objects.get(user=user)
        except: # if no credential exists
            return None
        else: # return the credential
            return cls.objects.get(user=user)
    
    @classmethod
    def register_credential(cls, token, user):
        '''Handle create or update token in database
        
            Arguments:
                - token {dict} -- a Credential instance
                - user {User} -- a User instance
        '''
        # validate input 
        if not isinstance(token, dict):
            raise TypeError('token MUST be a dictionary')
        if not isinstance(user, User):
            raise TypeError('user MUST be User instance')
        
        # check for credential in database
        credential = cls.fetch_credential(user=user) 
        
        if credential is None:
        	cls.objects.create(user=user, refresh_token=token['refresh_token'], 
                access_token=token['access_token'], expires_in=int(token['expires_in']), 
                expires_at=datetime.now(get_localzone())+timedelta(seconds=int(token['expires_in'])-FETCHING_TIME))
                
        else: # update if credential exists
            if 'refresh_token' in list(token.keys()):
                credential.refresh_token = token['refresh_token']
            credential.access_token = token['access_token']
            credential.expires_in = int(token['expires_in'])
            credential.expires_at = datetime.now(get_localzone())+timedelta(seconds=int(token['expires_in'])-FETCHING_TIME)
            credential.update_time = datetime.now(get_localzone())
            credential.save()
          
    def to_json(self):
        '''Return token info in JSON format
        '''
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': self.expires_in,
            'expires_at': self.expires_at.isoformat()
        }
        
# Google credential
class GoogleToken(Credential):
	pass

# Hubspot credential
class HubspotToken(Credential):
	pass