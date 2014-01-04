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

import json
import os
import re
import unittest
#PY3.3
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import httpretty
import requests

from hpsdnclient.auth import XAuthToken
from hpsdnclient.datatypes import Datapath
from hpsdnclient.error import NotFound
from hpsdnclient.rest import RestClient, UA
from hpsdnclient.tests.data import AUTH, DATAPATH


class RestClientTests(unittest.TestCase):
    def setUp(self):
        self.auth = XAuthToken('10.10.10.10', 'sdn', 'skyline')
        self.client = RestClient(self.auth)
        response_ok = requests.Response()
        response_ok.status_code = 200
        self.response_ok = response_ok

    def test_restclient_instantiation(self):
        self.assertEqual(self.client.args["auth"], self.auth)
        self.assertEqual(self.client.args["headers"], UA)
        self.assertEqual(self.client.args["verify"], False)
        self.assertEqual(self.client.args['timeout'], 0.5)

    def test_user_agent_string(self):
        #assert that the UA matches the following regexp
        #
        exp = ("^(hpsdnclient/[0-9]\\.[0-9]\\.[0-9] " +
               "python-requests/[0-9]\\.[0-9]\\.[0-9])$")
        self.assertTrue(re.search(exp, UA['user-agent'], re.S))

    def test__append_content_type(self):
        args = self.client._append_content_type()
        self.assertEqual(args['headers']['content-type'], 'application/zip')
        self.assertEqual(self.client.args['headers']['content-type'],
                         'application/json')

    @httpretty.activate
    def test__get_json(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.GET,
                               'http://foo.bar',
                               status=200)

        response = self.client._get('http://foo.bar', False)

        self.assertEqual(response.request.headers['content-type'],
                         'application/json')

    @httpretty.activate
    def test__get_file(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.GET,
                               'http://foo.bar',
                               status=200)

        response = self.client._get('http://foo.bar', True)

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.headers['content-type'],
                         'application/zip')

    @httpretty.activate
    def test__put(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.PUT,
                               'http://foo.bar',
                               status=201)

        response = self.client._put('http://foo.bar',
                                    json.dumps({"some": "data"}))

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/json')
        self.assertEqual(response.request.body,
                         json.dumps({"some": "data"}))

    @httpretty.activate
    def test__post_json(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.POST,
                               'http://foo.bar',
                               status=201)

        response = self.client._post('http://foo.bar',
                                     json.dumps({"some": "data"}),
                                     False)

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/json')
        self.assertEqual(response.request.body,
                         json.dumps({"some": "data"}))

    @httpretty.activate
    def test__post_file(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.POST,
                               'http://foo.bar',
                               status=201)

        response = self.client._post('http://foo.bar',
                                     json.dumps({"some": "data"}),
                                     True)

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/zip')
        self.assertEqual(response.request.body,
                         json.dumps({"some": "data"}))

    @httpretty.activate
    def test__delete_no_data(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.DELETE,
                               'http://foo.bar',
                               status=201)

        response = self.client._delete('http://foo.bar')

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/json')

    @httpretty.activate
    def test__delete_with_data(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.DELETE,
                               'http://foo.bar',
                               status=201)

        response = self.client._delete('http://foo.bar',
                                       json.dumps({"some": "data"}))

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/json')
        self.assertEqual(response.request.body,
                         json.dumps({"some": "data"}))

    @httpretty.activate
    def test__head(self):
        httpretty.register_uri(httpretty.POST,
                               'https://10.10.10.10:8443/sdn/v2.0/auth',
                               body=AUTH,
                               status=201)
        httpretty.register_uri(httpretty.HEAD,
                               'http://foo.bar',
                               status=201)

        response = self.client._head('http://foo.bar')

        self.assertTrue(isinstance(response, requests.Response))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.headers['content-type'],
                         'application/json')

    def test_get_json_valid_datatype(self):
        data = json.dumps({"version": "1.0.0", "datapath": DATAPATH})
        response = requests.Response()
        response._content = data
        response.status_code = 201
        response.headers['content-type'] = 'application/json'
        self.client._get = MagicMock(name="_get", return_value=response)

        r = self.client.get('http://foo.bar')

        self.client._get.assert_called_with('http://foo.bar')
        self.assertTrue(isinstance(r, Datapath))

    def test_get_json_valid_datatypes(self):
        data = json.dumps({"version": "1.0.0",
                           "datapaths": [DATAPATH, DATAPATH]})
        response = requests.Response()
        response._content = data
        response.status_code = 201
        response.headers['content-type'] = 'application/json'
        self.client._get = MagicMock(name="_get", return_value=response)

        r = self.client.get('http://foo.bar')

        self.client._get.assert_called_with('http://foo.bar')
        self.assertTrue(isinstance(r, list))
        for item in r:
            self.assertTrue(isinstance(item, Datapath))

    def test_get_json_invalid_datatype(self):
        data = json.dumps({"version": "1.0.0", "datapathz": DATAPATH})
        response = requests.Response()
        response._content = data
        response.status_code = 201
        response.headers['content-type'] = 'application/json'
        self.client._get = MagicMock(name="_get", return_value=response)

        self.assertRaises(NotFound, self.client.get, 'http://foo.bar')

    def test_get_file(self):
        data = "Hello World!"
        response = requests.Response()
        response._content = data
        response.status_code = 201
        response.headers['content-type'] = 'application/zip'
        response.headers['content-disposition'] = 'attachment; filename=h.txt'
        self.client._get = MagicMock(name="_get", return_value=response)

        r = self.client.get('http://foo.bar', is_file=True)

        self.client._get.assert_called_with('http://foo.bar', is_file=True)
        self.assertEqual(r, 'h.txt')
        f = open('h.txt', 'rb')
        self.assertEqual(f.read(), "Hello World!")
        f.close()
        os.remove('h.txt')

    def test_get_none(self):
        response = requests.Response()
        response.status_code = 201
        response.headers['Content-Type'] = 'application/none'
        self.client._get = MagicMock(name="_get", return_value=response)

        r = self.client.get('http://foo.bar')

        self.client._get.assert_called_with('http://foo.bar')
        self.assertTrue(r is None)

    def test_post(self):
        self.client._post = MagicMock(name="_post",
                                      return_value=self.response_ok)

        r = self.client.post('http://foo.bar', json.dumps({"some": "data"}))

        self.client._post.assert_called_with('http://foo.bar',
                                             json.dumps({"some": "data"}),
                                             False)

        self.assertTrue(isinstance(r, requests.Response))

    def test_put(self):
        self.client._put = MagicMock(name="_put",
                                     return_value=self.response_ok)

        r = self.client.put('http://foo.bar', json.dumps({"some": "data"}))

        self.client._put.assert_called_with('http://foo.bar',
                                            json.dumps({"some": "data"}))

        self.assertTrue(isinstance(r, requests.Response))

    def test_delete_data(self):
        self.client._delete = MagicMock(name="_delete",
                                        return_value=self.response_ok)

        r = self.client.delete('http://foo.bar', json.dumps({"some": "data"}))

        self.client._delete.assert_called_with('http://foo.bar',
                                               json.dumps({"some": "data"}))

        self.assertTrue(isinstance(r, requests.Response))


    def test_delete_no_data(self):
        self.client._delete = MagicMock(name="_delete",
                                        return_value=self.response_ok)

        r = self.client.delete('http://foo.bar')

        self.client._delete.assert_called_with('http://foo.bar', None)

        self.assertTrue(isinstance(r, requests.Response))

    def test_head(self):
        self.client._head = MagicMock(name="_head",
                                      return_value=self.response_ok)
        #self.raise_errors = MagicMock(name="raise_errors")

        r = self.client.head('http://foo.bar')

        self.client._head.assert_called_with('http://foo.bar')

        self.assertTrue(isinstance(r, requests.Response))
