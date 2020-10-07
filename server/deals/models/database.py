from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime, timedelta
from tzlocal import get_localzone

from .constants import FETCHING_TIME

class Account:        
    @classmethod
    def find_user(cls, user_id):
        '''Find user from database'''
        
        if not isinstance(user_id, str):
            raise TypeError("user_id must be an string")

        if '@' in user_id: # if user_id is an email
            try: 
                User.objects.get(email=user_id)
            except:
                return None
            else:
                return User.objects.get(email=user_id)

        else: # if user_id is a username
            try:
                User.objects.get(username=user_id)
            except:
                return None
            else:
                return User.objects.get(username=user_id)
                
    @classmethod
    def authenticate(cls, user_id, password):
        """
        Handle authenticate process
        """
        if not isinstance(user_id, str):
            raise TypeError("user_id must be an string")
        if not isinstance(password, str):
            raise TypeError("user_id must be an string")
        
        user = cls.find_user(user_id)
        
        # Verify password
        if check_password(password, user.password):
            return user

        return None
    
    @classmethod
    def generate_profile(cls, user):
        '''Return user's profile in JSON format'''
        if not isinstance(user, User):
            raise TypeError("user must be an User instance")
                   
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
        	profile['service']['hubspot']['is_available'] = False
        
        return profile

class Cache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deal_id = models.TextField()
    folder_id = models.TextField(null=True)
    status = models.TextField(null=True)
    
    @classmethod
    def get_deal_cache(cls, user, deal_id):
        '''Get deal cache
            Arguments:
                - user: User instance
                - deal_id: id of deal
        '''
        if not isinstance(user, User):
            raise TypeError("user must be an User instance")
        if not isinstance(deal_id, str):
            raise TypeError("deal_id must be a string")
        
        try:
            cls.objects.get(user=user, deal_id=deal_id)
        except:
            return None
        else:
            return cls.objects.get(user=user, deal_id=deal_id)
            
    @classmethod
    def clean_cache(cls, user, deal_id_list):
        '''Clean use cache

            Arguments:
                - deal_id_list: list of available deal
        '''
        if not isinstance(user, User):
            raise TypeError('user must be an User instance')
        if not isinstance(deal_id_list, list):
            raise TypeError('deal_id_list must be a list')
        
        deal_caches = cls.objects.filter(user=user)
        
        for cache in list(deal_caches):
            if cache.deal_id not in deal_id_list:
                cache.delete()

    @classmethod
    def caches_to_json(cls, user):
        '''Return list of cache info in JSON format'''
        if not isinstance(user, User):
            raise TypeError('user must be an User instance')
        
        deal_caches = cls.objects.filter(user=user)
        
        caches = []
        
        for cache in list(deal_caches):
            caches.append(cache.to_json())
           
        return caches
           
    def to_json(self):
        '''Return cache info in JSON format'''
        return {
            'deal_id': self.deal_id,
            'folder_id': self.folder_id,
            'status': self.status
        }
         
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
    def fetch_credential(cls, user):
        '''Fetch credential of the user from database
        
            Arguments:
                - user {User} - django models Object
           
            Return:
                - None if no credential found
                - GoogleToken object if found
        '''
        if not isinstance(user, User):
            raise TypeError("user must be an User instance")

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
            
            Returns:
                - True: registered success
                - False: fail
        '''
        # validate input 
        if not isinstance(token, dict):
            raise TypeError('token MUST be a dictionary')
        if not isinstance(user, User):
            raise TypeError('user MUST be User instance')
        
        # check for credential in database
        credential = cls.fetch_credential(user=user) 
        
        if credential is None:
            if 'refresh_token' in list(token.keys()):
                cls.objects.create(user=user, refresh_token=token['refresh_token'], 
                    access_token=token['access_token'], expires_in=int(token['expires_in']), 
                    expires_at=datetime.now(get_localzone())+timedelta(seconds=int(token['expires_in'])-FETCHING_TIME))
                    
                return 'registered'
                
            else:
                return 'fail'
                
        else: # update if credential exists
            if 'refresh_token' in list(token.keys()):
                credential.refresh_token = token['refresh_token']
            credential.access_token = token['access_token']
            credential.expires_in = int(token['expires_in'])
            credential.expires_at = datetime.now(get_localzone())+timedelta(seconds=int(token['expires_in'])-FETCHING_TIME)
            credential.update_time = datetime.now(get_localzone())
            credential.save()
            
            return 'updated'
          
    def to_json(self):
        '''Return token info in JSON format'''
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': self.expires_in,
            'expires_at': self.expires_at.isoformat()
        }
        
class State(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.TextField()
    expires_in = models.PositiveIntegerField()
    expires_at = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    
    @classmethod
    def register_state(cls, user, state):
        '''Find user from database'''
        
        if not isinstance(user, User):
            raise TypeError("user must be an a User instance")
        if not isinstance(state, str):
            raise TypeError("user must be an a string")
        
        # check if there is a unused state
        try:
            cls.objects.get(user=user)
        except:
            pass
        else:
            cls.objects.get(user=user).delete()
        
        cls.objects.create(user=user, state=state)  
      
    @classmethod
    def find_state(cls, user):
        '''Find user from database'''
        
        if not isinstance(user, User):
            raise TypeError("user must be an a User instance")
        
        # check if there is a unused state
        try:
            cls.objects.get(user=user)
        except:
            return None
        else:
            return cls.objects.get(user=user)
             
        
# Google credential
class GoogleToken(Credential):
	pass

# Hubspot credential
class HubspotToken(Credential):
	pass