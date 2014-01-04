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

import copy

import requests

from hpsdnclient.api import __version__
from hpsdnclient.datatypes import JsonObjectFactory, JSON_MAP, PLURALS
from hpsdnclient.error import raise_errors, NotFound

UA = {
    'content-type': 'application/json',
    'user-agent': 'hpsdnclient/{0} '.format(__version__) +
                  'python-requests/{0}'.format(requests.__version__)
}


class RestClient(object):
    def __init__(self, auth):
        self.auth = auth
        self.args = {"auth": self.auth,
                     "verify": False,
                     "headers": UA,
                     "timeout": 0.5
        }

    def _append_content_type(self):
        args = copy.deepcopy(self.args)
        args["headers"]["content-type"] = 'application/zip'
        return args

    def _get(self, url, is_file=False):
        if is_file == True:
            args = self._append_content_type()
        else:
            args = self.args
        r = requests.get(url, **args)
        return r

    def _put(self, url, data):
        r = requests.put(url, data=data, **self.args)
        return r

    def _post(self, url, data, is_file=False):
        if is_file:
            args = self._append_content_type()
        else:
            args = self.args
        r = requests.post(url, data=data, **args)
        return r

    def _delete(self, url, data=None):
        if data is None:
            r = requests.delete(url, **self.args)
        else:
            r = requests.delete(url, data=data, **self.args)
        return r

    def _head(self, url):
        r = requests.head(url, **self.args)
        return r

    def get(self, url, is_file=False):
        result = []
        if is_file:
            r = self._get(url, is_file=True)
        else:
            r = self._get(url)

        raise_errors(r)

        content = r.headers['Content-Type']

        if content == 'application/json':
            data = r.json()

            for k in list(data):
                if not k == 'version':
                    key = k

            if not key in PLURALS:
                try:
                    datatype = JSON_MAP[key]
                except KeyError:
                    raise NotFound(key)
                result = JsonObjectFactory.create(datatype, data[key])
            else:
                datatype = PLURALS[key]
                for d in data[key]:
                    result.append(JsonObjectFactory.create(datatype, d))

        elif content == 'text/plain':
            result = r.text

        elif r.headers['Content-Type'] == 'application/zip':
            data = r.content
            # Strip the 'attachment; filename='' from Content-Disposition
            filename = r.headers["Content-Disposition"][21:]
            # Save the data to a file
            f = open(filename, 'wb')
            f.write(data)
            f.close()
            # Return the filename
            result = filename
        else:
            result = None
        return result

    def post(self, url, data, is_file=False):
        r = self._post(url, data, is_file)
        raise_errors(r)
        return r

    def put(self, url, data):
        r = self._put(url, data)
        raise_errors(r)
        return r

    def delete(self, url, data=None):
        r = self._delete(url, data)
        raise_errors(r)
        return r

    def head(self, url):
        r = self._head(url)
        raise_errors(r)
        return r
