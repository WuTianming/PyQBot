#!/usr/bin/env python3

import json
from urllib import request, parse

class tuling(object):
    url_req = "http://www.tuling123.com/openapi/api"

    def __init__(self, APIKey=None):
        if str(APIKey) in ('None', ''):
            print('You\'ll have to provide an APIKey first.')
            print('Get it @ http://tuling123.com')
            raise ValueError('APIKey not available')
        else:
            self.key = APIKey

    def response(self, msg, uin):
        d = parse.urlencode(
                {'key': self.key, 'info': msg, 'userid': uin}).encode('utf-8')
        with request.urlopen(self.url_req, data=d) as f:
            j = json.loads(f.read().decode('utf-8'))
            return j['text']
