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

""" This fle implements the Flare Core REST API """

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.2.0'

import json
import time

import requests

from hpsdnclient.api import ApiBase
import hpsdnclient.rest as rest
import hpsdnclient.datatypes as datatypes
from hpsdnclient.error import raise_errors

class CoreMixin(ApiBase):
    """ Flare REST API Core Methods. i.e, those in sdn/v2.0/ """

    def __init__(self, controller, auth):
        super(CoreMixin, self).__init__(controller, auth)
        self._core_base_url = ("https://{0}:8443".format(self.controller) +
                             "/sdn/v2.0/")

    def get_support(self, artifact=None, fields=None):
        """ Get a full support report """
        url = self._core_base_url + 'support'
        if artifact:
            url += '?id={}'.format(artifact)
        if fields:
            url += '?fields={}'.format(fields)
        self._get(url)

    def get_licenses(self, key=None):
        """ List all licenses """
        url = self._core_base_url + 'licenses'
        if key:
            url += '?key={}'.format(key)
        self._get(url, 'licenses')

    def post_licences(self, key):
        """ Add a new license """
        url = self._core_base_url + 'licenses'
        r = rest.post(url, self.auth, key)
        raise_errors(r)

    def get_install_id(self):
        """ Get install id """
        url = self._core_base_url + 'licenses'
        r = rest.get(url, self.auth)
        raise_errors(r)
        return r.text()

    def get_licence_detail(self, serial_no):
        """ Get a license by serial number """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        return self._get(url, 'license', False)

    def post_licence_action(self, serial_no, action):
        """ Perfom an action on the license """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        r = rest.post(url, self.auth, action)
        raise_errors(r)

    def get_configs(self):
        """ Get a list of configuration paramters """
        #Data strcuture is wild! Need to find a way to tame it
        pass

    def get_config_component(self, component):
        #As above
        pass

    def update_config_component(self, component):
        pass

    def delete_config_component(self, component):
        """ Revert a configuration to default """
        pass

    def get_apps(self):
        """ Get a list of applications """
        url = self._core_base_url + 'apps'
        return self._get(url, 'apps')

    def deploy_app(self, app):
        """ Deploy an app """
        url = self._core_base_url + 'apps'
        r = rest.post(url, self.auth, app, is_file=True)
        raise_errors(r)
        data = r.json()
        return datatypes.JsonObject.factory(data["app"])

    def get_app_info(self, app):
        """ Get application information """
        url = self._core_base_url + 'apps/{}'.format(app)
        return self._get(url, 'app')

    def delete_app(self, app):
        """ Undeploy and application """
        url = self._core_base_url + 'apps/{}'.format(app)
        r = rest.delete(url, self.auth)
        raise_errors(r)

    def post_app_action(self, app, action):
        """ Perform an action on a deployed application """
        url = self._core_base_url + 'apps/{}/action'.format(app)
        r = rest.post(url, self.auth, action)
        raise_errors(r)

    def get_app_health(self, app):
        """ Get app health information """
        url = self._core_base_url + 'apps/{}/health'.format(app)
        return self._get(url, 'app')

    def monitor_app_health(self, app):
        """ Monitor app health """
        #ToDo: This one uses odd status codes
        pass

    def download_logs(self):
        url = self._core_base_url + 'logs'
        return self._get(url, is_file=True)

    def get_auth(self, user, password):
        """Get Authentication Token. This method returns a dictionary
        with the token and expiration time"""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        data = {'login':{ 'user': user, 'password': password}}
        r = requests.post(url, data=json.dumps(data))
        t = []
        if r.status_code == 200:
            data = r.json()
            t['token'] = data[u'record'][u'token']
            exptime = data[u'record'][u'expiration']/1000
            t['token_expiration'] = time.gmtime(exptime)
            return t
        else:
            r.raise_for_status()

    def delete_auth(self, token):
        """ Delete Authentication Token, AKA, Logout. This method logs
        out the owner of the supplied token."""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token":token}
        r = requests.delete(url, headers=headers)
        if not r.status_code == 200:
            r.raise_for_status()

