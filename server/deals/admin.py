from .models.database import GoogleToken, HubspotToken, Cache
from django.contrib import admin

# Register your models here.
admin.site.register(GoogleToken)
admin.site.register(HubspotToken)
admin.site.register(Cache)