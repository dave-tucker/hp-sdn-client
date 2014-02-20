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

import os
import requests
from hpsdnclient.tests.base import ApiTestCase
from hpsdnclient.error import NotFound

class TestCoreMixin(ApiTestCase):

    def test_get_support(self):
        support = self.api.get_support()
        self.assertTrue(support)

        support = self.api.get_support(id="alert")
        self.assertTrue(support)

        support = self.api.get_support(fields="content")
        self.assertTrue(support)

        support = self.api.get_support(id="alert", fields="content")
        self.assertTrue(support)

    def test_add_license_get_details_and_deactivate(self):
        #ToDo: Get a test license that works wth the SDN Controller
        pass

    def test_get_install_id(self):
        install_id = self.api.get_install_id()
        self.assertTrue(install_id)

    def test_get_apps(self):
        apps = self.api.get_apps()
        self.assertTrue(apps)

    def test_get_app_info(self):
        app_info = self.api.get_app_info("com.hp.sdn.ctl.path")
        self.assertTrue(app_info)

    def test_upload_start_and_uninstall_app(self):

        r = requests.get("https://dl.dropboxusercontent.com/u/2418976/hm-1.0.0-SNAPSHOT.zip", stream=True)
        with open("hm-1.0.0-SNAPSHOT.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

        self.api.upload_app("hm-1.0.0-SNAPSHOT.zip")
        app = self.api.get_app_info("com.mango.hm")
        self.assertEquals("STAGED", app.state)

        self.api.manage_app("com.mango.hm", "install")
        app = self.api.get_app_info("com.mango.hm")
        self.assertEquals("ACTIVE", app.state)

        self.api.manage_app("com.mango.hm", "stop")
        app = self.api.get_app_info("com.mango.hm")
        self.assertEquals("RESOLVED", app.state)

        self.api.uninstall_app("com.mango.hm")
        self.assertRaises(NotFound, self.api.get_app_info, "com.mango.hm")

        os.remove("hm-1.0.0-SNAPSHOT.zip")

    def test_get_app_health(self):
        app_health = self.api.get_app_health("com.hp.sdn.ctl.path")
        self.assertTrue(app_health)

    def test_download_logs(self):
        logs = self.api.download_logs()
        self.assertTrue(os.path.isfile(logs))
        os.remove(logs)

    def test_login(self):
        login = self.api.login("sdn", "skyline")

        url = "https://{}:8443/sdn/v2.0/datapaths".format(os.getenv("SDNCTL"))
        headers = {"X-Auth-Token": login["token"]}
        r = requests.get(url, headers=headers, verify=False)
        self.assertTrue(200, r.status_code)

    def test_logout(self):

        login = self.api.login("sdn", "skyline")
        self.api.logout(login["token"])
        url = "https://{}:8443/sdn/v2.0/datapaths".format(os.getenv("SDNCTL"))
        headers = {"X-Auth-Token": login["token"]}
        r = requests.get(url, headers=headers, verify=False)
        self.assertTrue(401, r.status_code)
