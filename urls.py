from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('rest_api.urls')),

    # Examples:
    # url(r'^$', 'mytest.views.home', name='home'),
    # url(r'^mytest/', include('mytest.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
