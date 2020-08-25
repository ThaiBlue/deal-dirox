from django.contrib import admin
from .models import GoogleToken, HubspotToken

# Register your models here.
admin.site.register(GoogleToken)
admin.site.register(HubspotToken)