from django.contrib import admin
from tastypie.models import ApiKey
from rest_api.models import Url

class ApiKeyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ApiKey, ApiKeyAdmin)


class UrlAdmin(admin.ModelAdmin):
    pass

admin.site.register(Url)
