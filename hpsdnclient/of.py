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

import json
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

		"""

		url = 'https://{0}:8443/sdn/v2.0/of/stats'.format(self.controller)
		r = []
		try:
			data = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		for d in data['controller_stats']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_port_stats(self, dpid, port_id=None):
		""" get_port_stats()

			List all port statistics or by a given datapath or by a given datapath and port number.

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/stats/ports?dpid={1}'.format(self.controller, urllib.quote(dpid))
		if port_id:
			url = url + '&port_id={0}'.format(port_id)
		r = []
		
		try:
			data = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		for d in data['stats']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_group_stats(self, dpid, group_id=None):
		""" get_group_stats()

			List group statistics

			Notes: Returns error for dpid not found.

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/stats/groups?dpid={1}'.format(self.controller, urllib.quote(dpid))
		if group_id:
			url = url + '&port_id={0}'.format(group_id)
		
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def get_meter_stats(self, dpid, meter_id):
		""" get_meter_stats()

			List meter statistics

			Notes: 

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/stats/meters?dpid={1}&meter={2}'.format(self.controller, urllib.quote(dpid), meter_id)
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return r

	# DATAPATHS #

	def get_datapaths(self):
		""" get_datapaths() 

			List all datapaths that are managed by this controller.

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths'.format(self.controller)
		try:
			data = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		r = []
		for d in data['datapaths']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_datapath_detail(self, dpid):
		""" get_datapath()

			Get detail information on a datapath.

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r['datapath'])

	def get_datapath_meter_features(self, dpid):
		""" get_datapath_meter_features()

			Not implemented

		"""

		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/features/meter'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r['meter_features'])


	def get_datapath_group_features(self, dpid):
		""" get_datapath_group_features()

			Not implemented

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/features/groups'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r['group_features'])


	def get_ports(self, dpid):
		""" get_ports()

			List all ports for this datapath 

		"""

		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/ports'.format(self.controller, urllib.quote(dpid))
		
		try:
			data = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		r = []
		for d in data['ports']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_port_detail(self, dpid, port_id):
		""" get_port_detail()

			Gets detailed port information
			
		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/ports/{2}'.format(self.controller, urllib.quote(dpid), port_id)
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r['port'])

	def get_meters(self, dpid):
		""" get_meters()

			List all meters
			
		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def add_meters(self, dpid, meters):
		""" add_meter()

			Add a new meter
			
		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/meters'.format(self.controller, urllib.quote(dpid))
		try:
			rest.post(url, self.auth_token, json.dumps(meters.to_dict()))
		except Exception, e:
			raise FlareApiError('Something went wrong... {0}'.format(e))

	def get_meter_details(self, dpid, meter_id):
		""" get_meter_details ()

			Get detailed meter information

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meter_id)
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def update_meter(self, dpid, meter_id, meter):
		""" update_meter ()

			Update a meter 

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meter_id)
		try:
			r = rest.put(url, self.auth_token, meters, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def delete_meter(self, dpid, meter_id):
		""" delete_meter()

			Delete a meter
			
		"""

		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/meters/{2}'.format(self.controller, urllib.quote(dpid), meter_id)
		try:
			r = rest.delete(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def get_flows(self, dpid):
		""" get_flows()

			Gets a list of flows
			
		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		try:
			data = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		r = []
		for d in data['flows']:
			r.append(types.JsonObject.factory(d))
		return r

	def add_flows(self, dpid, flows):
		""" add_flows()

			Add a flow, or flows
			
		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		if isinstance(flows, list):
			tmp = []
			for f in flows:
				if isinstance(d, types.Flow):
					tmp.append(d.to_dict())
				else:
					raise FlareApiError("Invalid object passed to add_datapath_flows. Expected types.Flow or a list of types.Flow")
					break
			data = { "flows" : tmp }
		elif isinstance(flows, types.Flow):
			data = { "flow" : flows.to_dict() }
		else:
			raise FlareApiError("Invalid object passed to add_datapath_flows. Expected types.Flow or a list of types.Flow")
		try:
			r = rest.post(url, self.auth_token, json.dumps(data))
		except Exception, e:
			print data
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

	def update_flows(self, dpid, flow):
		""" update_flows()

			Update a flow, or flows
			
		"""

		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.put(url, self.auth_token, flow, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def delete_flows(self, dpid, flows):
		""" delete_flows()

			Delete flow, or flows

		"""

		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/flows'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.delete(url, self.auth_token, flow, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

	def get_groups(self, dpid):
		""" get_groups()

			Get a list of groups

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError('Something went wrong... {0}'.format(e))

		return types.JsonObject.factory(r)

	def add_groups(self, dpid, groups):
		""" add_groups ()

			Add a group, or groups

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/groups'.format(self.controller, urllib.quote(dpid))
		try:
			rest.post(url, self.auth_token, json.dumps(groups.to_dict()))
		except Exception, e:
			raise FlareApiError('Something went wrong... {0}'.format(e))

	def get_group_details(self, dpid, groupid):
		""" get_groups ()

			Get group details

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		
		try:
			r = rest.get(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError('Something went wrong... {0}'.format(e))

		return types.JsonObject.factory(r)

	def update_groups(self, dpid, groupid, groups):
		""" update_groups ()

			Update a group, or groups

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid))
		try:
			rest.post(url, self.auth_token, json.dumps(groups.to_dict()))
		except Exception, e:
			raise FlareApiError('Something went wrong... {0}'.format(e))

	def delete_groups(self, dpid, groupid):
		""" delete_groups ()

			Delete a group or groups

		"""
		url = 'https://{0}:8443/sdn/v2.0/of/datapaths/{1}/groups/{2}'.format(self.controller, urllib.quote(dpid), groupid)
		try:
			r = rest.delete(url, self.auth_token, 'json')
		except Exception, e:
			raise FlareApiError("Something went wrong with your request. {0}".format(e))

		return types.JsonObject.factory(r)

