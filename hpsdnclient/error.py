#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
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

""" Error handling for the HP SDN Client """

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.2.0'

import json
import urllib

def raise_errors(response):
    if response.status_code == 400:
        raise_400(response)
    elif response.status_code == 404:
        raise_404(response)
    elif response.status_code == 500:
        raise_500(response)
    else:
        #let requests raise the error
        response.raise_for_status()

def raise_400(response):
    data = response.json()

    if "Invalid JSON format" in data['message']:
        raise InvalidJson(response.request.url,
                          json.dumps(response.request.body),
                          data['message'])
    elif "IllegalArgumentException" in data['error']:
        arguments = []
        for x in response.url.split('/')[6:]:
            arguments.append(urllib.unquote(x))
        raise IllegalArgument(arguments)
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
        raise IllegalState(data["message"])
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
        message = """This feature is not supported on DPID {0}.
                     It requires OpenFlow version {1}
                  """.format(dpid, required_version)
        super(VersionMismatch, self).__init__(message)

class IllegalArgument(HpsdnclientError):
    def __init__(self, arguments):
        super(IllegalArgument, self).__init__()
        self.arguments = arguments

class NotFound(HpsdnclientError):
    pass

class IllegalState(HpsdnclientError):
    pass

class DatatypeError(HpsdnclientError):
    def __init__(self, received, expected):
        self.received = received
        self.expected = expected
        message = "Expected: {0} Received: {1}".format(expected, received)
        super(DatatypeError, self).__init__(message)

