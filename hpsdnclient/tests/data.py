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

""" Test data for use in unit tests """

LICENSE = {
    "install_id": 1234567,
    "serial_no": 10,
    "license_metric": "Controller Node",
    "product": "HP VAN SDN Ctrl Base",
    "metric_qty": 50,
    "license_type": "DEMO",
    "base_license": True,
    "creation_date": "2013-06-25T23:51:09.826Z",
    "activated_date": "2013-06-22T23:51:09.826Z",
    "expiry_date": "2023-06-25T23:51:09.826Z",
    "license_status": "INACTIVE",
    "deactivated_key": "SOME LICKEY"
}

APP = {
    "uid": "com.hp.cloud",
    "version": "01.11.00.2342",
    "vendor": "Hewlett-Packard",
    "name": "Cloud Controller",
    "desc": "Cloud Network Controller",
    "state": "INSTALLED",
    "deployed": "2013-05-23T10:09:08.000Z"
}

APP_HEALTH = {
    "deployed": "2013-10-16T21:15:10.922Z",
    "name": "Topology Viewer",
    "state": "ACTIVE",
    "status": "OK",
    "uid": "com.hp.sdn.tvue"
}

AUDIT_LOG = {
    "uid": "730d99ee-78f9-4301-ab2b-7871df61a6d3",
    "system_uid": "a1adf6a0-13d3-45de-bf66-acc504e84dba",
    "user": "sdn",
    "ts": "2013-06-05T17:54:19.265Z",
    "activity": "Artifact Management - Upload",
    "description": "geewiz-apps-1.0.0.jar has been staged"
}

SYSTEM = {
    "uid": "adc5e492-957c-4f8c-aa0a-97fa2dac5f23",
    "version": "01.11.00.0000",
    "role": "leader",
    "core_data_version": 0,
    "core_data_version_timestamp": "1970-01-01T00:00:00.000Z",
    "time": "1970-01-01T00:00:00.000Z",
    "self": True,
    "status": "active"
}

REGION = {
    "uid": "adc5e492-957c-4f8c-aa0a-97fa2dac5f01",
    "master": {
        "ip": "125.200.104.101",
        "name": "Controller_1"
    },
    "slaves": [
        {
            "ip": "125.200.104.102",
            "name": "Controller_2"
        }
    ],
    "devices": [
        {
            "ip": "125.200.104.200"
        }
    ]
}

TEAM = {
    "name": "Test Cluster",
    "ip": "192.168.139.111",
    "version": "1374169868918",
    "systems": [
        {
            "name": "member 1",
            "ip": "192.168.139.101",
            "priority": 10
        },
        {
            "name": "member 2",
            "ip": "192.168.139.102",
            "priority": 20
        },
        {
            "name": "member 3",
            "ip": "192.168.139.103",
            "priority": 30
        }
    ]
}

ALERT = {
    "desc": "Some description",
    "org": "TeamingManager",
    "sev": "INFO",
    "state": True,
    "system_uid": "669aa151-2790-4cb0-9656-75e9651893ee",
    "topic": "teaming",
    "ts": "2013-10-16T21:14:29.704Z",
    "uid": "2237dab8-c5e0-4a43-83ba-60b318741450"
}

ALERT_TOPIC = {
    "desc": "Alerts associated with license compliance",
    "org": "compliance-manager",
    "topic": "licensing"
}

ALERT_TOPIC_LISTENER = {
    "uid": "cb0f4bf2-a8f5-4b06-8937-abfc79d33423",
    "app_id": "imc",
    "name": "IMC OpenFLow Listener",
    "callbacks": [
        {
            "topics": [
                "of_controller",
                "of_controller_link"
            ],
            "uri": "http://imc.h3c.com/sdn"
        }
    ]
}

METRIC_APP = {
    "app_id": "com.hp.sdn.cloud",
    "app_name": "HP VAN SDN Cloud Controller",
}

METRIC = {
    "name": "Metric A",
    "type": "COUNTER",
    "uid": "65f1a180-ab5e-4b41-8c9f-b1597a4d1200",
    "primary_tag": "router1",
    "secondary_tag": "port1",
    "jmx": True,
    "persistence": True,
    "summary_interval": "ONE"
}

METRIC_VALUES = {
    "type": "COUNTER",
    "uid": "95ac45f3-75d2-49ff-a815-d6b780dc4e98",
    "datapoint_count": 1,
    "datapoints": [
        {
            "count": "43",
            "milliseconds_span": "58",
            "update_time": "Mon Aug 19 15:02:41 PDT 2013"
        }
    ]
}

