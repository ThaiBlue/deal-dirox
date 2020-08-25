from django.db import models
from django.contrib.auth.models import User

# OAuth2 Credential model
class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True)
    expiration_time = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

# Google credential
class GoogleToken(Credential):
	pass

# Hubspot credential
class HubspotToken(Credential):
	pass