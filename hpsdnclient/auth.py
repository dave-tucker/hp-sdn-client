#!/usr/bin/env python
#
#   Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import datetime

import requests


class XAuthToken(requests.auth.AuthBase):
    """This class handles authentication against the HP SDN REST API and
    uses the Requests API. XAuthToken derives from
    requests.auth.AuthBase and hpsdnclient.ApiBase."""

    def __init__(self, server, user, password):
        """Initializes the class. Set the server, user and password
        member variables. Sets the token and expiration values to
        None"""
        super(XAuthToken, self).__init__()
        self.server = server
        self.user = user
        self.password = password
        self.token = None
        self.token_expiration = None

    def __call__(self, request):
        """This method is called when an authentication token is
        required. We first check that the token exists and has not
        expired and then return the X-Auth-Token request header."""
        if (self.token is None or
                self.token_expiration <= datetime.datetime.now()):
            self.get_auth()
        request.headers['X-Auth-Token'] = self.token
        return request

    def get_auth(self):
        """This method requests an authentication token from the SDN
        controller and returns a dictionary with the token and
        expiration time."""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.server)
        payload = {'login': {'user': self.user, 'password': self.password}}
        r = requests.post(url, data=json.dumps(payload),
                          verify=False, timeout=0.5)
        r.raise_for_status()
        data = r.json()
        self.token = data[u'record'][u'token']
        timestamp = data[u'record'][u'expiration'] / 1000
        self.token_expiration = datetime.datetime.fromtimestamp(timestamp)

    def delete_auth(self):
        """Delete Authentication Token, AKA, Logout. This method logs
        the current user out"""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.server)
        headers = {"X-Auth-Token": self.token}
        r = requests.delete(url, headers=headers,
                            verify=False, timeout=0.5)
        r.raise_for_status()
        self.token = None
        self.token_expiration = None
