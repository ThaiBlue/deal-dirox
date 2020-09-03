from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta

from .constants import FETCHING_TIME

class Account(User):
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

# OAuth2 Credential model
class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expiration_in = models.PositiveIntegerField()
    expiration_at = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    
    @classmethod
    def fetch_credential(cls, user):
        try: # check if user had registered a google account yet
        	cls.objects.get(user=user)
        except: # if no credential exists
            return None
        else: # return the credential
            return cls.objects.get(user=user)
            
    @classmethod
    def register_credential(cls, token, user):
        '''Handle create or update token in database
           - token {dict} -- a Credential instance
           - user {User} -- a User instance
        '''
        # check for credential in database
        credential = cls.fetch_credential(user=user) 
        
        if credential is None:
        	cls.objects.create(user=user, refresh_token=token['refresh_token'], 
                access_token=token['access_token'], expiration_in=int(token['expiration_in']), 
                expiration_at=datetime.utcnow()+timedelta(seconds=int(token['expiration_in']-FETCHING_TIME)))
                
        else: # update if credential exists
            credential.access_token = token['access_token']
            credential.refresh_token = token['refresh_token']
            credential.expiration_in = int(token['expiration_in'])
            credential.expiration_at = datetime.utcnow()+timedelta(seconds=int(token['expiration_in']-FETCHING_TIME))
            credential.update_time = datetime.utcnow()
            credential.save()
          
    def to_json(self):
        '''Return token info in JSON format'''
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expiration_in': self.expiration_in,
            'expiration_at': self.expiration_at.utcoffset()
        }
        
# Google credential
class GoogleToken(Credential):
	pass

# Hubspot credential
class HubspotToken(Credential):
	pass
