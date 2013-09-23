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

Currently:

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
__version__ = '0.1.0'

import urllib

import rest
import types
from error import FlareApiError

class Of(object):

	def __init__(self):
		pass

	# STATS #
	def get_stats(self):
		""" get_stats()

			List controller statistics for all controllers that are part of this controller's team.

			Notes: Currently returns []. Not implemented

		"""

		url = 'http://{0}:8080/sdn/v2.0/of/stats'.format(self.controller)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['stats']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_port_stats(self, dpid, port_id=None):
		""" get_port_stats()

			List all port statistics or by a given datapath or by a given datapath and port number.

			Notes: Always returns stat block for dpid b0:0b:00:00:36:00:65:02

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/stats/ports?dpid={1}'.format(self.controller, urllib.quote(dpid))
		if port_id:
			url = url + '&port_id={0}'.format(port_id)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['stats']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_group_stats(self, dpid, group_id=None):
		""" get_group_stats()

			List group statistics

			Notes: Returns error for dpid not found.

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/stats/groups?dpid={1}'.format(self.controller, urllib.quote(dpid))
		if group_id:
			url = url + '&port_id={0}'.format(group_id)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_meter_stats(self, dpid):
		""" get_meter_stats()

			List meter statistics

			Notes: 

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/stats/meters?dpid={1}'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return r

	# DATAPATHS #

	def get_datapaths(self):
		""" get_datapaths() 

			List all datapaths that are managed by this controller.

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths'.format(self.controller)
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['datapaths']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_datapath_detail(self, dpid):
		""" get_datapath()

			Get detail information on a datapath.

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r['datapath'])

	def get_datapath_meter_features(self, dpid):
		""" get_datapath_meter_features()

			Not implemented

		"""

		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/features/meter'.format(self.controller, urllib.quote(dpid))
		pass

	def get_datapath_group_features(self, dpid):
		""" get_datapath_group_features()

			Not implemented

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/features/groups'.format(self.controller, urllib.quote(dpid))
		pass

	def get_ports(self, dpid):
		""" get_ports()

			List all ports for this datapath 

		"""

		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/ports'.format(self.controller, urllib.quote(dpid))
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['ports']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_port_detail(self, dpid, port_id):
		""" get_port_detail()

			Gets detailed port information
			
		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/ports/{2}'.format(self.controller, urllib.quote(dpid), port_id)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r['port'])

	def get_meters(self, dpid):
		""" get_meters()

			List all meters
			
		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def add_meter(self, dpid, meters):
		""" add_meter()

			Add a new meter
			
		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, meters, 'json')
		return types.JsonObject.factory(r)

	def get_meter_details(self, dpid, meter_id):
		""" get_meter_details ()

			Get detailed meter information

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meter_id)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def update_meter(self, dpid, meterid, meter):
		""" update_meter ()

			Update a meter 

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meterid)
		r = rest.put(url, self.auth_token, meters, 'json')
		return types.JsonObject.factory(r)

	def delete_meter(self, dpid, meterid):
		""" delete_meter()

			Delete a meter
			
		"""

		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meterid)
		r = rest.delete(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def get_flows(self, dpid):
		""" get_flows()

			Gets a list of flows
			
		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		data = rest.get(url, self.auth_token, 'json')
		r = []
		for d in data['flows']:
			r.append(types.JsonObject.factory(d))
		return r

	def add_flows(self, dpid, flow):
		""" add_flows()

			Add a flow, or flows
			
		"""
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

	def update_flows(self, dpid, flow):
		""" update_flows()

			Update a flow, or flows
			
		"""

		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		r = rest.put(url, self.auth_token, flow, 'json')
		return types.JsonObject.factory(r)

	def delete_flows(self, dpid, flows):
		""" delete_flows()

			Delete flow, or flows

		"""

		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		r = rest.delete(url, self.auth_token, flow, 'json')
		return types.JsonObject.factory(r)

	def get_groups(self, dpid):
		""" get_groups()

			Get a list of groups

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def add_groups(self, dpid, group):
		""" add_groups ()

			Add a group, or groups

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, group, 'json')
		return types.JsonObject.factory(r)

	def get_group(self, dpid, groupid):
		""" get_groups ()

			Get group details

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		r = rest.get(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

	def update_groups(self, dpid, groupid, groups):
		""" update_groups ()

			Update a group, or groups

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid))
		r = rest.post(url, self.auth_token, groups, 'json')
		return types.JsonObject.factory(r)

	def delete_groups(self, dpid, groupid):
		""" delete_groups ()

			Delete a group or groups

		"""
		url = 'http://{0}:8080/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		r = rest.delete(url, self.auth_token, 'json')
		return types.JsonObject.factory(r)

