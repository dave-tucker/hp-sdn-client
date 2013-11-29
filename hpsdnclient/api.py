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

import json

from hpsdnclient.datatypes import JsonObjectFactory
from hpsdnclient.error import raise_errors, NotFound
import hpsdnclient.rest as rest

JSON_MAP = {
             'controller_stats' : 'ControllerStats',
             'stats' : 'Stats',
             'datapath' : 'Datapath',
             'meter_features' : 'MeterFeatures',
             'group_features' : 'GroupFeatures',
             'port' : 'Port',
             'meter' : 'Meter',
             'flow' : 'Flow',
             'group' : 'Group',
             'cluster' : 'Cluster',
             'packet' : 'Packet'
           }

PLURALS = { 'datapaths': JSON_MAP['datapath'],
            'ports' : JSON_MAP['port'],
            'meters': JSON_MAP['meter'],
            'flows': JSON_MAP['flow'],
            'groups': JSON_MAP['group'],
            'clusters': JSON_MAP['cluster'],
            'links': 'Link',
            'nodes': 'Node',
            'arps': 'Arp',
            'lldp_suppressed' : 'LldpProperties',
            'observations' : 'observation',
            'packets': JSON_MAP['packet'],

          }


class ApiBase(object):
    """Base class for the Api object"""
    def __init__(self, controller, auth):
        self.controller = controller
        self.auth = auth

    def _get(self, url, is_file=False):
        result = []
        if is_file:
            r = rest.get(url, self.auth, is_file=True)
        else:
            r = rest.get(url, self.auth)
            raise_errors(r)

        content = r.headers['Content-Type']

        if content == 'application/json':
            data = r.json()
            key = data.keys()[0]
            if not key in PLURALS:
                try:
                    datatype = JSON_MAP[key]
                except KeyError:
                    raise NotFound("The key {} is not mapped" +
                                   "to a datatype".format(key))
                result = JsonObjectFactory.create(datatype, data[key])
            else:
                try:
                    datatype = PLURALS[key]
                except KeyError:
                    raise NotFound("The key {} is not mapped" +
                                   "to a datatype".format(key))
                for d in data[key]:
                        result.append(JsonObjectFactory.create(datatype, d))

        elif content == 'text/plain':
            result = r.text()

        elif r.headers['Content-Type'] == 'application/zip':
            data = r.content()
            # Strip the 'attachment; filename='' from Content-Disposition
            filename = r.headers["Content-Disposition"][21:]
            # Save the data to a file
            f = open(filename, 'wb')
            f.write(data)
            f.close()
            # Return the filename
            result = filename
        else:
            result = None
        return result
