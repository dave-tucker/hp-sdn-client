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
# Python3 compatibility
try:
    import urllib.parse as urllib
except ImportError:
    import urllib


def raise_errors(response):
    if response.status_code == 400:
        raise_400(response)
    elif response.status_code == 404:
        raise_404(response)
    elif response.status_code == 500:
        raise_500(response)
    else:
        # let requests raise the error
        response.raise_for_status()


def raise_400(response):
    data = response.json()

    if "Invalid JSON format" in data['message']:
        raise InvalidJson(response.request.url,
                          json.dumps(response.request.body),
                          data['message'])
    elif "IllegalArgumentException" in data['error']:
        raise IllegalArgument()
    elif "VersionMismatchException" in data['error']:
        dpid = urllib.unquote(response.request.url.split('/')[7])
        required_version = data['message'][-3:]
        raise VersionMismatch(dpid, required_version)
    else:
        response.raise_for_status()


def raise_404(response):
    data = response.json()
    if "NotFoundException" in data['error']:
        raise NotFound(data['message'])
    else:
        response.raise_for_status()


def raise_500(response):
    data = response.json()
    if "IllegalStateException" in data['error']:
        raise OpenflowProtocolError()
    else:
        response.raise_for_status()


class HpsdnclientError(Exception):
    """Base class for Flare API errors"""
    pass


class InvalidJson(HpsdnclientError):
    def __init__(self, url, request_body, message):
        self.url = url
        self.request_body = request_body
        self.message = message
        super(InvalidJson, self).__init__(message)


class VersionMismatch(HpsdnclientError):
    def __init__(self, dpid, required_version):
        self.dpid = dpid
        self.required_version = required_version
        message = ("This feature is not supported on DPID {0}. " +
                   "It requires OpenFlow version {1}").format(dpid,
                                                              required_version)
        super(VersionMismatch, self).__init__(message)


class IllegalArgument(HpsdnclientError):
    def __init__(self, arguments=None):
        super(IllegalArgument, self).__init__()
        self.arguments = arguments


class NotFound(HpsdnclientError):
    def __init__(self, message):
        super(NotFound, self).__init__(message)


class OpenflowProtocolError(HpsdnclientError):
    def __init__(self):
        message = ("Something bad happened at the OpenFlow protocol layer." +
                   " This could be because this feature is not implemented " +
                   "on this device")
        super(OpenflowProtocolError, self).__init__(message)


class DatatypeError(HpsdnclientError):
    def __init__(self, received, expected):
        self.received = received
        self.expected = expected
        message = "Received: {0} Expected: {1}".format(received, expected)
        super(DatatypeError, self).__init__(message)
