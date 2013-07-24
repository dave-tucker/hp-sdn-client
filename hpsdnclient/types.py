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

""" Data Types used for the REST objects """

import json
import inspect

ETHERNET = ['ipv4','arp','rarp','snmp','ipv6','mpls_u', 'mpls_m', 'lldp', 'pbb', 'bddp']

VERSION = ['1.0.0', '1.1.0', '1.2.0', '1.3.0)']

ACTIONS = ['output', 
           'set_vlan_vid',
           'set_vlan_pcp',
           'strip_vlan',
           'set_dl_src',
           'set_dl_dst',
           'set_nw_src',
           'set_nw_dst',
           'set_nw_tos',
           'set_tp_src',
           'set_tp_dst',
           'enqueue']

CAPABILITIES = ['flow_stats',
                'table_stats',
                'port_stats',
                'stp',
                'group_stats',
                'reserved',
                'ip_reasm',
                'queue_stats',
                'arp_match_ip',
                'port_blocked'
                ]

PORT_CONFIG = ["port_down",
               "no_stp",
               "no_recv",
               "ro_recv_stp",
               "no_flood",
               "no_fwd",
               "no_packet_in"
               ]

PORT_STATE = ["link_down",
              "blocked",
              "live",
              "stp_listen",
              "stp_learn",
              "stp_forward",
              "stp_block"
             ]

PORT_FEATURES = ["rate_10mb_hd",
                 "rate_10mb_fd",
                 "rate_100mb_hd",
                 "rate_100mb_fd",
                 "rate_1gb_hd",
                 "rate_1gb_fd",
                 "rate_10gb_fd",
                 "rate_40gb_fd",
                 "rate_100gb_fd",
                 "rate_1tb_fd",
                 "rate_other",
                 "copper",
                 "fiber",
                 "autoneg",
                 "pause",
                 "pause_asym"
                ]

FLOW_MOD_CMD = ["add",
                "modify",
                "modify_strict",
                "delete",
                "delete_strict"
                ]

FLOW_MOD_FLAGS = ["send_flow_rem",
                  "check_overlap",
                  "emerg",
                  "reset_counts",
                  "no_packet_counts",
                  "no_byte_counts"]

IP_PROTOCOL = ["tcp",
               "udp",
               "sctp",
               "icmp",
               "ipv6-icmp"
               ]

ICMP_V6_TYPE = ["nbr_sol", "nbr_adv"]

MATCH_MODE = ["none", "present", "exact"]

IPV6_EXTHDR = ["no_next",
                   "esp",
                   "auth",
                   "dest",
                   "frag",
                   "router",
                   "hop",
                   "un_rep",
                   "un_seq"]

METER_FLAGS = ["kbps",
                   "pktps",
                   "burst",
                   "stats"]

METER_TYPE = ["drop", "dscp_remark","experimenter"]

GROUP_TYPE = ["all", "select", "indirect", "ff"]

COMMANDS = ["add", "modify", "delete"]

enums = [ ETHERNET,
          VERSION, 
          ACTIONS,
          CAPABILITIES,
          PORT_CONFIG,
          PORT_STATE,
          PORT_FEATURES,
          FLOW_MOD_CMD,
          FLOW_MOD_FLAGS,
          IP_PROTOCOL,
          ICMP_V6_TYPE,
          MATCH_MODE,
          ICMP_V6_TYPE,
          MATCH_MODE,
          IPV6_EXTHDR,
          METER_FLAGS,
          METER_TYPE,
          GROUP_TYPE,
          COMMANDS
        ]


def _find_class(data):
    keys = [d for d in data]
    for c in JsonObject.__subclasses__():
        cls = c()
        if all(k in dir(cls) for k in keys):
            return cls
            break

