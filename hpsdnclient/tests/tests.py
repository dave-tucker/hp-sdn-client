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
    Here lies the unit tests for the hpsdnclient library

    In order to run these tests you must:
        - have the HP SDN Controller running
        - have a physical or MiniNet topology running
        - have traffic running across the network topology

    Before running these tests, update SDNCTL, USER and PASS

"""

import time
import unittest

import hpsdnclient as hp
from hpsdnclient import utils as utils

SDNCTL = '10.44.254.129'
USER = 'sdn'
PASS = 'skyline'
DPID = '00:00:00:00:00:00:00:02'

def setUpModule():
    pass

def tearDownModule():
    pass

class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        self.mac_string = '00:00:00:00:00:01'
        self.mac_hex = '0x1'
        self.dpid_string = '00:00:00:00:00:00:00:02'
        self.dpid_hex = '0x2'

    def tearDown(self):
        pass

    def test_mac_string_to_hex(self):
        tmp = utils.string_to_hex(self.mac_string, utils.MAC)
        self.assertEqual(tmp, self.mac_hex)

    def test_dpid_string_to_hex(self):
        tmp = utils.string_to_hex(self.dpid_string, utils.DPID)
        self.assertEqual(tmp, self.dpid_hex)

    def test_mac_hex_to_string(self):
        tmp = utils.hex_to_string(self.mac_hex, utils.MAC)
        self.assertEqual(tmp, self.mac_string)

    def test_dpid_hex_to_string(self):
        tmp = utils.hex_to_string(self.dpid_hex, utils.DPID)
        self.assertEqual(tmp, self.dpid_string)


class ApiBaseTest(unittest.TestCase):

    def setUp(self):
        self.api = hp.Api(controller=SDNCTL, user=USER, password=PASS)

    def tearDown(self):
        self.api = None

class OfTest(ApiBaseTest):

    def setUp(self):
        super(OfTest, self).setUp()

    def tearDown(self):
        super(OfTest, self).tearDown()

    def test_get_stats(self):
        data = self.api.get_stats()
        self.assertTrue(data)

    def test_get_port_stats(self):
        data = self.api.get_port_stats(DPID, 1)
        self.assertTrue(data)

    def test_get_group_stats(self):
        #need to create a group on an OF1.3 DPID
        pass

    def test_get_meter_stats(self):
        #need to create a meter on an OF1.3 DPID
        pass

    def test_get_datapaths(self):
        data = self.api.get_datapaths()
        self.assertTrue(data)
        
    def test_get_datapath_detail(self):
        data = self.api.get_datapath_detail(DPID)
        self.assertTrue(data)

    def test_get_datapath_meter_features(self):
        data = self.api.get_datapath_meter_features(DPID)
        #Not supported on OF1.0 devices
        self.assertRaises(hp.error.FlareApiError)

    def test_get_datapath_group_features(self):
        data = self.api.get_datapath_group_features(DPID)
        #Not supported on OF1.0 devices
        self.assertRaises(hp.error.FlareApiError)

    def test_get_ports(self):
        data = self.api.get_ports(DPID)
        self.assertTrue(data)

    def test_get_port_detail(self):
        data = self.api.get_port_detail(DPID, 1)
        self.assertTrue(data)
        
    def test_get_meters(self):
        #need to create a meter on an OF1.3 DPID
        pass

    def test_get_meter_details(self):
        #need to create a meter on an OF1.3 DPID
        pass
    
    def test_get_flows(self):
        data = self.api.get_flows(DPID)
        self.assertTrue(data)

    def test_get_groups(self):
        data = self.api.get_groups(DPID)
        self.assertRaises(hp.error.FlareApiError)
    
    def test_get_group_details(self):
        data = self.api.get_group_details(DPID, 1)
        self.assertRaises(hp.error.FlareApiError)

    def test_add_groups(self):
        group = hp.types.Group()
        data = self.api.add_groups(DPID, group)
        self.assertRaises(hp.error.FlareApiError)

    def test_add_flows(self):
        match = hp.types.Match(eth_type="ipv4",ipv4_src="10.0.0.1",ipv4_dst="10.0.0.22",ip_proto="tcp", tcp_dst="80")
        output6 = hp.types.Action(output=6)
        flow = hp.types.Flow(priority=30000, idle_timeout=30, match=match, actions=output6)
        self.assertTrue(self.api.add_flows(DPID, flow))
        self.assertTrue(flow in self.api.get_flows(DPID))

    def test_add_meters(self):
        meter = hp.types.Meter()
        data = self.api.add_meters(DPID, meter)
        self.assertRaises(hp.error.FlareApiError)
