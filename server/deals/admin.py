from django.contrib import admin
from .models import GoogleToken, HubspotToken, Cache

# Register your models here.
admin.site.register(GoogleToken)
admin.site.register(HubspotToken)
admin.site.register(Cache)