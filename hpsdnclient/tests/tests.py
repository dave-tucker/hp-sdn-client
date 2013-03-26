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

"""Here lies the unit tests for the hpsdnclient library"""

import unittest

import hpsdnclient.hpsdnclient as f
import hpsdnclient.utils
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch

FLARE_IP = '10.211.55.12'
BASE_URL = 'http://{}:8080/sdn/v1.0'.format(FLARE_IP)

class TestPackage():
    def setUpModule():
            tree = FatTree(k=3)
            self.net = Mininet( controller=lambda name: RemoteController('flare', FLARE_IP, 6633), switch = OVSKernelSwitch, topo=tree, xterms=terms)
            self.net.start()
            self.net.pingall()
    def tearDownModule():
            self.net.stop()

class FakeFlow(f.Flow):
    def __init__(self):
        super(FakeFlow, self).__init__(dpid = f.hex_to_string('0x1',f.DPID), 
                                       in_port = 1, 
                                       src_mac = f.hex_to_string('0x1000',f.MAC),
                                       dst_mac = f.hex_to_string('0x2000',f.MAC), 
                                       src_ip = '10.10.10.1', 
                                       dst_ip = '10.10.10.2', 
                                       action = 'null', 
                                       multiple_actions = 'output=2')

class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        self.mac_string = '00:00:00:00:00:01'
        self.mac_hex = '0x1'
        self.dpid_string = '00:00:00:00:00:00:00:02'
        self.dpid_hex = '0x2'

    def tearDown(self):
        pass

    def test_mac_string_to_hex(self):
        tmp = f.string_to_hex(self.mac_string, f.MAC)
        self.assertEqual(tmp, self.mac_hex)

    def test_dpid_string_to_hex(self):
        tmp = f.string_to_hex(self.dpid_string, f.DPID)
        self.assertEqual(tmp, self.dpid_hex)

    def test_mac_hex_to_string(self):
        tmp = f.hex_to_string(self.mac_hex, f.MAC)
        self.assertEqual(tmp, self.mac_string)

    def test_dpid_hex_to_string(self):
        tmp = f.hex_to_string(self.dpid_hex, f.DPID)
        self.assertEqual(tmp, self.dpid_string)

class FlareApiBaseTest(unittest.TestCase):

    def setUp(self):
        self.api = f.Api(base_url = BASE_URL)

    def tearDown(self):
        self.api = None
        self.net.stop()

class TestApiDevices(FlareApiBaseTest):

    def test_get_devices(self):
        pass

    def test_get_flow(self):
        self.assertFalse(self.api.get_flows_by_dpid(f.hex_to_string('0x1', f.DPID))) 

    def test_create_flow(self):
        flow = FakeFlow()
        self.assertTrue(self.api.create_flow(f.hex_to_string('0x1', f.DPID), flow))

        r = self.api.get_flows_by_dpid(f.hex_to_string('0x1', f.DPID))
        self.assertEqual(r[0].dpid, flow.dpid)
        self.assertEqual(r[0].in_port, flow.in_port)
        self.assertEqual(r[0].src_mac, flow.src_mac)
        self.assertEqual(r[0].dst_mac, flow.dst_mac)
        self.assertEqual(r[0].action, flow.action)
        self.assertEqual(r[0].multiple_actions, flow.multiple_actions)

    def test_update_flow(self):
        flow = FakeFlow()
        self.test_create_flow()

        flow.network_tos = 46
        self.assertTrue(self.api.update_flow(f.hex_to_string('0x1', f.DPID), flow))

        r = self.api.get_flows_by_dpid(f.hex_to_string('0x1', f.DPID))
        self.assertEqual(r[0].network_tos, flow.network_tos)

    def test_delete_flow(self):
        flow = FakeFlow()
        self.test_create_flow()

        self.assertTrue(self.api.delete_flow(flow))

class TestApiLimiters(FlareApiBaseTest):

    def test_get_limiters(self):
        pass

    def test_create_limters(self):
        pass

    def test_update_limiters(self):
        pass

    def test_delete_limiters(self):
        pass

