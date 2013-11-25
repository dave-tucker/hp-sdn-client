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

""" These are wrapper functions around the pyhton-requests HTTP verbs """

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.2.0'

import requests

DEFAULT = {
            'content-type': 'application/json',
            'user-agent': 'hpsdnclient/{0} '.format(__version__) +
                          'python-requests/{0}'.format(requests.__version__)
            }

UA = {
       'user-agent': 'hpsdnclient/{0} '.format(__version__) +
                     'python-requests/{0}'.format(requests.__version__)
     }

def get(url, token, is_file=None):
    """ get()

        Implements the HTTP GET verb using the Requests API.

    """
    if is_file:
        r = requests.get(url, auth=token, verify=False,
                         headers=DEFAULT, timeout=0.5, stream=True)
    else:
        r = requests.get(url, auth=token, verify=False,
                         headers=DEFAULT, timeout=0.5)
    return r

def put(url, token, data):
    """ put()

        Implements the REST PUT verb using the Requests API.

    """
    r = requests.put(url, auth=token, data=data,
                     headers=DEFAULT, verify=False, timeout=0.5)
    return r

def post(url, token, data, is_file=False):
    """ post()

        Implements the REST POST verb using the Requests API.

    """
    if is_file:
        r = requests.post(url, auth=token, files=data,
                          headers=UA, verify=False, timeout=0.5)
    else:
        r = requests.post(url, auth=token, data=data,
                          headers=DEFAULT, verify=False, timeout=0.5)
    return r

def delete(url, token, data=None):
    """ delete()

        Implements the REST DELETE verb using the Requests API.

    """

    if not data == None:
        r = requests.delete(url, auth=token, headers=DEFAULT,
                            data=data, verify=False, timeout=0.5)
    else:
        r = requests.delete(url, auth=token, headers=DEFAULT,
                            verify=False, timeout=0.5)
    return r

def head(url, token):
    """ head()

        Implements the REST HEAD verb using the Requests API.

    """

    r = requests.head(url, auth=token, headers=DEFAULT,
                          verify=False, timeout=0.5)
    return r
