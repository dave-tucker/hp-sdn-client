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

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch

MAC = 12
DPID = 16

def string_to_hex(s, length):
    """ Convert a string like 00:00 in to hex 0x0000 format"""
    tmp = '{0:#x}'.format(int(s.replace(':', '').lstrip('0'),length))
    return tmp

def hex_to_string(h, length):
    """Convert a hex number from 0x0000 to 00:00 format"""
    tmp = h.lstrip('0x').zfill(length)
    tmp = ':'.join(a+b for a,b in zip(tmp[::2], tmp[1::2]))
    return tmp

class Tree(object):
    """ Create a tree topology from semi-scratch in Mininet """

    def __init__(self, cname='flare', cip='127.0.0.1', k=2):
        """Create tree topology for mininet
            cname: controller name
            cip: controller ip
        	k: number of leaf switches (and hosts)
        """

        self.flare =  RemoteController(cname, cip, 6633)
        self.net = Mininet(controller=self.flare, switch = OVSKernelSwitch, build=False )

        self.spine = self.net.addSwitch('s0')
        self.leaves = []
        self.hosts = []
        i = 1
        while i <= k:
            #list item is i-1
            j = i-1
            self.leaves.append(self.net.addSwitch('s%s' %i))
            self.hosts.append(self.net.addHost('h%s' %i))
            self.net.addLink(self.hosts[j], self.leaves[j])
            self.net.addLink(self.leaves[j], self.spine)
            i+=1

    def run(self):
        """ Runs the created network topology and launches mininet cli"""
        self.run_silent()
        CLI(self.net)
        self.net.stop()

    def run_silent(self):
        """ Runs silently - for unit testing """
        self.net.build()
        self.spine.start([self.flare])
        for leaf in self.leaves:
            leaf.start([self.flare])

    def pingAll(self):
        """ PingAll to create flows - for unit testing """
        self.net.pingAll()

    def stop(self):
        "Stops the topology. You should call this after run_silent"
        self.net.stop()

class DoubleTree(Tree):
    """Create a Tree Topology in Mininet with two links between leaf and spine"""

    def __init__(self, k=2, **opts):
        super(DoubleTree, self).__init__(k=k, **opts)
        i = 1
        while i <= k:
            j = i-1
            self.net.addLink(self.leaves[j], self.spine)
            i+=1

class Tower(object):
    """ Create a tower topology from semi-scratch in Mininet """

    def __init__(self, cname='flare', cip='127.0.0.1', k=4, h=6):
        """Create tower topology for mininet
            cname: controller name
            cip: controller ip
            k: number of leaf switches
            h: number of hosts perl leaf switch
        """

        self.flare =  RemoteController(cname, cip, 6633)
        self.net = Mininet(controller=self.flare, switch = OVSKernelSwitch, build=False )

        # Create the two spine switches
        self.spine_a = self.net.addSwitch('s1')
        self.spine_b = self.net.addSwitch('s2')

        # Create two links between the spine switches
        self.net.addLink(self.spine_a, self.spine_b)
        self.net.addLink(self.spine_b, self.spine_a)

        self.leaves = []
        self.hosts = []

        # Now create the leaf switches, their hosts and connect them together
        i = 1
        c = 0
        while i <= k:
            self.leaves.append(self.net.addSwitch('s1%s' % i))
            self.net.addLink(self.leaves[i-1], self.spine_a)
            self.net.addLink(self.leaves[i-1], self.spine_b)

            j = 1
            while j <= h:
                self.hosts.append(self.net.addHost('h%s%s' % (i, j)))
                self.net.addLink(self.hosts[c], self.leaves[i-1])
                j+=1
                c+=1

            i+=1

    def run(self):
        """ Runs the created network topology and launches mininet cli"""
        self.run_silent()
        CLI(self.net)
        self.net.stop()

    def run_silent(self):
        """ Runs silently - for unit testing """
        self.net.build()
        self.spine_a.start([self.flare])
        self.spine_b.start([self.flare])
        for leaf in self.leaves:
            leaf.start([self.flare])

    def pingAll(self):
        """ PingAll to create flows - for unit testing """
        self.net.pingAll()

    def stop(self):
        "Stops the topology. You should call this after run_silent"
        self.net.stop()

