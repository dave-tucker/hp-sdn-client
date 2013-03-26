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

import time
import unittest

import hpsdnclient.hpsdnclient as f
import hpsdnclient.utils as utils
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topolib import TreeTopo

FLARE_IP = '10.211.55.12'
BASE_URL = 'http://{}:8080/sdn/v1.0'.format(FLARE_IP)

net = None

def setUpModule():
        topo = utils.Tree(k=3)
        global net
        net = Mininet(controller=lambda name: RemoteController('flare', FLARE_IP, 6633), 
                      switch = OVSKernelSwitch,
                      topo=topo,
                      xterms=False)
        net.start()
        time.sleep(30)
        net.pingAll()

def tearDownModule():
        global net
        net.stop()


class FakeFlow(f.Flow):
    def __init__(self):
        super(FakeFlow, self).__init__(dpid = utils.hex_to_string('0x1',utils.DPID), 
                                       in_port = '1', 
                                       src_mac = utils.hex_to_string('0x1000',utils.MAC),
                                       dst_mac = utils.hex_to_string('0x2000',utils.MAC), 
                                       src_ip = '10.10.10.1', 
                                       dst_ip = '10.10.10.2', 
                                       action = 'null', 
                                       multiple_actions = 'output=2')


class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        self.MAC_string = '00:00:00:00:00:01'
        self.MAC_hex = '0x1'
        self.DPID_string = '00:00:00:00:00:00:00:02'
        self.DPID_hex = '0x2'

    def tearDown(self):
        pass

    def test_mac_string_to_hex(self):
        tmp = utils.string_to_hex(self.MAC_string, utils.MAC)
        self.assertEqual(tmp, self.MAC_hex)

    def test_dpid_string_to_hex(self):
        tmp = utils.string_to_hex(self.DPID_string, utils.DPID)
        self.assertEqual(tmp, self.DPID_hex)

    def test_mac_hex_to_string(self):
        tmp = utils.hex_to_string(self.MAC_hex, utils.MAC)
        self.assertEqual(tmp, self.MAC_string)

    def test_dpid_hex_to_string(self):
        tmp = utils.hex_to_string(self.DPID_hex, utils.DPID)
        self.assertEqual(tmp, self.DPID_string)


class FlareApiBaseTest(unittest.TestCase):

    def setUp(self):
        self.api = f.Api(base_url = BASE_URL)

    def tearDown(self):
        self.api = None

class TestApiDevices(FlareApiBaseTest):

    def test_get_devices(self):
        pass

    def test_get_flow(self):
        r = self.api.get_flows_by_dpid(utils.hex_to_string('0x1', utils.DPID))
        for record in r:
            self.assertTrue(record.dpid)
            self.assertTrue(record.in_port)
            self.assertTrue(record.src_mac)

    def test_create_flow(self):
        flow = FakeFlow()
        self.assertTrue(self.api.create_flow(utils.hex_to_string('0x1', utils.DPID), flow))

        r = self.api.get_flows_by_dpid(utils.hex_to_string('0x1', utils.DPID))
        f1 = flow
        self.assertEqual(r[0].dpid, flow.dpid)
        self.assertEqual(r[0].in_port, flow.in_port)
        self.assertEqual(r[0].src_mac, flow.src_mac)
        self.assertEqual(r[0].dst_mac, flow.dst_mac)
        self.assertEqual(r[0].action, flow.action)
        self.assertEqual(r[0].multiple_actions, flow.multiple_actions)

    def test_update_flow(self):
        flow = FakeFlow()
        self.test_create_flow()

        flow.network_tos = '46'
        self.assertTrue(self.api.update_flow(utils.hex_to_string('0x1', utils.DPID), flow))

        r = self.api.get_flows_by_dpid(utils.hex_to_string('0x1', utils.DPID))
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

