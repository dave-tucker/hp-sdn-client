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
import time

import requests

from hpsdnclient.api import ApiBase
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
        self._get(url)

    def post_licences(self, key):
        """ Add a new license """
        url = self._core_base_url + 'licenses'
        r = self.restclient.post(url, key)
        raise_errors(r)

    def get_install_id(self):
        """ Get install id """
        url = self._core_base_url + 'licenses/installid'
        return self.restclient.get(url)

    def get_licence_detail(self, serial_no):
        """ Get a license by serial number """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        return self.restclient.get(url)

    def post_licence_action(self, serial_no, action):
        """ Perfom an action on the license """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        r = self.restclient.post(url, action)
        raise_errors(r)

    def get_configs(self):
        """ Get a list of configuration paramters """
        #Data structure is wild! Need to find a way to tame it
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
        return self.restclient.get(url)

    def deploy_app(self, app):
        """ Deploy an app """
        url = self._core_base_url + 'apps'
        r = self.restclient.post(url, app, is_file=True)
        raise_errors(r)

    def get_app_info(self, app):
        """ Get application information """
        url = self._core_base_url + 'apps/{}'.format(app)
        return self.restclient.get(url)

    def delete_app(self, app):
        """ Undeploy and application """
        url = self._core_base_url + 'apps/{}'.format(app)
        r = self.restclient.delete(url)
        raise_errors(r)

    def post_app_action(self, app, action):
        """ Perform an action on a deployed application """
        url = self._core_base_url + 'apps/{}/action'.format(app)
        r = self.restclient.post(url, action)
        raise_errors(r)

    def get_app_health(self, app):
        """ Get app health information """
        url = self._core_base_url + 'apps/{}/health'.format(app)
        return self.restclient.get(url)

    def monitor_app_health(self, app):
        """ Monitor app health """
        #ToDo: This one uses odd status codes
        pass

    def download_logs(self):
        url = self._core_base_url + 'logs'
        return self.restclient.get(url, is_file=True)

    def get_auth(self, user, password):
        """Get Authentication Token. This method returns a dictionary
        with the token and expiration time"""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        data = {'login':{ 'user': user, 'password': password}}
        r = requests.post(url, data=json.dumps(data))
        t = []
        r.raise_for_status()
        data = r.json()
        t['token'] = data[u'record'][u'token']
        exptime = data[u'record'][u'expiration']/1000
        t['token_expiration'] = time.gmtime(exptime)
        return t

    def delete_auth(self, token):
        """ Delete Authentication Token, AKA, Logout. This method logs
        out the owner of the supplied token."""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token":token}
        r = requests.delete(url, headers=headers)
        r.raise_for_status()
