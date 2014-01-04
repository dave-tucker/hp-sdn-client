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

import json
import urllib

from hpsdnclient.api import ApiBase
from hpsdnclient.error import raise_errors

class NetMixin(ApiBase):

    def __init__(self, controller, auth):
        super(NetMixin, self).__init__(controller, auth)
        self._net_base_url = ("https://{0}:8443".format(self.controller) +
                             "/sdn/v2.0/net/")

    def get_clusters(self):
        """ Gets a list of clusters """
        url = self._net_base_url + 'clusters'
        return self.restclient.get(url)

    def get_cluster_tree(self, cluster_id):
        """ Gets the broadcast tree for a specific cluster """
        url = self._net_base_url + 'clusters/{0}/tree'.format(cluster_id)
        return self.restclient.get(url)

    def get_links(self, dpid=None):
        """ Returns a list of all links discovered by the SDN controller """
        url = self._net_base_url + 'links'
        if dpid:
            url = url + '?dpid={0}'.format(urllib.quote(dpid))
        return self.restclient.get(url)

    def get_forward_path(self, src_dpid, dst_dpid):
        """ Gets the shortest computed path between src_dpid and dst_dpid """
        url = (self._net_base_url +
               'paths/forward' +
               '?src_dpid={0}&dst_dpid={1}'.format(urllib.quote(src_dpid),
                                                   urllib.quote(dst_dpid)))
        return self.restclient.get(url)

    def get_arps(self, vid=None, ip=None):
        """ Provides ARP details for the given IP address and VLAN ID """
        url = self._net_base_url + 'arps'

        if vid and not ip:
            url = url + "?vid={0}".format(vid, ip)
        elif vid and ip:
            url = url + "?vid={0}&ip={1}".format(vid, ip)

        return self.restclient.get(url)

    def get_nodes(self, ip=None, vid=None, dpid=None, port=None):
        """ Provides the end node detail for the given IP address and VID
            Provides the end node list for a given VID
            Provides the end node list for a given datapath ID
            Provides the end node list for a given datapath ID and port
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

    def get_lldp(self):
        """ get_lldp()

            Gets a list of LLDP supressed ports from the SDN Controller

        """
        url = self._net_base_url + 'lldp'
        return self.restclient.get(url)

    def set_lldp(self, ports):
        """ Puts selected ports in to LLDP suppressed state """
        url = self._net_base_url + 'lldp'
        r = self.restclient.post(url, json.dumps(ports))
        raise_errors(r)

    def delete_lldp(self, ports):
        """ Removes ports from LLDP suppressed state """
        url = self._net_base_url + 'lldp'
        r = self.restclient.delete(url, json.dumps(ports))
        raise_errors(r)

    def get_diag_observations(self, packet_uid=None, packet_type=None):
        """ Gets a list of diagnostic observation posts"""
        url = self._net_base_url + 'diag/observations'
        if packet_uid:
            url += '?packet_uid={}'.format(packet_uid)
        if packet_type:
            url += '?packet_type={}'.format(packet_type)
        return self.restclient.get(url)

    def set_diag_observations(self, observation):
        """ Creates a diagnostic observation post """
        url = self._net_base_url + 'diag/observations'
        r = self.restclient.post(url, json.dumps(observation))
        raise_errors(r)

    def delete_diag_observations(self, observation):
        """ Delete a diagnostic observation post """
        url = self._net_base_url + 'diag/observations'
        r = self.restclient.delete(url, json.dumps(observation))
        raise_errors(r)

    def get_diag_packets(self, packet_type=None):
        """ Get a list of all diagnostic packets in the system """
        url = self._net_base_url + 'diag/packets'
        if packet_type:
            url += '?type{}'.format(packet_type)
        return self.restclient.get(url)

    def set_diag_packet(self, packet):
        """ Crate a diagnositc packet """
        url = self._net_base_url + 'diag/packets'
        r = self.restclient.post(url, json.dumps(packet))
        raise_errors(r)

    def delete_diag_packet(self, packet):
        """ Remove a diagnostic packet """
        url = self._net_base_url + 'diag/packets'
        r = self.restclient.delete(url, json.dumps(packet))
        raise_errors(r)

    def get_diag_packet(self, packet_uid):
        """ Get a specific diagnostic packet """
        url = self._net_base_url + 'diag/packets/{}'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_path(self, packet_uid):
        """ Get expected paths for diagnostic packet """
        url = self._net_base_url + 'diag/packets/{}/path'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_nexthop(self, packet_uid, dpid):
        """ Show next hop information for packet at a given dpid """
        url = self._net_base_url + 'diag/packets/{}/nexthop'.format(packet_uid)
        url += '?src_dpid={}'.format(dpid)
        return self.restclient.get(url)

    def set_diag_packet_action(self, packet_uid, action):
        """ Create a copy of the packet on the network """
        url = self._net_base_url + 'diag/packets/{}/action'.format(packet_uid)
        r = self.restclient.post(url, json.dumps(action))
        raise_errors(r)
