#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import time

import requests

class XAuthToken(requests.auth.AuthBase):
    """This class handles authentication against the HP SDN REST API and
    uses the Requests API. XAuthToken derives from
    requests.auth.AuthBase and hpsdnclient.ApiBase."""

    def __init__(self, controller, user, password):
        """Initializes the class. Set the controller, user and password
        member variables. Sets the token and expiration values to
        None"""
        super(XAuthToken, self).__init__()
        self.controller = controller
        self.user = user
        self.password = password
        self.token = None
        self.token_expiration = None

    def __call__(self, r):
        """This method is called when an authentication token is
        required. We first check that the token exists and has not
        expired and then return the X-Auth-Token request header."""
        if self.token is None or self.token_expiration <= time.gmtime():
            self.get_auth()
        r.headers['X-Auth-Token'] = self.token
        return r

    def get_auth(self):
        """This method requests an authentication token from the SDN
        controller and returns a dictionary with the token and
        expiration time."""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        payload = {'login':{ 'user': self.user, 'password': self.password}}
        r = requests.post(url, data=json.dumps(payload),
                          verify=False, timeout=0.5)
        if r.status_code == 200:
            data = r.json()
            self.token = data[u'record'][u'token']
            exptime = data[u'record'][u'expiration']/1000
            self.token_expiration = time.gmtime(exptime)
        else:
            r.raise_for_status()

    def delete_auth(self):
        """Delete Authentication Token, AKA, Logout. This method logs
        the current user out"""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token":self.token}
        r = requests.delete(url, headers=headers,
                            verify=False, timeout=0.5)
        if r.status_code == 200:
            self.token = None
            self.token_expiration = None
        else:
            r.raise_for_status()
