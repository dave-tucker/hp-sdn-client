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

import hpsdnclient as hp

""" Short Detour 2.0 """

#initialize the api
controller = '10.44.254.129'
auth = hp.XAuthToken(user='sdn',password='skyline', server=controller)
api = hp.Api(controller=controller, auth=auth)

#create the match object
match = hp.datatypes.Match(eth_type="ipv4",ipv4_src="10.0.0.1",
                       ipv4_dst="10.0.0.22",ip_proto="tcp",
                       tcp_dst="80")

#create the action objects
output1 = hp.datatypes.Action(output=1)
output6 = hp.datatypes.Action(output=6)

#create the flows
flow1 = hp.datatypes.Flow(priority=30000, idle_timeout=30,
                          match=match, action=output6)
flow2 = hp.datatypes.Flow(priority=30000, idle_timeout=30,
                          match=match, action=output1)

#push the flows to the datatpaths
api.add_flows('00:00:00:00:00:00:00:0e', flow1)
api.add_flows('00:00:00:00:00:00:00:01', flow1)
api.add_flows('00:00:00:00:00:00:00:0b', flow2)
