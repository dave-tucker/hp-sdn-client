#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person
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

import unittest
from hpsdnclient import utils as utils

class TestUtils(unittest.TestCase):

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

