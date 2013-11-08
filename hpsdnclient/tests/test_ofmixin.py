#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from hpsdnclient.tests.base import ApiBaseTest
from hpsdnclient.error import OpenflowProtocolError, VersionMismatch, NotFound
import hpsdnclient.datatypes

OF10_DPID = '00:00:00:00:00:00:00:0b'
OF13_DPID = '00:00:00:00:00:00:00:02'

class TestOfMixin10(ApiBaseTest):

    def setUp(self):
        super(TestOfMixin10, self).setUp()

    def tearDown(self):
        super(TestOfMixin10, self).tearDown()

    def _flow_exists(self, flow):
        match_fields = ['eth_type', 'ipv4_src', 'ipv4_dst',
                        'ip_proto', 'tcp_dst']
        action_fields = ['output']

        for f in self._api.get_flows(OF10_DPID):
            for m in match_fields:
                if not (flow.match.__getattribute__(m) ==
                        f.match.__getattribute__(m)):
                    break
            for a in action_fields:
                if not (flow.actions.__getattribute__(a) ==
                        f.actions.__getattribute__(a)):
                    break
            return True

    def test_get_stats(self):
        data = self._api.get_stats()
        self.assertTrue(data)

    def test_get_port_stats(self):
        data = self._api.get_port_stats(OF10_DPID, 1)
        self.assertTrue(data)

    def test_get_group_stats(self):
        self.assertRaises(VersionMismatch, self._api.get_group_stats,
                          OF10_DPID, 1)

    def test_get_meter_stats(self):
        self.assertRaises(NotFound, self._api.get_meter_stats,
                          OF10_DPID, 1)

    def test_get_datapaths(self):
        data = self._api.get_datapaths()
        self.assertTrue(data)

    def test_get_datapath_detail(self):
        data = self._api.get_datapath_detail(OF10_DPID)
        self.assertTrue(data)

    def test_get_datapath_meter_features(self):
        self.assertRaises(NotFound,
                          self._api.get_datapath_meter_features, OF10_DPID)

    def test_get_datapath_group_features(self):
        self.assertRaises(VersionMismatch,
                          self._api.get_datapath_group_features, OF10_DPID)

    def test_get_ports(self):
        data = self._api.get_ports(OF10_DPID)
        self.assertTrue(data)

    def test_get_port_detail(self):
        data = self._api.get_port_detail(OF10_DPID, 1)
        self.assertTrue(data)

    def test_get_meters(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_meters, OF10_DPID)

    def test_get_meter_details(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_meter_details,
                          OF10_DPID, 1)

    def test_get_flows(self):
        data = self._api.get_flows(OF10_DPID)
        self.assertTrue(data)


    def test_get_groups(self):
        self.assertRaises(VersionMismatch, self._api.get_groups, OF10_DPID)

    def test_get_group_details(self):
        self.assertRaises(VersionMismatch,
                          self._api.get_group_details,
                          OF10_DPID, 1)

    def test_add_groups(self):
        group = hpsdnclient.datatypes.Group()
        self.assertRaises(VersionMismatch, self._api.add_groups,
                          OF10_DPID, group)

    def test_add_flows(self):
        match = hpsdnclient.datatypes.Match(eth_type="ipv4",
                                            ipv4_src="10.0.0.1",
                                            ipv4_dst="10.0.0.22",
                                            ip_proto="tcp",
                                            tcp_dst="80")
        output6 = hpsdnclient.datatypes.Action(output=6)
        flow = hpsdnclient.datatypes.Flow(priority=30000, idle_timeout=30,
                             match=match, actions=output6)
        self._api.add_flows(OF10_DPID, flow)
        self.assertTrue(self._flow_exists(flow))

    def test_add_meters(self):
        meter = hpsdnclient.datatypes.Meter()
        self.assertRaises(VersionMismatch, self._api.add_meters,
                          OF10_DPID, meter)

class TestOfMixin13(ApiBaseTest):

    def setUp(self):
        super(TestOfMixin13, self).setUp()

    def tearDown(self):
        super(TestOfMixin13, self).tearDown()

    def _flow_exists(self, flow):
        match_fields = ['eth_type', 'ipv4_src', 'ipv4_dst',
                        'ip_proto', 'tcp_dst']
        action_fields = ['output']

        for f in self._api.get_flows(OF10_DPID):
            for m in match_fields:
                if not (flow.match.__getattribute__(m) ==
                        f.match.__getattribute__(m)):
                    break
            for a in action_fields:
                if not (flow.actions.__getattribute__(a) ==
                        f.actions.__getattribute__(a)):
                    break
            return True

    def test_get_stats(self):
        data = self._api.get_stats()
        self.assertTrue(data)

    def test_get_port_stats(self):
        data = self._api.get_port_stats(OF13_DPID, 1)
        self.assertTrue(data)

    def test_get_group_stats(self):
        self.assertRaises(OpenflowProtocolError, self._api.get_group_stats,
                          OF13_DPID, 1)

    def test_get_meter_stats(self):
        self.assertRaises(NotFound, self._api.get_meter_stats,
                          OF13_DPID, 1)

    def test_get_datapaths(self):
        data = self._api.get_datapaths()
        self.assertTrue(data)

    def test_get_datapath_detail(self):
        data = self._api.get_datapath_detail(OF13_DPID)
        self.assertTrue(data)

    def test_get_datapath_meter_features(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_datapath_meter_features, OF13_DPID)

    def test_get_datapath_group_features(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_datapath_group_features, OF13_DPID)

    def test_get_ports(self):
        data = self._api.get_ports(OF13_DPID)
        self.assertTrue(data)

    def test_get_port_detail(self):
        data = self._api.get_port_detail(OF13_DPID, 1)
        self.assertTrue(data)

    def test_get_meters(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_meters, OF13_DPID)

    def test_get_meter_details(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_meter_details,
                          OF13_DPID, 1)

    def test_get_flows(self):
        data = self._api.get_flows(OF13_DPID)
        self.assertTrue(data)


    def test_get_groups(self):
        self.assertRaises(OpenflowProtocolError, self._api.get_groups, OF13_DPID)

    def test_get_group_details(self):
        self.assertRaises(OpenflowProtocolError,
                          self._api.get_group_details,
                          OF13_DPID, 1)

    def test_add_groups(self):
        group = hpsdnclient.datatypes.Group(id="1", type="select")
        self.assertRaises(VersionMismatch, self._api.add_groups,
                          OF13_DPID, group)

    def test_add_flows(self):
        match = hpsdnclient.datatypes.Match(eth_type="ipv4",
                                            ipv4_src="10.0.0.1",
                                            ipv4_dst="10.0.0.22",
                                            ip_proto="tcp",
                                            tcp_dst="80")
        output6 = hpsdnclient.datatypes.Action(output=6)
        flow = hpsdnclient.datatypes.Flow(priority=30000, idle_timeout=30,
                             match=match, actions=output6)
        self._api.add_flows(OF13_DPID, flow)
        self.assertTrue(self._flow_exists(flow))

    def test_add_meters(self):
        meter = hpsdnclient.datatypes.Meter()
        self.assertRaises(VersionMismatch, self._api.add_meters,
                          OF13_DPID, meter)