CONTROLLER_STATS = {
    "duration_ms": 8413750,
    "lost": {
        "bytes": 0,
        "packets": 0
    },
    "msg_in": 3178,
    "msg_out": 1594,
    "packet_in": {
        "bytes": 0,
        "packets": 0
    },
    "packet_out": {
        "bytes": 38920,
        "packets": 556
    },
    "uid": "aa079dc9-b9ec-4e15-a2ee-b753c2d02397"
}

STATS = {
    "dpid": "00:64:74:46:a0:ff:07:00",
    "port_stats": [
        {
            "collisions": 0,
            "duration_nsec": 4294967295,
            "duration_sec": 4294967295,
            "port_id": 24,
            "rx_bytes": 86162,
            "rx_crc_err": 0,
            "rx_dropped": 0,
            "rx_errors": 0,
            "rx_frame_err": 0,
            "rx_over_err": 0,
            "rx_packets": 860,
            "tx_bytes": 204628,
            "tx_dropped": 0,
            "tx_errors": 0,
            "tx_packets": 1594
        }
    ]
}

PORT_STATS = {
    "collisions": 0,
    "duration_nsec": 4294967295,
    "duration_sec": 4294967295,
    "port_id": 24,
    "rx_bytes": 86162,
    "rx_crc_err": 0,
    "rx_dropped": 0,
    "rx_errors": 0,
    "rx_frame_err": 0,
    "rx_over_err": 0,
    "rx_packets": 860,
    "tx_bytes": 204628,
    "tx_dropped": 0,
    "tx_errors": 0,
    "tx_packets": 1594
}

GROUP_STATS = {
    "id": 121,
    "ref_count": 0,
    "packet_count": 0,
    "byte_count": 0,
    "duration_sec": 30,
    "duration_nsec": 773000000,
    "bucket_stats": [
        {
            "packet_count": 0,
            "byte_count": 0
        }
    ]
}

METER_STATS = {
    "band_stats": [
        {
            "byte_count": 0,
            "packet_count": 0
        },
        {
            "byte_count": 0,
            "packet_count": 0
        }
    ],
    "byte_count": 0,
    "duration_nsec": 3801967296,
    "duration_sec": 3664433282,
    "flow_count": 0,
    "id": 1,
    "packet_count": 0
}

DATAPATH = {
    "capabilities": [
        "flow_stats",
        "table_stats",
        "port_stats",
        "group_stats",
        "port_blocked"
    ],
    "device_ip": "140.1.1.1",
    "device_port": 62075,
    "dpid": "00:64:74:46:a0:ff:07:00",
    "last_message": "2013-10-16T23:54:35.576Z",
    "negotiated_version": "1.3.0",
    "num_buffers": 0,
    "num_tables": 3,
    "ready": "2013-10-16T21:17:02.652Z"
}

METER_FEATURES = {
    "flags": [
        "kbps",
        "pktps",
        "stats"
    ],
    "max_bands_per_meter": 2,
    "max_color_value": 8,
    "max_meters": 126,
    "types": [
        "drop"
    ]
}

GROUP_FEATURES = {
    "actions": [
        {
            "all": [
                "output"
            ]
        },
        {
            "select": [
                "output"
            ]
        }
    ],
    "capabilities": [
        "select_liveness"
    ],
    "max_groups": [
        {
            "all": 32
        },
        {
            "select": 32
        }
    ],
    "types": [
        "all",
        "select"
    ]
}

PORT = {
    "advertised_features": [],
    "config": [],
    "current_features": [
        "rate_1gb_fd",
        "rate_1tb_fd"
    ],
    "current_speed": 3567587328,
    "id": 24,
    "mac": "74:46:a0:ff:07:28",
    "max_speed": 3567587328,
    "name": "24",
    "peer_features": [],
    "state": [
        "live"
    ],
    "supported_features": [
        "rate_10mb_hd",
        "rate_10mb_fd",
        "rate_100mb_hd",
        "rate_100mb_fd",
        "rate_1gb_fd",
        "rate_1tb_fd"
    ]
}

METER = {
    "bands": [
        {
            "burst_size": 1000,
            "mtype": "drop",
            "rate": 1500
        },
        {
            "burst_size": 1000,
            "mtype": "dscp_remark",
            "prec_level": 1,
            "rate": 100
        }
    ],
    "flags": [
        "kbps",
        "burst",
        "stats"
    ],
    "id": 1
}

GROUP = {
    "buckets": [
        {
            "actions": [
                {
                    "output": 24
                }
            ],
            "watch_group": 4294967295,
            "watch_port": 4294967295,
            "weight": 0
        }
    ],
    "id": 1,
    "type": "all"
}

