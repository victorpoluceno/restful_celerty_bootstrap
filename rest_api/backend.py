import random
import string
import json
import requests

from abc import abstractmethod

from django.conf import settings


class UrlShortner(object):

    @abstractmethod
    def create(url):
        pass


def random_key():
    return ''.join(random.choice(string.letters + string.digits) 
        for i in xrange(10)) 


class GoogleSandBox(UrlShortner):

    @staticmethod
    def create(long_url):
        # fake request to simulate network latency
        requests.post('https://google.com')
        return 'http://sandbox/%s' % random_key()


class Google(UrlShortner):

    @staticmethod
    def create(long_url):
        response = requests.post('http://goo.gl/api/url', 
                params={'url': long_url})
        results = json.loads(response.content)
        return results['short_url']
       

class Request(object):

    def __init__(self, backend=GoogleSandBox):
        if 'SHORTNER_BACKEND' in dir(settings):
            backend = __import__(settings.SHORTNER_BACKEND)

        self.shortner = backend()

    def __getattr__(self, attr):
        return getattr(self.shortner, attr)
