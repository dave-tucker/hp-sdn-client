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
__version__ = '0.1.0'

class FlareApiError(Exception):
  """Base class for Flare API errors"""
  pass

class HttpError(FlareApiError):
    def __init__(self, res_code):
        self.res_code = res_code
        if res_code == 401:
            msg = "You aren't authentcated. Check the username & password you supplied"
        elif res_code == 403:
            msg = "You don't have permission to use the resource you requested"
        elif res_code == 404:
            msg = "Looks like the Api isn't responding. Check access to the SDN Controller"
        elif res_code == 409:
            msg = """Holy Grail you say? We've already got one!
                     On a more serious note we already have one of these objects you requested"""
        else:
            msg = "You were in great peril back there! HTTP threw a {}".format(res_code)
