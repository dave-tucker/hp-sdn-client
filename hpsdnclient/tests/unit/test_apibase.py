#!/usr/bin/env python
#
#   Copyright 2013 Hewlett-Packard Development Company, L.P.
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

import unittest

from hpsdnclient.apibase import ApiBase
from hpsdnclient.rest import RestClient
from hpsdnclient.auth import XAuthToken


class ApiBaseTest(unittest.TestCase):
    def test_apibase_instantiation(self):
        controller = '10.10.10.10'
        token = XAuthToken('10.10.10.10', 'sdn', 'skyline')
        rest_client = RestClient(token)
        apibase = ApiBase(controller, rest_client)
        self.assertEqual(apibase.controller, controller)
        self.assertEqual(apibase.rest_client, rest_client)
