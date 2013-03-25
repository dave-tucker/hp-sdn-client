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

"""This library provides a Python interface to the HP SDN Controller API"""

__author__ = 'Dave Tucker, Hewlett-Packard'
__version__ = '0.0.1'

import json
import sys
import time
import urllib

import requests

class FlareApiError(Exception):
  '''Base class for Flare API errors'''

  def message(self):
    return self.args[0]

class Config(object):
    """The Flare API Config object"""
    def __init__(self,
                 timeout = None,
                 use_ip_type = None):
        self.timeout = timeout
        self.use_ip_type = use_ip_type

    def __str__(self):
        return self.to_json_string()

    def _to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def _to_dict(self):
        data = {}
        if self.timeout:
            data['timeout'] = self.timeout
        if self.use_ip_type:
            data['useIpType'] = self.use_ip_type
        return data

    @staticmethod
    def _create_from_json(data):
        return Config(timeout = data.get('timeout',None),
                      use_ip_type = data.get('useIpType',None))


class System(object):
    def __init__(self, 
                 uid = None, 
                 address = None, 
                 port = None, 
                 role = None, 
                 config_revision = None, 
                 time = None, 
                 is_self = None):
        self.uid = uid
        self.address = address
        self.port = port
        self.role = role
        self.config_revision = config_revision
        self.time = time
        self.is_self = is_self

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = {}
        if self.uid:
            data['uid'] = self.uid
        if self.address:
            data['address'] = self.address
        if self.port:
            data['port'] = self.port
        if self.config_revision:
            data['configRevision'] = self.config_revision
        if self.time:
            data['time'] = self.time
        if self.is_self:
            data['self'] = self.is_self
        return data

    @staticmethod
    def create_from_json(data):
        return System(uid=data.get('uid',None),
                      address=data.get('address',None),
                      port=data.get('port', None),
                      role=data.get('role', None),
                      config_revision=data.get('configRevision', None),
                      time=data.get('time', None),
                      is_self=data.get('self', None))


class Device(object):
    def __init__(self,
                 ip = None, 
                 dpid = None, 
                 status = None):
        self.ip = ip
        self.dpid = dpid
        self.status = status

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = {}
        if self.ip:
            data['ip'] = self.ip
        if self.dpid:
            data['dpid'] = self.dpid
        if self.status:
            data['status'] = self.status
        return data

    @staticmethod
    def create_from_json(data):
        return Device(ip = data.get('ip', None),
                      dpid = data.get('dpid', None),
                      status = data.get('status', None))

class Mac(object):
    def __init__(self, 
                 mac = None, 
                 port = None, 
                 dpid = None, 
                 mac_type = None):
        self.mac = mac
        self.port = port
        self.dpid = dpid
        self.mac_type = mac_type

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = {}
        if self.mac:
            data['mac address'] = self.mac
        if self.port:
            data['port number'] = self.port
        if self.dpid:
            data['switch dpid'] = self.dpid
        if self.type:
            data['entry type'] = self.mac_type
        return data

    @staticmethod
    def create_from_json(data):
        return Mac(mac = data.get('mac address', None),
                   port = data.get('port', None),
                   dpid = data.get('switch dpid', None),
                   mac_type = data.get('entry type', None))

