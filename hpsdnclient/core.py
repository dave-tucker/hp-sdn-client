#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software  and associated documentation files (the "Software"), to deal
# in the Software without restriction,  including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or  substantial portions of the Software.#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED,  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR  PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF  OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#

""" This fle implements the Flare Core REST API
/support GET
/licenses GET
/licenses POST
/licenses/installid GET
/licenses/{sno} GET
/licenses/{sno}/action POST
/configs GET
/configs/{component} GET
/configs/{component} PUT
/configs/{component} DELETE
/apps GET
/apps POST
/apps/{app_uid} DELETE
/apps/{app_uid} PUT
/apps/{app_uid} GET
/apps/{app_uid}/action POST
/apps/{app_uid}/health GET
/apps/{app_uid}/health HEAD
/logs GET
/logs/local GET
/auditlog GET
/systems GET
/systems/{system_uid} GET
/systems/{system_uid}/action POST
/systems/{system_uid}/backup GET
/systems/{system_uid}/backup POST
/regions GET
/regions POST
/regions/{region_uid} GET
/regions/{region_uid} PUT
/regions/{region_uid} DELETE
/team GET
/team POST
/teamD ELETE
/team/action POST
/backups GET
/backups/{session_uid} GET
/restores GET
/restores/{session_uid} GET
/alerts GET
/alerts/topics GET
/alerts/listeners GET
/alerts/listeners POST
/alerts/listeners/{listener_uid} GET
/alerts/listeners/{listener_uid} DELETE
/alerts/listeners/{listener_uid} PUT
/metrics/primaries GET
/metrics/secondaries GET
/metrics GET
/metrics/{metric_uid} GET
/metrics/{metric_uid}/values GET
"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.1.0'

import time
import urllib

import requests

from error import FlareApiError
        
class Core(object):
    """ Flare REST API Core Methods. i.e, those in sdn/v2.0/ """
    	
    def __init__(self):
		pass

    def get_support(self):
        """ get_support ()

            Get tech support information

        """

        pass

    def get_licenses(self):
        """ get_licenses ()

            Get license information

        """

        pass

    def post_licences(self):
        """ post_licences(self)

            Add licenses

        """

        pass

    def get_licences_install_id(self):
        """ get_licences_install_id(self)

            Add licenses

        """

        pass

    def get_licence_detail(self):
        """ get_license_detail (self)

            Get license detail

        """

        pass


    def post_licence_action(self):
        """ post_licence_action (self)

            Perform an action on a license

        """

        pass

    def get_auth(self):
        """ get_auth ()

            Get Authentication Token 

            This method returns a dictionary with the token and expiration time. 

        """
        #ToDo: Rework to return just a token
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        payload = {'login':{ 'user': self.user, 'password': self.password}}
        r = requests.post(url, data=json.dumps(payload))
        t = []
        if r.status_code == requests.codes.ok:
            data = r.json()
            t['token'] = data[u'record'][u'token']
            t['token_expiration'] = time.gmtime(data[u'record'][u'expiration']/1000)
            return t
        else:
            raise FlareApiError("Oh no! Something went wrong")
            r.raise_for_status()

    def delete_auth(self):
        #ToDo: Rework 
        """ delete_auth ()

            Delete Authentication Token, AKA, Logout

            This method logs the current user out 

        """
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token":self.token}
        r = requests.delete(url, headers=headers)
        if r.status_code == requests.codes.ok:
            return
        else:
            raise FlareApiError("Oh no! Something went wrong")
            r.raise_for_status()

