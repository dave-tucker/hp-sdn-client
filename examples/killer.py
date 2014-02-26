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
from hpsdnclient.datatypes import Flow, Match, Action

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str,
                        help="The IP Address to kill",
                        required=True)

    args = parser.parse_args()

    kill_flow(args.ip)

def kill_flow(ip):
    controller = os.getenv("SDNCTL")
    user = os.getenv("SDNUSER")
    password = os.getenv("SDNPASS")
    auth = hp.XAuthToken(user=user, password=password, server=controller)
    api = hp.Api(controller=controller, auth=auth)

    match = Match(eth_type="ipv4", ipv4_src=ip)
    action = Action(output=0)
    flow = Flow(priority=30000, match=match, actions=action, hard_timeout=30)
    datapaths = api.get_datapaths()
    for d in datapaths:
        api.add_flows(d.dpid, flow)

if __name__ == "__main__":
    main()
