from django.db import models
from django.contrib.auth.models import User

from tastypie.models import create_api_key
models.signals.post_save.connect(create_api_key, sender=User)


class Url(models.Model):
    long_url = models.CharField(max_length=250, unique=True)
    key = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return "<%s, %s>"  % (self.id, self.long_url)
