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

import json
import time

import requests

from hpsdnclient.api import ApiBase
from hpsdnclient.error import raise_errors


class CoreMixin(ApiBase):
    """Core REST API Methods

    This class contains methods that call the Core REST API functions in
    the HP VAN SDN Controller

    - Application management
    - Authentication
    - Controller management
        - Logs
        - Support Reports
    - Licensing

    """
    def __init__(self, controller, auth):
        super(CoreMixin, self).__init__(controller, auth)
        self._core_base_url = ("https://{0}:8443".format(self.controller) +
                               "/sdn/v2.0/")

    def get_support(self, id=None, fields=None):
        """ Generates a support report

       :param str id: A comma seperated list of id's to be returned (Optional)
       :param str fields: The fields to be returned (Optional)
       :return: The support report
       :rtype: hpsdnclient.datatypes.Support

        """
        url = self._core_base_url + 'support'
        if id and fields:
            url += '?id={}&fields={}'.format(id, fields)
        elif id:
            url += '?id={}'.format(id)
        elif fields:
            url += '?fields={}'.format(fields)
        return self.restclient.get(url)

    def get_licenses(self, key=None):
        """ Get all known licenses or find a specific license by key

       :param str key: A specific license key to find (Optional)
       :return: A list of licenses
       :rtype: list

        """
        url = self._core_base_url + 'licenses'
        if key:
            url += '?key={}'.format(key)
        self.restclient.get(url)

    def add_license(self, key):
        """ Add a new license

       :param str key: The license key to add

        """
        url = self._core_base_url + 'licenses'
        r = self.restclient.post(url, key)
        raise_errors(r)

    def get_install_id(self):
        """ Get install id

        :return: Install ID
        :rtype: str

        """
        url = self._core_base_url + 'licenses/installid'
        return self.restclient.get(url)

    def get_licence_detail(self, serial_no):
        """ Get a license details given its serial number

        :param str serial_no: The serial number to retrieve details for
        :return: License details
        :rtype: hpsdnclient.datatypes.License

        """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        return self.restclient.get(url)

    def deactivate_license(self, serial_no):
        """ Deactivate a license

        :param str serial_no: The serial number of the license to deactivate

        """
        action = json.dumps({"action": "deactivate"})
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        r = self.restclient.post(url, action)
        raise_errors(r)

    # Config data structure is wild! Need to find a way to tame it
    #
    # def get_configs(self):
    #    """ Get a list of configuration paramters """
    #    pass
    #
    # def get_config_component(self, component):
    #    #As above
    #    pass
    #
    # def update_config_component(self, component):
    #    pass
    #
    # def delete_config_component(self, component):
    #    """ Revert a configuration to default """
    #    pass

    def get_apps(self):
        """ Get a list of applications uploaded to the controller

        :return: List of applications
        :rtype: list

        """
        url = self._core_base_url + 'apps'
        return self.restclient.get(url)

    def upload_app(self, app):
        """ Upload an application to the controller

        :param filename app: The path to the file to be uploaded

        """
        url = self._core_base_url + 'apps'
        r = self.restclient.post(url, app, is_file=True)
        raise_errors(r)

    def get_app_info(self, app):
        """ Get information about the specified application

        :param str app: The application to query for information
        :return: Application info
        :rtype: hpsdnclient.datatypes.App

        """
        url = self._core_base_url + 'apps/{}'.format(app)
        return self.restclient.get(url)

    def uninstall_app(self, app):
        """ Uninstall and delete an application from the controller

        :param str app: The application to be uninstalled

        """
        url = self._core_base_url + 'apps/{}'.format(app)
        r = self.restclient.delete(url)
        raise_errors(r)

    def manage_app(self, app, action):
        """ Install, Start or Stop an application on the controller

        :param str app: The application to manage
        :param str action: The action to perform ("start", "stop" or "install")

        """
        url = self._core_base_url + 'apps/{}/action'.format(app)
        r = self.restclient.post(url, action)
        raise_errors(r)

    def get_app_health(self, app):
        """ Get application health information as returned by the application

        :param str app: The application to query
        :return: Application health information
        :rtype: hpsdnclient.datatypes.AppHealth

        """
        url = self._core_base_url + 'apps/{}/health'.format(app)
        return self.restclient.get(url)

    def download_logs(self):
        """ Downloads log files for the controller team.
        The logs are a zip file containing an inner zip file of logs for each
        team member.This is saved to the path where the application is being
        run.

        :return: File path
        :rtype: String

        """
        url = self._core_base_url + 'logs'
        return self.restclient.get(url, is_file=True)

    def login(self, user, password):
        """ Login to the controller.
        While not necessary (as the hp-sdn-client handles this for you)
        it's included here for completeness

        :param str user: Username
        :param str password: Password
        :return: Dictionary containing Token and Expiry Time
        :rtype: dict

        """
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        data = {'login': {'user': user, 'password': password}}
        r = requests.post(url, data=json.dumps(data), verify=False, timeout=1)
        t = {}
        r.raise_for_status()
        data = r.json()
        t['token'] = data[u'record'][u'token']
        exptime = data[u'record'][u'expiration']/1000
        t['token_expiration'] = time.gmtime(exptime)
        return t

    def logout(self, token):
        """ Logout of the controller
        Logs out the user with the supplied token

        :param str token: X-Auth-Token of the user to logout

        """
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token": token}
        r = requests.delete(url, headers=headers, verify=False, timeout=1)
        r.raise_for_status()