class Flow(object):
    def __init__(self,
                 dpid = None, 
                 in_port = None, 
                 src_mac = None, 
                 dst_mac = None, 
                 src_ip = None, 
                 dst_ip = None, 
                 action = None, 
                 multiple_actions = None, 
                 duration_seconds = None, 
                 packet_count = None,
                 byte_count = None, 
                 idle_timeout = None, 
                 data_layer_virtual_lan = None,
                 data_layer_priority_code_point = None,
                 data_layer_type = None,
                 network_tos = None,
                 network_protocol = None,
                 transport_src = None,
                 transport_dst = None):

        self.dpid = dpid
        self.in_port = in_port
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.action = action
        self.multiple_actions=[]
        self.duration_seconds  = duration_seconds
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.idle_timeout = idle_timeout
        self.data_layer_virtual_lan = data_layer_virtual_lan
        self.data_layer_priority_code_point = data_layer_priority_code_point
        self.data_layer_type = data_layer_type
        self.network_tos = network_tos
        self.network_protocol = network_protocol
        self.transport_src = transport_src
        self.transport_dst = transport_dst

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = {}
        if self.dpid:
            data['dpid'] = self.dpid
        if self.in_port:
            data['InPort'] = self.in_port
        if self.src_mac:
            data['SourceMAC'] = self.src_mac
        if self.dst_mac:
            data['DestMAC'] = self.dst_mac
        if self.src_ip:
            data['SourceIP'] = self.src_ip
        if self.dst_ip:
            data['DestIP'] = self.dst_ip
        if self.action:
            data['Action'] = self.action
        if self.multiple_actions:
            data['MultipleActions'] = self.multiple_actions
        if self.duration_seconds:
            data['DurationInSeconds'] = self.duration_seconds
        if self.packet_count:
            data['PacketCount'] = self.packet_count
        if self.byte_count:
            data['ByteCount'] = self.byte_count
        if self.idle_timeout:
            data['IdleTimeout'] = self.idle_timeout
        if self.data_layer_virtual_lan:
            data['DataLayerVirtualLan'] = self.data_layer_virtual_lan
        if self.data_layer_priority_code_point:
            data['DataLayerPriorityCodePoint'] = self.data_layer_priority_code_point
        if self.data_layer_type:
            data['DataLayerType'] = self.data_layer_type
        if self.network_tos:
            data['NetworkTypeOfService'] = self.network_tos
        if self.network_protocol:
            data['NetworkProtocol'] = self.network_protocol
        if self.transport_src:
            data['TransportSource'] = self.transport_src
        if self.transport_dst:
            data['TransportDestination'] = self.transport_dst
        return data

    @staticmethod
    def create_from_json(data):
        return Flow(dpid = data.get('dpid', None),
                    in_port = data.get('InPort', None),
                    src_mac = data.get('SourceMAC', None), 
                    dst_mac = data.get('DestMAC', None),
                    src_ip= data.get('SourceIP', None), 
                    dst_ip= data.get('DestIP', None),
                    action= data.get('Action', None), 
                    multiple_actions= data.get('MutlipleActions', None), 
                    duration_seconds = data.get('DurationInSeconds', None), 
                    packet_count= data.get('PacketCount', None),
                    byte_count= data.get('ByteCount', None), 
                    idle_timeout= data.get('IdleTimeout', None),
                    data_layer_virtual_lan= data.get('DataLayerVirtualLan', None),
                    data_layer_priority_code_point= data.get('DataLayerVirtualLanPriorityCodePoint', None), 
                    data_layer_type= data.get('DataLayerType', None), 
                    network_tos= data.get('NetworkTypeOfService', None),
                    network_protocol= data.get('NetworkProtocol', None), 
                    transport_src= data.get('TransportSource', None), 
                    transport_dst= data.get('TransportDestination', None)
                    )


class Limiter(object):
    def __init__(self, 
                 dpid = None,
                 sub_type = None,
                 max_objects = None,
                 capabilities = None,
                 limiter_id = None,
                 flags = None,
                 drop_rate = None,
                 mark_rate = None,
                 burst_size = None):
        self.dpid = dpid
        self.sub_type = sub_type,
        self.max_objects = max_objects
        self.capabilities = capabilities
        self.drop_rate = drop_rate
        self.mark_rate = mark_rate
        self.burst_size = burst_size

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = {}

    @staticmethod
    def create_from_json(data):
        return Limiter(dpid = data.get('dpid', None),
                       sub_type = data.get('sub_type', None),
                       max_objects = data.get('max_objects', None),
                       capabilities = data.get('capabilities', None),
                       limiter_id = data.get('limiter_id', None),
                       flags = data.get('flags', None),
                       drop_rate = data.get('drop_rate', None),
                       mark_rate = data.get('mark_rate', None),
                       burst_size = data.get('burst_size', None))


