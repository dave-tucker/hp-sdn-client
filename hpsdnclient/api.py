#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person obtaining a copy
# of this software  and associated documentation files (the "Software"), to deal
# in the Software without restriction,  including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or  substantial portions of the Software.#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED,  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR  PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF  OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#

"""This library provides a Python interface to the HP SDN Controller API"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.0.1'

import json
import time

import requests

from error import FlareApiError
import core
import net
import of

class ApiBase(object):
    def __init__(self,
                 controller,
                 user,
                 password
                ):
    
        self.controller = controller
        self.user = user
        self.password = password

class Api(ApiBase, of.Of):
    def __init__(self, **kwds):
        super(Api, self).__init__(**kwds)
        self.auth_token = XAuthToken(controller = self.controller,
                                     user = self.user,
                                     password = self.password)
 

class XAuthToken(requests.auth.AuthBase, ApiBase):
    def __init__(self, **kwds):
        super(XAuthToken, self).__init__(**kwds)
        
        self.token = None
        self.token_expiration = None

    def __call__(self, r):
        if self.token is None or self.token_expiration <= time.gmtime():
            self.get_auth()
        r.headers['X-Auth-Token'] = self.token
        return r

    def get_auth(self):
        url = 'http://{0}:8080/sdn/v2.0/auth'.format(self.controller)
        payload = {'login':{ 'user': self.user, 'password': self.password}}
        r = requests.post(url, data=json.dumps(payload))
        if r.status_code == requests.codes.ok:
            data = r.json()
            self.token = data[u'record'][u'token']
            self.token_expiration = time.gmtime(data[u'record'][u'expiration']/1000)
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def delete_auth(self):
        url = 'http://{0}:8080/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token":self.token}
        r = requests.delete(url, headers=headers)
        if r.status_code == requests.codes.ok:
            self.token = None
            self.token_expiration = None
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()
