import json
import unittest
from random import random

from funkload.utils import Data
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Simple(FunkLoadTestCase):
    def setUp(self):
        self.server_url = self.conf_get('main', 'url')
        self.server_params = self.conf_get('main', 'params')

    def test_check(self):
        # post with text/xml content type
        response = self.post(self.server_url + '/api/v1/url/' + self.server_params, 
                params=Data('application/json', '{"long_url": "http://hakta.com"}'),
                description="Initial post to create a url", ok_codes=[201])
        target = response.headers['Location']

        nb_time = self.conf_getInt('test_check', 'nb_time')
        for i in range(nb_time):
            response = self.get(target + self.server_params, description='Get url')

        self.assertNotEqual(json.loads(response.body)['key'], None)
        self.assertNotEqual(json.loads(response.body)['key'], '')


if __name__ in ('main', '__main__'):
    unittest.main()
