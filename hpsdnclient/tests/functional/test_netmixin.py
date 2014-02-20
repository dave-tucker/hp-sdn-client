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

from hpsdnclient.tests.base import ApiTestCase
from hpsdnclient.datatypes import LldpProperties, Observation, Packet, Ethernet, Ip, Udp
import time

OF10_DPID = "00:00:00:00:00:00:00:03"

class TestNetMixin(ApiTestCase):

    def _create_diag_packet(self):
        eth = Ethernet(eth_src="00:00:00:00:00:0b", eth_dst="00:00:00:00:00:15",
                       eth_type="IPv4", vlan_pcp="PRIORITY_5")

        ip = Ip(ipv4_src="10.0.0.11", ipv4_dst="10.0.0.21", ip_proto="UDP",
                ip_dscp="CS0", ip_ecn="NOT_ECT")

        udp = Udp(udp_dst=152, udp_src=12345)

        packet = Packet(type="UDP", eth=eth, ip=ip, udp=udp)

        return packet

    def test_get_clusters(self):
        data = self.api.get_clusters()
        self.assertTrue(data)

    def test_get_cluster_broadcast_tree(self):
        data = self.api.get_cluster_broadcast_tree(1)
        self.assertTrue(data)

    def test_get_links(self):
        data = self.api.get_links()
        self.assertTrue(data)

    def test_get_forward_path(self):
        data = self.api.get_forward_path("00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:05")
        self.assertTrue(data)

    def test_get_arps(self):
        data = self.api.get_arps()
        self.assertTrue(data)

    def test_get_nodes(self):
        data = self.api.get_nodes()
        self.assertTrue(data)

    def test_get_set_and_delete_lldp_suppressed(self):
        lldp = LldpProperties(dpid=OF10_DPID, ports=[3,4,5])

        self.api.set_lldp_suppressed(lldp)

        self.assertTrue(lldp, self.api.get_lldp_suppressed_ports())

        self.api.remove_lldp_suppressed(lldp)

        self.assertEquals([], self.api.get_lldp_suppressed_ports())

    def test_get_create_and_delete_diag_observation_posts(self):

        packet = self._create_diag_packet()
        self.api.create_diag_packet(packet)

        packets = self.api.get_diag_packets()

        obs = Observation(dpid=OF10_DPID, packet_uid=packets[0].uid)
        self.api.create_diag_observation_post(obs)

        ops = self.api.get_diag_observation_posts()

        self.assertTrue(obs.dpid, ops[0].dpid)
        self.assertTrue(obs.packet_uid, ops[0].packet_uid)

        self.api.delete_diag_observation_post(obs)
        self.api.delete_diag_packet(packets[0].uid)
        self.assertEquals([], self.api.get_diag_observation_posts())

    def test_create_and_delete_diag_packets(self):

        packet = self._create_diag_packet()

        self.api.create_diag_packet(packet)

        remote_packet = self.api.get_diag_packets()
        #self.assertEquals(remote_packet[0].eth, packet.eth)
        self.assertEquals(remote_packet[0].ip, packet.ip)
        self.assertEquals(remote_packet[0].udp, packet.udp)

        self.api.delete_diag_packet(remote_packet[0].uid)
        time.sleep(2)
        self.assertEquals([], self.api.get_diag_packets())

    def test_get_diag_packet_path(self):

        packet = self._create_diag_packet()
        self.api.create_diag_packet(packet)

        packets = self.api.get_diag_packets()
        #ToDo: Return the UID of a resource when its created

        path = self.api.get_diag_packet_path(packets[0].uid)
        self.assertTrue(path)

        self.api.delete_diag_packet(packets[0].uid)

    def test_get_diag_packet_nexthop(self):

        packet = self._create_diag_packet()
        self.api.create_diag_packet(packet)

        packets = self.api.get_diag_packets()

        path = self.api.get_diag_packet_nexthop(packets[0].uid, OF10_DPID)
        self.assertTrue(path)

        self.api.delete_diag_packet(packets[0].uid)

    def test_set_diag_packet_action(self):

        packet = self._create_diag_packet()
        self.api.create_diag_packet(packet)

        packets = self.api.get_diag_packets()

        simulation = {"dpid": "00:00:00:00:00:00:00:03", "out_port": "7" }

        self.api.set_diag_packet_action(packets[0].uid, simulation)

        self.api.delete_diag_packet(packets[0].uid)
