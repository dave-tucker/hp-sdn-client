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

from mininet.topo import Topo
from mininet.util import irange

MAC = 12
DPID = 16

def string_to_hex(s, length):
    tmp = '{0:#x}'.format(int(s.replace(':', '').lstrip('0'),length))
    return tmp

def hex_to_string(h, length):
    tmp = h.lstrip('0x').zfill(length)
    tmp = ':'.join(a+b for a,b in zip(tmp[::2], tmp[1::2]))
    return tmp

class Tree(Topo):
    """Create tree topology for mininet"""

    def __init__( self, k=2, **opts):
        """Init.
        	k: number of leaf switches (and hosts)
        	hconf: host configuration options
        	lcong: link configuration options """

        super(FatTree, self).__init__(**opts)

        self.k = k

        #Add spine switch
        s0 = self.addSwitch( 's0')

        for i in irange(1,k):
        	host = self.addHost('h%s' % i)
        	switch = self.addSwitch('s%s' %i)
        	self.addLink( host, switch)
        	self.addLink( switch, s0)