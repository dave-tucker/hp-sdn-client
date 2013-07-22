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

""" This file implements the Flare Net REST API

/clusters	GET
/clusters/{cluster_uid}/tree	GET
/links	GET
/paths/forward	GET
/arps	GET
/nodes	GET
/lldp	GET
/lldp	POST
/lldp	DELETE
/diag/observations	GET
/diag/observations	POST
/diag/observations	DELETE
/diag/packets	GET
/diag/packets	POST
/diag/packets/{packet_uid}	GET
/diag/packets/{packet_uid}	DELETE
/diag/packets/{packet_uid}/path	GET
/diag/packets/{packet_uid}/nexthop	GET
/diag/packets/{packet_uid}/action	POST

"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.0.1'

import urllib

