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

""" Here is the implementation for the REST verbs using the Requests API """

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.2.0'

import requests

from hpsdnclient.error import FlareApiError

DATA_TYPES = set(['json', 'zip'])
SUCCESS_CODES = ( 200, 201, 204 )

def get(url, token, data_type):
    """ get()

        Implements the REST GET verb using the Requests API.

    """
    try:
        r = requests.get(url, auth=token, verify=False, timeout=0.5)
    except Exception as e:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()
    if not r.status_code in SUCCESS_CODES:
        if data_type == 'json':
            data = r.json()
            if "message" in data:
                raise FlareApiError(data["message"])
            else:
                r.raise_for_status()
    else:
        data = r.json()
        if data == [] or data == None:
            raise FlareApiError("There is nothing to see here....")
        else:
            return data


def put(url, token, data):
    """ put()

        Implements the REST PUT verb using the Requests API.

    """
    headers = {'content-type': 'application/json'}
    try:
        r = requests.put(url, auth=token, data=data,
                         headers=headers, verify=False, timeout=0.5)
    except Exception as e:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

    if not r.status_code in SUCCESS_CODES:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

def post(url, token, data):
    """ post()

        Implements the REST POST verb using the Requests API.

    """
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post(url, auth=token, data=data,
                          headers=headers, verify=False, timeout=0.5)
    except Exception as e:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

    if not r.status_code in SUCCESS_CODES:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

def delete(url, token, data=None):
    """ delete()

        Implements the REST DELETE verb using the Requests API.

    """
    headers = {'content-type': 'application/json'}

    if not data == None:
        try:
            r = requests.delete(url, auth=token, headers=headers,
                                data=data, verify=False, timeout=0.5)
        except Exception as e:
            data = r.json()
            if "message" in data:
                raise FlareApiError(data["message"])
            else:
                r.raise_for_status()
    else:
        try:
            r = requests.delete(url, auth=token, headers=headers,
                                verify=False, timeout=0.5)
        except Exception as e:
            data = r.json()
            if "message" in data:
                raise FlareApiError(data["message"])
            else:
                r.raise_for_status()
    if not r.status_code in SUCCESS_CODES:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

def head(url, token):
    """ head()

        Implements the REST HEAD verb using the Requests API.

    """
    headers = {'content-type': 'application/json'}
    try:
        r = requests.head(url, auth=token, headers=headers,
                          verify=False, timeout=0.5)
    except Exception as e:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()

    if not r.status_code in SUCCESS_CODES:
        data = r.json()
        if "message" in data:
            raise FlareApiError(data["message"])
        else:
            r.raise_for_status()
