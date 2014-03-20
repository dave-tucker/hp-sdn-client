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

import json
import urllib

from hpsdnclient.api import ApiBase
from hpsdnclient.error import raise_errors
from hpsdnclient.datatypes import LldpProperties


class NetMixin(ApiBase):
    """Network Service REST API Methods

    This class contains methods that call the Network Services
    REST API functions in the HP VAN SDN Controller

    - Topology Service
    - Node Service
    - Link Service
    - Path Planner
    - Path Diagnostics Service

    """
    def __init__(self, controller, auth):
        super(NetMixin, self).__init__(controller, auth)
        self._net_base_url = ("https://{0}:8443".format(self.controller) +
                              "/sdn/v2.0/net/")
        self._diag_base_url = ("https://{0}:8443".format(self.controller) +
                               "/sdn/v2.0/diag/")

    def get_clusters(self):
        """ Gets a list of clusters

        :return: A list of clusters
        :rtype: list

        """
        url = self._net_base_url + 'clusters'
        return self.restclient.get(url)

    def get_cluster_broadcast_tree(self, cluster_id):
        """ Gets the broadcast tree for a specific cluster

        :param str cluster_id: The cluster ID
        :return: The broadcast tree for the provided cluster ID
        :rtype: hpsdnclient.datatypes.Cluster

        """
        url = self._net_base_url + 'clusters/{0}/tree'.format(cluster_id)
        return self.restclient.get(url)

    def get_links(self, dpid=None):
        """ Returns a list of all links discovered by the SDN controller

        :param str dpid: Return only the links for the specified DPID
        :return: A list of Links
        :rtype: list

        """
        url = self._net_base_url + 'links'
        if dpid:
            url = url + '?dpid={0}'.format(urllib.quote(dpid))
        return self.restclient.get(url)

    def get_forward_path(self, src_dpid, dst_dpid):
        """ Gets the shortest computed path between src_dpid and dst_dpid

        :param str src_dpid: The source DPID
        :param str dst_dpid: THe destination DPID
        :return: The shortest path between the two DPID's
        :rtype: hpsdnclient.datatypes.Path

        """
        url = (self._net_base_url +
               'paths/forward' +
               '?src_dpid={0}&dst_dpid={1}'.format(urllib.quote(src_dpid),
                                                   urllib.quote(dst_dpid)))
        return self.restclient.get(url)

    def get_arps(self, vid=None, ip=None):
        """ Provides ARP details for the given IP address and VLAN ID

        :param str vid: Return ARPs in the provided VLAN ID
        :param str ip: Return only the ARP for the specified IP Address
        :return: List of ARPs
        :rtype: list

        """
        url = self._net_base_url + 'arps'

        if vid and not ip:
            url = url + "?vid={0}".format(vid, ip)
        elif vid and ip:
            url = url + "?vid={0}&ip={1}".format(vid, ip)

        return self.restclient.get(url)

    def get_nodes(self, ip=None, vid=None, dpid=None, port=None):
        """ Get all Nodes discovered by the controller

        - With `ip`` and ``vid`` returns node details
        - With ``vid`` returns Nodes in the specified VLAN
        - With ``dpid`` returns Nodes attached to the specified DPID
        - With ``dpid`` and ``port`` returns Nodes for given port/DPID

        :param str ip: IP address
        :param str vid: VLAN ID
        :param str dpid: Datapath ID
        :param str port: Port

        """
        url = self._net_base_url + 'nodes'

        if vid and not ip:
            url += "?vid={0}".format(vid, ip)
        elif vid and ip:
            url += "?vid={0}&ip={1}".format(vid, ip)
        elif dpid and not port:
            url += "?dpid={0}".format(urllib.quote(dpid))
        elif dpid and port:
            url += "?dpid={0}&port={1}".format(urllib.quote(dpid), port)

        return self.restclient.get(url)

    def get_lldp_suppressed_ports(self):
        """ Gets a list of LLDP suppressed ports from the controller

        :return: A list of ports in the LLDP suppressed state
        :rtype: list

        """
        url = self._net_base_url + 'lldp'
        return self.restclient.get(url)

    def set_lldp_suppressed(self, ports):
        """ Puts the provided ports in to LLDP suppressed state

        :params str ports: The ports to be suppressed

        """
        if isinstance(ports, list):
            tmp = []
            for item in list:
                if isinstance(item, LldpProperties):
                    tmp.append(item.to_dict())
                else:
                    tmp.append(item)
            data = {"lldp_suppressed": tmp}

        else:
            data = {"lldp_suppressed": [ports.to_dict()]}

        url = self._net_base_url + 'lldp'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def remove_lldp_suppressed(self, ports):
        """ Removes ports from LLDP suppressed state

        :params hpsdnclient.datatypes.LldpProperties ports:
            The ports to be removed from LLDP suppressed state

        """

        if isinstance(ports, list):
            tmp = []
            for item in list:
                if isinstance(item, LldpProperties):
                    tmp.append(item.to_dict())
                else:
                    tmp.append(item)
            data = {"lldp_suppressed": tmp}

        else:
            data = {"lldp_suppressed": [ports.to_dict()]}
        url = self._net_base_url + 'lldp'
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

    def get_diag_observation_posts(self, packet_uid=None, packet_type=None):
        """ Gets a list of diagnostic observation posts

        :param str packet_uid: Only return OP's with the provided Packet UID
        :param str packet_type: Return only OP's with the provided Packet Type
        :return: List of OP's
        :rtype: list

        """
        url = self._diag_base_url + 'observations'
        if packet_uid:
            url += '?packet_uid={}'.format(packet_uid)
        if packet_type:
            url += '?packet_type={}'.format(packet_type)
        return self.restclient.get(url)

    def create_diag_observation_post(self, observation):
        """ Creates a diagnostic observation post

        :param hpsdnclient.datatypes.Observation observation:
            The observation post to create

        """
        data = {"observation": observation.to_dict()}
        url = self._diag_base_url + 'observations'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def delete_diag_observation_post(self, observation):
        """ Delete a diagnostic observation post

        :param str observation: The observation post to delete

        """
        data = {"observation": observation.to_dict()}
        url = self._diag_base_url + 'observations'
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

    def get_diag_packets(self, packet_type=None):
        """ Get a list of all diagnostic packets in the system

        :param packet_type: Filter result by provided packet type
        :return: A list of diagnostics packets
        :rtype: list

        """
        url = self._diag_base_url + 'packets'
        if packet_type:
            url += '?type{}'.format(packet_type)
        return self.restclient.get(url)

    def create_diag_packet(self, packet):
        """ Create a diagnostic packet

        :param str packet: The packet to create

        """
        data = {"packet": packet.to_dict()}
        url = self._diag_base_url + 'packets'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def delete_diag_packet(self, packet_uid):
        """ Delete a diagnostic packet

        :param str packet_uid: The uid of the packet to be deleted

        """
        url = self._diag_base_url + 'packets/{}'.format(packet_uid)
        r = self.restclient.delete(url)
        raise_errors(r)

    def get_diag_packet(self, packet_uid):
        """ Get diagnostic packet details for the provided packet UID

        :param str packet_uid: The packet UID to get details for
        :return: Diagnostic Packet Details
        :rtype: hpsdnclient.datatypes.Packet

        """
        url = self._diag_base_url + 'packets/{}'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_path(self, packet_uid):
        """ Get expected paths for diagnostic packet

        :param packet_uid: The UID of the diagnostic packet
        :return: Path
        :rtype: hpsdnclient.datatypes.Path

        """
        url = self._diag_base_url + 'packets/{}/path'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_nexthop(self, packet_uid, dpid):
        """ Show next hop information for packet at a given Datapath ID

        :param str packet_uid: The packet UID
        :param str dpid: The Datapath ID
        :returns: The next hop
        :rtype: hpsdnclient.datatypes.NextHop

        """
        url = self._diag_base_url + 'packets/{}/nexthops'.format(packet_uid)
        url += '?src_dpid={}'.format(dpid)
        return self.restclient.get(url)

    def set_diag_packet_action(self, packet_uid, action):
        """ Performs the specified simulation action on a packet

        :param str packet_uid: The packet UID
        :param str action: The action to perform

        """
        data = {"simulation": action}
        url = self._diag_base_url + 'packets/{}/action'.format(packet_uid)
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)
