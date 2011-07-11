from abc import abstractmethod
import json

import random
import string
import urllib
import urllib2
#import requests

from django.conf import settings

URL_SHORTNER_BACKEND = 'google'
URL_SHORTNER_SANDBOX = True


def random_key():
    return ''.join(random.choice(string.letters + string.digits) 
            for i in xrange(10)) 


class Request(object):
    def __init__(self):
        sandbox = settings.__dict__.get('URL_SHORTNER_SANDBOX', 
                URL_SHORTNER_SANDBOX)

        backend = settings.__dict__.get('URL_SHORTNER_BACKEND', 
                URL_SHORTNER_BACKEND)

        if backend == 'google':
            self.url_shortner = Google
        elif backend == 'bitly':
            self.url_shortner = Bitly
        else:
            raise UnknownBackendError()

        self.url_shortner.sandbox = True

    def __getattr__(self, attr):
        return getattr(self.url_shortner, attr)


class UrlShortner(object):

    @abstractmethod
    def create(url):
        pass


class Google(UrlShortner):
    url = 'http://goo.gl/api/url'

    @staticmethod
    def create(url):
        gurl = '%s?url=%s' % (self.url, urllib.quote(url))
        req = urllib2.Request(gurl, data='')
        results = json.load(urllib2.urlopen(req))
        return results['short_url']
       
        #TODO: why it doesnt work with requests lib? check what is wrong
        '''
        response = requests.get('http://goo.gl/api/url?url=%s' % urllib.quote(url))
        data = {'longUrl': url}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data)
        return key'''


class GoogleSandBox(UrlShortner):
    url = 'https://google.com'

    @staticmethod
    def create(url):
        request = urllib2.Request(self.url)
        result = urllib2.urlopen(request)
        return 'http://goo.gl/%s' random_key()


#TODO: implement
class Bitly(UrlShortner):
    pass 
