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

import datetime
import unittest
#Python 3.3 compatability
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import httpretty
import requests

import hpsdnclient.auth as auth
from hpsdnclient.tests.data import AUTH


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.server = '10.10.10.10'
        self.user = 'sdn'
        self.password = 'skyline'
        self.xauthtoken = auth.XAuthToken(self.server,
                                          self.user,
                                          self.password)

    def test_instantiate_xauthtoken(self):
        self.assertEqual(self.xauthtoken.server, self.server)
        self.assertEqual(self.xauthtoken.user, self.user)
        self.assertEqual(self.xauthtoken.password, self.password)
        self.assertEqual(self.xauthtoken.token, None)
        self.assertEqual(self.xauthtoken.token_expiration, None)

    def test_call_no_token(self):
        self.xauthtoken.get_auth = MagicMock(name='get_auth')

        request = requests.Request()
        self.xauthtoken.__call__(request)

        self.xauthtoken.get_auth.assert_called_with()

    def test_call_with_valid_token(self):
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        self.xauthtoken.token = 'test_token'
        self.xauthtoken.token_expiration = expiry

        request = requests.Request()
        self.xauthtoken.__call__(request)

        self.assertEqual(request.headers['X-Auth-Token'], 'test_token')

    def test_call_with_expired_token(self):
        self.xauthtoken.get_auth = MagicMock(name='get_auth')
        expiry = datetime.datetime.now() - datetime.timedelta(days=1)
        self.xauthtoken.token = 'test_token'
        self.xauthtoken.token_expiration = expiry
        self.xauthtoken.get_auth = MagicMock(name='get_auth')

        request = requests.Request()
        self.xauthtoken.__call__(request)

        self.xauthtoken.get_auth.assert_called_with()

    @httpretty.activate
    def test_get_auth(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)

        timestamp = 1385824487000 / 1000
        expiry_time = datetime.datetime.fromtimestamp(timestamp)

        self.xauthtoken.get_auth()

        self.assertEqual(self.xauthtoken.token,
                         '6dea10bebf074ec3bc2b641535e04f04')
        self.assertEqual(self.xauthtoken.token_expiration,
                         expiry_time)

    @httpretty.activate
    def test_delete_auth(self):
        httpretty.register_uri(httpretty.DELETE,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               status=201)

        self.xauthtoken.delete_auth()

        self.assertEqual(self.xauthtoken.token, None)
        self.assertEqual(self.xauthtoken.token_expiration, None)

