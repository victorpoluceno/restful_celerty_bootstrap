from django.db import models

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.throttle import CacheThrottle
from tastypie.validation import FormValidation

from celery.execute import send_task
from celery.result import EagerResult

from rest_api.models import Url
from rest_api.forms import UrlForm
from rest_api.tasks import url_short

from django.conf import settings


class UrlThrottle(CacheThrottle):
    def should_be_throttled(self, identifier, **kwargs):
        try:
            should_be_throttled = settings.SHOULD_BE_THROTTLED
        except (AttributeError), e:
            should_be_throttled = True

        if super(UrlThrottle, self).should_be_throttled(identifier, **kwargs) \
                and should_be_throttled:
                return True

        return False


class UrlResource(ModelResource):
    class Meta:
        resource_name = 'url'
        queryset = Url.objects.all()
        fields = ['long_url', 'key']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        throttle = UrlThrottle(throttle_at=100)
        allowed_methods = ['get', 'post']
        validation = FormValidation(form_class=UrlForm)


def url_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if kwargs.get('created') == True:
        #FIXME: use send_task is much better to declouping workers from web server
        # but send_task does not seems to return a EagerResult on tests, when docs
        # says that it should so. Make a minimal sample and try to fix it on celery
        #r = send_task('rest_api.tasks.url_short', [instance.id]) 
        url_short.delay(instance.id)

models.signals.post_save.connect(url_post_save, sender=Url, 
        dispatch_uid='url_create')