class ApiBase(object):
    def __init__(self,
             base_url = 'http://127.0.0.1:8080/sdn/v1.0',
             user = 'sdn',
             password = 'skyline',
             domain = 'sdn'):
    
        self.base_url = base_url
        self.user = user
        self.password = password
        self.domain = domain

class Api(ApiBase):
    def __init__(self, **kwds):
        super(Api, self).__init__(**kwds)
        self.auth_token = XAuthToken(base_url = self.base_url,
                                user = self.user,
                                domain = self.domain,
                                password = self.password)

    def get_devices(self):
        url = '{0}/devices'.format(self.base_url)
        r = requests.get(url, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            data = r.json()
            devices = []
            for device in data:
                if 'error' in device:
                    raise FlareApiError("No devices found")
                else:
                    devices.append(Device.create_from_json(device))
            return devices
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def get_flows_by_dpid(self, dpid):
        url = '{0}/devices/{1}/flows'.format(self.base_url, urllib.quote(dpid))
        r = requests.get(url, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            data = r.json()
            flows = []
            for flow in data:
                if 'error' in flow:
                    raise FlareApiError("No Flows")
                else:
                    flows.append(Flow.create_from_json(flow))
            return flows
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def create_flow(self, dpid, flow):
        url = '{0}/devices/{1}/flows'.format(self.base_url, urllib.quote(dpid))
        data = flow.to_json_string()
        r = requests.post(url, data = data, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            return True
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def delete_flow(self, flow):
        url = '{0}/devices/flows'.format(self.base_url)
        data = flow.to_json_string()
        r = requests.delete(url, data = data, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            raise FlareApiError("Oh noes! Something went wrong")
            print >> sys.stderr, r.raw()
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()
    
    def get_limiters_by_dpid(self, dpid):
        url = '{0}/devices/{1}/limiters'.format(self.base_url, urllib.quote(dpid))
        r = requests.get(url, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            data = r.json()
            limiters = []
            for limiter in data:
                if 'error' in limiter:
                    print >> sys.stderr, "No limiters found"
                    break
                else:
                    limiter.append(Limiter.create_from_json(limiter))
            return limiters
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def create_limiter(self, limiter):
        url = '{0}/devices/{1}/limiters'.format(self.base_url, urllib.quote(dpid))
        data = limiter.to_json_string()
        r = requests.post(url, data = data, auth=self.auth_token)
        if r.status_code == requests.codes.ok:
            return True
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

class XAuthToken(requests.auth.AuthBase, ApiBase):
    def __init__(self, **kwds):
        super(XAuthToken, self).__init__(**kwds)
        
        self.token = None
        self.token_expiration = None

    def __call__(self, r):
        if self.token is None or self.token_expiration > time.gmtime():
            self.get_auth()
        r.headers['X-Auth-Token'] = self.token
        return r

    def get_auth(self):
        url = '{0}/auth'.format(self.base_url)
        payload = {'login':{ 'user': self.user, 'password': self.password, 'domain': self.domain}}
        r = requests.post(url, data=json.dumps(payload))
        if r.status_code == requests.codes.ok:
            data = r.json()
            self.token = data[u'record'][u'token']
            self.token_expiration = time.gmtime(data[u'record'][u'expiration']/1000)
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()

    def delete_auth(self):
        url = '{0}/auth'.format(self.base_url)
        headers = {"X-Auth-Token":self.token}
        r = requests.delete(url, headers=headers)
        if r.status_code == requests.codes.ok:
            self.token = None
            self.token_expiration = None
        else:
            raise FlareApiError("Oh noes! Something went wrong")
            r.raise_for_status()
