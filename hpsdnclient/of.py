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

"""
Implementation of the Flare OpenFlow REST API 

/stats	GET
/stats/ports	GET
/stats/groups	GET
/stats/meters	GET
/datapaths	GET
/datapaths/{dpid}	GET
/datapaths/{dpid}/features/meter	GET
/datapaths/{dpid}/features/group	GET
/datapaths/{dpid}/ports/{port_id}/action	POST
/datapaths/{dpid}/meters	GET
/datapaths/{dpid}/meters	POST
/datapaths/{dpid}/meters/{meter_id}	GET
/datapaths/{dpid}/meters/{meter_id}	PUT
/datapaths/{dpid}/meters/{meter_id}	DELETE
/datapaths/{dpid}/flows	GET
/datapaths/{dpid}/flows	POST
/datapaths/{dpid}/flows	PUT
/datapaths/{dpid}/flows	DELETE
/datapaths/{dpid}/groups	GET
/datapaths/{dpid}/groups	POST
/datapaths/{dpid}/groups/{group_id}	GET
/datapaths/{dpid}/groups/{group_id}	PUT
/datapaths/{dpid}/groups/{group_id}	DELETE

"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.0.1'

import urllib

import rest
import types
from error import FlareApiError

class Of(object):

	def __init__(self):
		pass

	# STATS #
	def get_stats(self):
		url = 'http://{0}:8080/sdn/v2.0/of/stats'.format(self.controller)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_port_stats(self):
		url = 'http://{0}:8080/sdn/v2.0/of/stats/ports'.format(self.controller)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_group_stats(self):
		url = 'http://{0}:8080/sdn/v2.0/of/stats/groups'.format(self.controller)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_meter_stats(self):
		url = 'http://{0}:8080/sdn/v2.0/of/stats/meters'.format(self.controller)
		r = rest.get(url, self.auth_token, 'json')
		return r

	# DATAPATHS #

	def get_datapaths(self):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths'.format(self.controller)
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['datapaths']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_datapath(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_meter_features(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/features/meter'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		if not r:
			raise FlareApiError('No data')
		else:
			return types.JsonObject.factory(r)

	def get_datapath_group_features(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/features/groups'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		if not r:
			raise FlareApiError('No data')
		else:
			return types.JsonObject.factory(r)

	def get_datapath_ports(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/ports'.format(self.controller, urllib.quote(dpid))
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['ports']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_datapaths_port(self, dpid, portid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/ports/{2}'.format(self.controller, urllib.quote(dpid), portid)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def set_datapaths_port_actions(self, dpid, portid, actions):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/ports/{2}/action'.format(self.controller, urllib.quote(dpid), portid)
		r = rest.post(url, self.auth_token, actions, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_meters(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def add_datapath_meter(self, dpid, meters):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, meters, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_meter(self, dpid, meterid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meterid)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def update_datapath_meter(self, dpid, meterid, meter):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meterid)
		r = rest.put(url, self.auth_token, meters, 'json')
		return types.JsonObject.factory(r)

	def delete_datapath_meter(self, dpid, meterid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meterid)
		r = rest.delete(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_flows(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['flows']:
			r.append(types.JsonObject.factory(d))
		return r

	def add_datapath_flows(self, dpid, flow):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		if isinstance(flows, list):
			tmp = []
			for d in data:
				if isinstance(d, types.Flow):
					tmp.append(d.to_dict())
				else:
					raise FlareApiError("Invalid object passed to add_datapath_flows. Expected types.Flow or a list of types.Flow")
					break
			data = [{"flows": tmp }]
		elif isinstance(flows, types.Flow):
			data = [{"flows": flow.to_dict() }]
		else:
			raise FlareApiError("Invalid object passed to add_datapath_flows. Expected types.Flow or a list of types.Flow")

		if rest.post(url, self.auth_token, json.dumps(flow), 'json'):
			return
		else:
			raise FlareApiError('Something went wrong')

	def update_datapath_flows(self, dpid, flow):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		r = rest.put(url, self.auth_token, flow, 'json')
		return types.JsonObject.factory(r)

	def delete_datapath_flows(self, dpid, flows):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		r = rest.delete(url, self.auth_token, flow, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_groups(self, dpid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def add_datapath_groups(self, dpid, group):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, group, 'json')
		return types.JsonObject.factory(r)

	def get_datapath_group(self, dpid, groupid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def update_datapath_groups(self, dpid, groupid, groups):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, groups, 'json')
		return types.JsonObject.factory(r)

	def delete_datapath_groups(self, dpid, groupid):
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		r = rest.delete(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