class JsonObject(object):
    def __init__(self):
        pass

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        tmp = self.to_dict()
        return json.dumps(tmp,sort_keys=True, indent=4, separators=(',', ': '))
    
    def to_dict(self):
        data = {}
        attributes = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for attr in attributes:
            if getattr(self,attr):
                value = getattr(self,attr) 
                if isinstance(value, list):
                    for item in value:
                        tmp = []
                        if isinstance(item, JsonObject):
                            tmp.append(item.to_dict())
                        else:
                            tmp.append(value)
                        data[attr.__str__()] = tmp
                elif isinstance(value, JsonObject):
                            data[attr.__str__()] = value.to_dict()
                elif type(value):
                    data[attr.__str__()] = value
        return data

    @staticmethod
    def factory(data):
        tmp = _find_class(data)
        attributes = [attr for attr in dir(tmp) if not callable(getattr(tmp,attr)) and not attr.startswith("__")]
        for attr in attributes:
            if attr in class_bindings:
                cls = class_bindings[attr].factory(data.get(attr))
                setattr(tmp, attr, cls)
            elif isinstance(data.get(attr),list):
                #Could be an enum or a class
                for e in enums:
                    if all(k in e for k in data.get(attr)):
                        setattr(tmp, attr, data.get(attr))
                        break
                else:
                    lst = []
                    for item in data.get(attr):
                        lst.append(JsonObject.factory(item))
                        setattr(tmp, attr, lst)
            else:
                setattr(tmp, attr, data.get(attr))
        return tmp

class Datapath(JsonObject):
    """The Flare Datapath Object"""
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.negotiated_version = kwargs.get('negotiated_version', None)
        self.ready = kwargs.get('ready', None)
        self.last_message = kwargs.get('last_message', None)
        self.num_buffers = kwargs.get('num_buffers', None)
        self.num_tables = kwargs.get('num_tables',None)
        self.supported_actions = kwargs.get('supported_action',[])
        self.capabilities = kwargs.get('capabilities',[])
        self.num_ports = kwargs.get('num_ports', None)
        self.device_ip = kwargs.get('device_ip', None)
        self.device_port = kwargs.get('device_port', None)
        self.masters = kwargs.get('masters', [])
        self.slaves = kwargs.get('num_slaves', [])

