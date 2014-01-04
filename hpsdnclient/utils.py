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

""" Useful utilities """

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
