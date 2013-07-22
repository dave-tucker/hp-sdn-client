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
               'set_vlan_id',
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
            if isinstance(data.get(attr),list):
                for item in getattr(self, attr):
                    tmp = []
                    if isinstance(item, JsonObject):
                        tmp.append(item.to_dict())
                    else:
                        tmp.append(getattr(self, attr))
                    data[attr.__str__()] = tmp
            elif type(getattr(self,attr)):
                data[attr.__str__()] = getattr(self, attr)
        return data

    @staticmethod
    def factory(data):
        tmp = _find_class(data)
        attributes = [attr for attr in dir(tmp) if not callable(getattr(tmp,attr)) and not attr.startswith("__")]
        for attr in attributes:
            if isinstance(data.get(attr),list):
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
    def __init__(self):
        self.dpid = None
        self.negotiated_version = None
        self.ready = None
        self.last_message = None
        self.num_buffers = None
        self.num_tables = None
        self.supported_actions = []
        self.capabilities = []
        self.num_ports = None
        self.device_ip = None
        self.device_port = None
        self.masters = []
        self.slaves = []

class Port(JsonObject):
    id = None
    name = None
    mac = None
    current_speed = None
    max_speed = None
    config = []
    state = []
    current_features = []
    advertised_features = []
    supported_features = []
    peer_features = []

class Flow(JsonObject):
    table_id = None
    priority = None
    match = []
    duration_sec = None
    duration_nsec = None
    idle_timeout = None
    hard_timeout = None
    packet_cout = None
    byte_count = None
    cookie = None
    cookie_mask = None
    buffer_id = None
    out_port = None
    flow_mod_cmd = None
    flow_mod_flags = []
    instructions = []
    actions = []

class MatchField(JsonObject):
    in_port = None
    in_phy_port = None
    metadata = None
    tunnel_id = None
    eth_dst = None
    eth_src = None
    eth_type = None
    ip_proto = None
    icmpv6_type = None
    ipv6_nd_sll = None
    ipv6_nd_tll = None
    vlan_vid = None
    mode = None
    vlan_pcp = None
    ip_dscp = None
    ip_ecn = None
    icmpv4_code = None
    icmpv6_code = None
    mpls_tc = None
    mpls_bos = None
    arp_op = None
    ipv6_flabel = None
    mpls_Label = None
    pbb_isisd = None
    ipv4_src = None
    ipv4_dst = None
    arp_spa = None
    arp_tpa = None
    ipv6_src = None
    ipv6_dst = None
    ipv6_nd_target = None
    tcp_src = None
    tcp_dst = None
    udp_src = None
    udp_dst = None
    sctp_src = None
    sctp_dst = None
    icmpv4_type = None
    ipv6_exthdr = []

class Action(JsonObject):
    output = None
    copy_ttl_out = None
    copy_ttl_in = None
    set_mpls_ttl = None
    dec_mpls_ttls = None
    push_vlan = None
    pop_vlan = None
    push_mpls = None
    pop_mpls = None
    set_queue = None
    group = None
    set_nw_ttl = None
    dec_nw_ttl = None
    set_field = None
    push_pbb = None
    pop_pbb = None
    experimenter = None
    data = None

class Instruction(JsonObject):
    clear_actions = None
    write_actions = []
    apply_actions = []
    write_metadata = None
    mask = None
    meter = None
    experimenter = None

class MeterStats(JsonObject):
    id = None
    flow_count = None
    packet_count = None
    byte_count = None
    duration_sec = None
    duration_nsec = None
    band_stats = []

class BandStats(JsonObject):
    packet_count = None
    byte_count = None

class Meter(JsonObject):
    id = None
    command = None
    flags = []
    bands = []

class MeterBand(JsonObject):
    burst_size = None
    rate = None
    mtype = None
    prec_level = None
    experimenter = None    

class Group(JsonObject):
    id = id
    properties = None
    ref_count = None
    packet_count = None
    byte_count = None
    duration_sec = None
    duration_nsec = None
    bucket_stats = []
    type = None
    buckets = []

class Bucket(JsonObject):
    weight = None
    watch_group = None
    watch_port = None
    actions = []

class Stats(JsonObject):
    dpid = None
    version = None
    port_stats= []
    group_stats = []

class PortStats(JsonObject):
    portid = None
    rx_packets = None
    tx_packets = None
    rx_bytes = None
    tx_bytes = None
    rx_dropped = None
    tx_dropped = None
    rx_erros = None
    tx_errors = None
    collisions = None
    duration_sec = None
    rx_crc_err = None
    rx_frame_err = None
    rx_over_err = None

class GroupStats(JsonObject):
    groupid = None
    ref_count = None
    packet_count = None
    byte_count = None
    duration_sec = None
    duration_nsec = None
    bucket_stats = []
