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

import argparse
import os
import hpsdnclient as hp
from hpsdnclient.error import NotFound

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str,
                        help="The file to upload",
                        required=True)
    parser.add_argument('--app', type=str,
                        help="The application name e.g com.mango.hm",
                        required=True)

    args = parser.parse_args()

    upload(args.filename, args.app)

def upload(filename, app):

    controller = os.getenv("SDNCTL")
    user = os.getenv("SDNUSER")
    password = os.getenv("SDNPASS")
    auth = hp.XAuthToken(user=user, password=password, server=controller)
    api = hp.Api(controller=controller, auth=auth)

    running = is_running(api, app)

    if running:
        api.manage_app(app, "stop")
        api.uninstall_app(app)

    api.upload_app(filename)
    api.manage_app(app, "install")
    api.manage_app(app, "start")


def is_running(api, app):
    try:
        api.get_app_info(app)
    except NotFound:
        return False
    return True

if __name__ == "__main__":
    main()
