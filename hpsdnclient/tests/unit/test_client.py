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

import unittest

from hpsdnclient.api import Api
from hpsdnclient.auth import XAuthToken
from hpsdnclient.apibase import ApiBase
from hpsdnclient.core import CoreMixin
from hpsdnclient.net import NetMixin
from hpsdnclient.of import OfMixin


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.auth = XAuthToken(server='example.com',
                               user='sdn',
                               password='skyline'
        )

    def test_api_instantiation(self):
        api = Api('10.10.10.10', self.auth)
        self.assertTrue(isinstance(api, ApiBase))
        self.assertTrue(isinstance(api, CoreMixin))
        self.assertTrue(isinstance(api, NetMixin))
        self.assertTrue(isinstance(api, OfMixin))
        self.assertEqual(api.restclient.auth, self.auth)
        self.assertEqual(api.controller, '10.10.10.10')
