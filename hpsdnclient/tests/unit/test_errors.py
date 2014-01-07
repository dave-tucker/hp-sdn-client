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
#PY3.3
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import httpretty
import requests

import hpsdnclient.error as error
import hpsdnclient.tests.data as test_data


# Create a test harness for the reponse object
# To test raise_400, raise_404, raise_500
#   create a dict with the sample messages
#   for each message in dict, check correct error is raised
#   for unknown error, check a Requests style exception is raised

# To test raise_errors
# Check that the correct function is called for each status_code


def test_raise_error_400():
    error.raise_400 = MagicMock(name='raise_400')
    response = requests.Response()
    response.status_code = 400
    error.raise_errors(response)

    error.raise_400.assert_called_with(response)


def test_raise_error_404():
    error.raise_404 = MagicMock(name='raise_404')
    response = requests.Response()
    response.status_code = 404
    error.raise_errors(response)

    error.raise_404.assert_called_with(response)


def test_raise_error_500():
    error.raise_500 = MagicMock(name='raise_500')
    response = requests.Response()
    response.status_code = 500
    error.raise_errors(response)

    error.raise_500.assert_called_with(response)


def test_raise_error_unknown():
    response = requests.Response()
    response.status_code = 999
    response.raise_for_status = MagicMock(name='raise_for_status')
    error.raise_errors(response)

    response.raise_for_status.assert_called_with()

### Need sample error messages

class Raise400Tests(unittest.TestCase):
    @httpretty.activate
    def test_raises_invalid_json(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body=test_data.INVALID_JSON,
                               status=400)
        response = requests.post('http://foo.bar',
                                 data={"invalid": "json"})

        self.assertRaises(error.InvalidJson, error.raise_400, response)

    @httpretty.activate
    def test_raises_illegal_argument(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body=test_data.ILLEGAL_ARG,
                               status=400)
        response = requests.post('http://foo.bar',
                                 data={"illegal": "arg"})

        self.assertRaises(error.IllegalArgument, error.raise_400, response)

    @httpretty.activate
    def test_raises_version_mismatch(self):
        url = "https://foo.bar:8443/sdn/v2.0/of/datapaths/0x1/groups"
        httpretty.register_uri(httpretty.POST,
                               url,
                               body=test_data.VERSION_MISMATCH,
                               status=400)
        response = requests.post(url,
                                 data={"version": "mismatch"})

        with self.assertRaises(error.VersionMismatch):
            try:
                error.raise_400(response)
            except error.VersionMismatch as e:
                self.assertEqual(e.dpid, '0x1')
                self.assertEqual(e.required_version, '1.3')
                raise

    @httpretty.activate
    def test_raises_for_status(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body='{"error":"unkown", "message":"unknown"}',
                               status=400)
        response = requests.post('http://foo.bar',
                                 data={"unknown": "error"})

        response.raise_for_status = MagicMock(name='raise_for_status')

        error.raise_400(response)
        response.raise_for_status.assert_called_with()


class Raise404Tests(unittest.TestCase):
    @httpretty.activate
    def test_raises_not_found(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body=test_data.NOTFOUND,
                               status=404)
        response = requests.post('http://foo.bar',
                                 data={"not": "found"})

        self.assertRaises(error.NotFound, error.raise_404, response)

    @httpretty.activate
    def test_raises_for_status(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body='{"error":"unkown", "message":"unknown"}',
                               status=404)
        response = requests.post('http://foo.bar',
                                 data={"unknown": "error"})

        response.raise_for_status = MagicMock(name='raise_for_status')

        error.raise_404(response)
        response.raise_for_status.assert_called_with()


class Raise500Tests(unittest.TestCase):
    @httpretty.activate
    def test_raises_openflow_protocol_error(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body=test_data.ILLEGAL_STATE,
                               status=500)
        response = requests.post('http://foo.bar',
                                 data={"illegal": "operation"})

        self.assertRaises(error.OpenflowProtocolError,
                          error.raise_500, response)

    @httpretty.activate
    def test_raises_for_status(self):
        httpretty.register_uri(httpretty.POST, "http://foo.bar/",
                               body='{"error":"unkown", "message":"unknown"}',
                               status=500)
        response = requests.post('http://foo.bar',
                                 data={"unknown": "error"})

        response.raise_for_status = MagicMock(name='raise_for_status')

        error.raise_500(response)
        response.raise_for_status.assert_called_with()


class ErrorTypeTests(unittest.TestCase):
    def test_invalid_json(self):
        url = 'http://dummy.url'
        json_string = '{"a":"b", "c":{"d":"e", "f":"g"}, "h":[1,2,3]}'
        message = 'The json is invalid'
        try:
            raise error.InvalidJson(url, json_string, message)
        except error.InvalidJson as e:
            self.assertEquals(e.args[0], message)
            self.assertEquals(e.request_body, json_string)
            self.assertEquals(e.url, url)

    def test_version_mismatch(self):
        dpid = '00:00:00:00:00:00:00:01'
        required_version = '1.3'
        expected_message = ("This feature is not supported on DPID " +
                            "00:00:00:00:00:00:00:01. It requires OpenFlow " +
                            "version 1.3")
        try:
            raise error.VersionMismatch(dpid, required_version)
        except error.VersionMismatch as e:
            self.assertEquals(e.args[0], expected_message)

    def test_illegal_argument(self):
        try:
            raise error.IllegalArgument("test")
        except error.IllegalArgument as e:
            self.assertEquals(e.arguments, "test")

    def test_not_found(self):
        message = "test"
        expected_message = "test"
        try:
            raise error.NotFound(message)
        except error.NotFound as e:
            self.assertEquals(e.args[0], expected_message)

    def test_openflow_protocol_error(self):
        expected_message = ("Something bad happened at the OpenFlow protocol" +
                            " layer. This could be because this feature is " +
                            "not implemented on this device")
        try:
            raise error.OpenflowProtocolError()
        except error.OpenflowProtocolError as e:
            self.assertEquals(e.args[0], expected_message)

    def test_datatype_eror(self):
        expected_message = "Received: Dogs Expected: Cats"
        try:
            raise error.DatatypeError('Dogs', 'Cats')
        except error.DatatypeError as e:
            self.assertEquals(e.args[0], expected_message)
