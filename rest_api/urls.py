from django.conf.urls.defaults import *
from tastypie.api import Api
from rest_api.api import UrlResource

v1_api = Api(api_name='v1')
v1_api.register(UrlResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)