class Port(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.mac = kwargs.get('mac', None)
        self.current_speed = kwargs.get('current_speed', None)
        self.max_speed = kwargs.get('max_speed', None)
        self.config = kwargs.get('config', [])
        self.state = kwargs.get('state', [])
        self.current_features = kwargs.get('current_features', [])
        self.advertised_features = kwargs.get('advertised_features', [])
        self.supported_features = kwargs.get('supported_features', [])
        self.peer_features = kwargs.get('peer_features', [])

class Flow(JsonObject):
    def __init__(self, **kwargs):
        self.table_id = kwargs.get('table_id', None)
        self.priority = kwargs.get('priority', None)
        self.match = kwargs.get('match', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.idle_timeout = kwargs.get('idle_timeout', None)
        self.hard_timeout = kwargs.get('hard_timeout', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.cookie = kwargs.get('cookie', None)
        self.cookie_mask = kwargs.get('cookie_mask', None)
        self.buffer_id = kwargs.get('buffer_id', None)
        self.out_port = kwargs.get('out_port', None)
        self.flow_mod_cmd = kwargs.get('flow_mod_cmd', None)
        self.flow_mod_flags = kwargs.get('flow_mod_flags', [])
        self.instructions = kwargs.get('instructions', [])
        self.actions = kwargs.get('actions', [])

class Match(JsonObject):
    def __init__(self, **kwargs):
        self.in_port = kwargs.get('in_port', None)
        self.in_phy_port = kwargs.get('in_port_phy', None)
        self.metadata = kwargs.get('metadata', None)
        self.tunnel_id = kwargs.get('tunnel_id', None)
        self.eth_dst = kwargs.get('eth_dst', None) 
        self.eth_src = kwargs.get('eth_src', None)
        self.eth_type = kwargs.get('eth_src', None)
        self.ip_proto = kwargs.get('ip_proto', None)
        self.icmpv6_type = kwargs.get('icmpv6_type', None)
        self.ipv6_nd_sll = kwargs.get('ipv6_nd_sll', None)
        self.ipv6_nd_tll = kwargs.get('ipv6_nd_tll', None)
        self.vlan_vid = kwargs.get('vlan_vid', None)
        self.mode = kwargs.get('mode', None)
        self.vlan_pcp = kwargs.get('vlan_pcp', None)
        self.ip_dscp = kwargs.get('ip_dscp', None)
        self.ip_ecn = kwargs.get('ip_ecn', None)
        self.icmpv4_code = kwargs.get('icmpv4_code', None)
        self.icmpv6_code = kwargs.get('icmpv6_type', None)
        self.mpls_tc = kwargs.get('mpls_tc', None)
        self.mpls_bos = kwargs.get('mpls_bos', None)
        self.arp_op = kwargs.get('arp_op', None)
        self.ipv6_flabel = kwargs.get('ipv6_flabel', None)
        self.mpls_label = kwargs.get('mpls_label', None)
        self.pbb_isisd = kwargs.get('pbb_isisd', None)
        self.ipv4_src = kwargs.get('ipv4_src', None)
        self.ipv4_dst = kwargs.get('ipv4_dst', None)
        self.arp_spa = kwargs.get('arp_spa', None)
        self.arp_tpa = kwargs.get('arp_tpa', None)
        self.ipv6_src = kwargs.get('ipv6_src', None)
        self.ipv6_dst = kwargs.get('ipv6_dst', None)
        self.ipv6_nd_target = kwargs.get('ipv6_nd_target', None)
        self.tcp_src = kwargs.get('tcp_src', None)
        self.tcp_dst = kwargs.get('tcp_dst', None)
        self.udp_src = kwargs.get('udp_src', None)
        self.udp_dst = kwargs.get('udp_dst', None)
        self.sctp_src = kwargs.get('sctp_src', None)
        self.sctp_dst = kwargs.get('sctp_dst', None)
        self.icmpv4_type = kwargs.get('icmpv4_type', None)
        self.ipv6_exthdr = kwargs.get('ipv6_exthdr', None)

    def to_dict(self):
        data = []
        attributes = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for attr in attributes:
            if getattr(self,attr):
                tmp = {}
                tmp[attr.__str__()] = getattr(self,attr) 
                data.append(tmp)
        return data

    @staticmethod
    def factory(data):
        tmp = Match()
        attributes = [attr for attr in dir(tmp) if not callable(getattr(tmp,attr)) and not attr.startswith("__")]
        for d in data:
            if isinstance(d, dict):
                for key in d:
                    setattr(tmp, key, d[key])
            else:
                raise FlareApiError("Invalid data type. Expected list of dicts, got {0}".format(type(data.get(d))))
        return tmp

class Action(JsonObject):
    def __init__(self, **kwargs):
        self.output = kwargs.get('output', None)
        self.copy_ttl_out = kwargs.get('copy_ttl_out', None)
        self.copy_ttl_in = kwargs.get('copy_ttl_in', None)
        self.set_mpls_ttl = kwargs.get('set_mpls_ttl', None)
        self.dec_mpls_ttls = kwargs.get('dec_mpls_ttls', None)
        self.push_vlan = kwargs.get('push_vlan', None)
        self.pop_vlan = kwargs.get('pop_vlan', None)
        self.push_mpls = kwargs.get('push_mpls', None)
        self.pop_mpls = kwargs.get('pop_mpls', None)
        self.set_queue = kwargs.get('set_queue', None)
        self.group = kwargs.get('group', None)
        self.set_nw_ttl = kwargs.get('set_nw_ttl', None)
        self.dec_nw_ttl = kwargs.get('dec_nw_ttl', None)
        self.set_field = kwargs.get('set_field', None)
        self.push_pbb = kwargs.get('push_pbb', None)
        self.pop_pbb = kwargs.get('pop_pbb', None)
        self.experimenter = kwargs.get('experimenter', None)
        self.data = kwargs.get('data', None)

    def to_dict(self):
        data = []
        attributes = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for attr in attributes:
            if getattr(self,attr):
                tmp = {}
                tmp[attr.__str__()] = getattr(self,attr) 
                data.append(tmp)
        return data

    @staticmethod
    def factory(data):
        tmp = Action()
        attributes = [attr for attr in dir(tmp) if not callable(getattr(tmp,attr)) and not attr.startswith("__")]
        for d in data:
            if isinstance(d, dict):
                for key in d:
                    setattr(tmp, key, d[key])
            else:
                raise FlareApiError("Invalid data type. Expected list of dicts, got {0}".format(type(data.get(d))))
        return tmp

class Instruction(JsonObject,):
    def __init__(self, **kwargs):
        self.clear_actions = kwargs.get('clear_actions', None)
        self.write_actions = kwargs.get('write_actions', [])
        self.apply_actions = kwargs.get('apply_actions', [])
        self.write_metadata = kwargs.get('write_metadata', None)
        self.mask = kwargs.get('mask', None)
        self.meter = kwargs.get('meter', None)
        self.experimenter = kwargs.get('experimenter', None)

class MeterStats(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.flow_count = kwargs.get('flow_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.band_stats = kwargs.get('band_stats', [])

class BandStats(JsonObject):
    def __init__(self, **kwargs):
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)

class Meter(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.command = kwargs.get('command', None)
        self.flags = kwargs.get('flags',[])
        self.bands = kwargs.get('bands',[])

class MeterBand(JsonObject):
    def __init__(self, **kwargs):
        self.burst_size = kwargs.get('burst_size', None)
        self.rate = kwargs.get('rate', None)
        self.mtype = kwargs.get('mtype', None)
        self.prec_level = kwargs.get('prec_level', None)
        self.experimenter = kwargs.get('experimenter', None)    

class Group(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id',None)
        self.properties = kwargs.get('properties',None)
        self.ref_count = kwargs.get('ref_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.bucket_stats = kwargs.get('bucket_stats', [])
        self.type = kwargs.get('type', None)
        self.buckets = kwargs.get('buckets', [])

class Bucket(JsonObject):
    def __init__(self, **kwargs):
        self.weight = kwargs.get('weight', None)
        self.watch_group = kwargs.get('watch_group', None)
        self.watch_port = kwargs.get('watch_port', None)
        self.actions = kwargs.get('actions', [])

class Stats(JsonObject):
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.version = kwargs.get('version', None)
        self.port_stats= kwargs.get('port_stats', [])
        self.group_stats = kwargs.get('group_stats', [])

class PortStats(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.rx_packets = kwargs.get('rx_packets', None)
        self.tx_packets = kwargs.get('tx_packets', None)
        self.rx_bytes = kwargs.get('rx_bytes', None)
        self.tx_bytes = kwargs.get('tx_bytes', None)
        self.rx_dropped = kwargs.get('rx_dropped', None)
        self.tx_dropped = kwargs.get('tx_dropped', None)
        self.rx_errors = kwargs.get('rx_errors', None)
        self.tx_errors = kwargs.get('tx_errors', None)
        self.collisions = kwargs.get('collisions', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.rx_crc_err = kwargs.get('rx_crc_err', None)
        self.rx_frame_err = kwargs.get('rx_frame_err', None)
        self.rx_over_err = kwargs.get('rx_over_err', None)

class GroupStats(JsonObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.ref_count = kwargs.get('ref_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.bucket_stats = kwargs.get('bucket_stats', [])

class_bindings = {'match' : Match,
                  'actions' : Action }