FLOW = {
    "duration_sec": 66,
    "duration_nsec": 825000000,
    "priority": 29999,
    "idle_timeout": 300,
    "hard_timeout": 0,
    "cookie": "0x2328",
    "packet_count": 2,
    "byte_count": 140,
    "match": [
        {
            "in_port": 3
        },
        {
            "eth_src": "be:f9:8c:b6:5b:9c"
        },
        {
            "eth_dst": "fe:b4:08:c5:23:fc"
        }
    ],
    "actions": [
        {
            "output": 2
        }
    ]
}

FLOW_MA = {
    "duration_sec": 66,
    "duration_nsec": 825000000,
    "priority": 29999,
    "idle_timeout": 300,
    "hard_timeout": 0,
    "cookie": "0x2328",
    "packet_count": 2,
    "byte_count": 140,
    "match": [
        {
            "in_port": 3
        },
        {
            "eth_src": "be:f9:8c:b6:5b:9c"
        },
        {
            "eth_dst": "fe:b4:08:c5:23:fc"
        }
    ],
    "actions": [
        {
            "output": 1
        },
        {
            "output": 2
        },
        {
            "output": 3
        }
    ]
}

CLUSTER = {
    "uid": "172334323",
    "links": [
        {
            "src_dpid": "00:00:00:00:00:00:00:02",
            "src_port": 3,
            "dst_dpid": "00:00:00:00:00:00:00:03",
            "dst_port": 5
        }
    ]
}

LINK = {
    "src_dpid": "00:00:00:00:00:00:00:02",
    "src_port": 3,
    "dst_dpid": "00:00:00:00:00:00:00:03",
    "dst_port": 5
}

PATH = {
    "cost": 3,
    "links": [
        {
            "src_dpid": "00:00:00:00:00:00:00:02",
            "src_port": 3,
            "dst_dpid": "00:00:00:00:00:00:00:03",
            "dst_port": 5
        }
    ]
}

ARP = {
    "ip": "10.0.0.3",
    "mac": "a2:c0:98:8e:ec:4a",
    "vid": 3
}

NODE = {
    "ip": "10.0.0.6",
    "mac": "a2:c0:98:8e:ec:4a",
    "dpid": "00:00:00:00:00:00:00:02",
    "port": 3,
    "vid": 3
}

LLDP = {
    "dpid": "00:00:00:00:00:00:00:02",
    "ports": [3, 5, 7]
}

OBSERVATION = {
    "dpid": "00:00:00:00:00:00:00:01",
    "type": "TCP",
    "packet_uid": "1",
    "status": "OK"
}

PACKET = {
    "uid": "1",
    "eth": {
        "eth_src": "01:01:01:01:01:01",
        "eth_dst": "02:02:02:02:02:02",
        "eth_type": "0x0800(IPv4)",
        "vlan_vid": "100",
        "vlan_priority": "PRIORITY_5"
    },
    "ip": {
        "ipv4_dst": "10.0.100.102",
        "ipv4_src": "10.0.100.101",
        "ip_proto": "TCP",
        "ip_dscn": "CS0",
        "ip_scn": "NOT_ECT"
    },
    "tcp": {
        "tcp_dst": 80,
        "tcp_src": 12345
    }
}

NEXT_HOP = {
    "dpid": "00:00:00:00:00:00:00:03",
    "port": 3
}

INVALID_JSON = '{"message": "Invalid JSON format: Failed to deserialize ping. Please refer to the HP VAN SDN Controller JSON schema for more information."}'

ILLEGAL_ARG = '{"error" : "java.lang.IllegalArgumentException", "message" : "v1.0 SET_QUEUE should use createAction(pv,SET_QUEUE,queueId,port)"}'

VERSION_MISMATCH = '{ "error": "com.hp.of.lib.VersionMismatchException", "message": "Not supported before version 1.3"}'

NOTFOUND = '{"error": "com.hp.api.NotFoundException", "message": "No such device: 00:00:00:00:00:00:00:01"}'

ILLEGAL_STATE = '{"error": "java.lang.IllegalStateException", "message": "{ofm:[V_1_3,ERROR,36,410271],BAD_REQUEST/BAD_TYPE,#dataBytes=24,OFM-cause:[V_1_3,MULTIPART_REQUEST,24,410271]}"}'

AUTH = ('{"record":{"token":"6dea10bebf074ec3bc2b641535e04'
        'f04","expiration":1385824487000,"expirationDate":'
        '"2013-11-30 07-14-47 -0800","userId":"cb35f95f8a0'
        '14501bf5b6a94e7813e7b","userName":"sdn","domainId'
        '":"","domainName":""}}')








