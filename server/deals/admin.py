from django.contrib import admin
from .models import GoogleToken, HubspotToken, Account

# Register your models here.
admin.site.register(GoogleToken)
admin.site.register(HubspotToken)