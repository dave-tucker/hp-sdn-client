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
import hpsdnclient.tests.data as test_data
import hpsdnclient.datatypes as datatypes

class DatatypeTestCase(unittest.TestCase):

    def _test_type(self, data, datatype):
        obj = datatypes.JsonObjectFactory.find_and_create(data)
        self.assertTrue(isinstance(obj, datatype))

    def test_create_license(self):
        self._test_type(test_data.LICENSE, datatypes.License)

    def test_create_app(self):
        self._test_type(test_data.APP, datatypes.App)

    def test_create_app_health(self):
        self._test_type(test_data.APP_HEALTH, datatypes.AppHealth)

    def test_create_audit_log(self):
        self._test_type(test_data.AUDIT_LOG, datatypes.AuditLogEntry)

    def test_create_system(self):
        self._test_type(test_data.SYSTEMS, datatypes.System)

    def test_create_region(self):
        self._test_type(test_data.REGION, datatypes.Region)

    def test_create_team(self):
        self._test_type(test_data.TEAM, datatypes.Team)

    def test_create_alert(self):
        self._test_type(test_data.ALERT, datatypes.Alert)

    def test_create_alert_topic(self):
        self._test_type(test_data.ALERT_TOPIC, datatypes.AlertTopic)

    def test_create_alert_topic_listener(self):
        self._test_type(test_data.ALERT_TOPIC_LISTENER,
                        datatypes.AlertTopicListener)

    def test_create_metric_app(self):
        self._test_type(test_data.METRIC_APP, datatypes.MetricApp)

    def test_create_metric(self):
        self._test_type(test_data.METRIC, datatypes.Metric)

    def test_create_metric_values(self):
        self._test_type(test_data.METRIC_VALUES, datatypes.MetricValues)

    def test_create_controller_stats(self):
        self._test_type(test_data.CONTROLLER_STATS, datatypes.ControllerStats)

    def test_create_stats(self):
        self._test_type(test_data.STATS, datatypes.Stats)

    def test_create_port_stats(self):
        self._test_type(test_data.PORT_STATS, datatypes.PortStats)

    def test_create_group_stats(self):
        self._test_type(test_data.GROUP_STATS, datatypes.GroupStats)

    def test_create_meter_stats(self):
        self._test_type(test_data.METER_STATS, datatypes.MeterStats)

    def test_create_datapath(self):
        self._test_type(test_data.DATAPATH, datatypes.Datapath)

    def test_create_meter_features(self):
        self._test_type(test_data.METER_FEATURES, datatypes.MeterFeatures)

    def test_create_group_features(self):
        self._test_type(test_data.GROUP_FEATURES, datatypes.GroupFeatures)

    def test_create_port(self):
        self._test_type(test_data.PORT, datatypes.Port)

    def test_create_meter(self):
        self._test_type(test_data.METER, datatypes.Meter)

    def test_create_group(self):
        self._test_type(test_data.GROUP, datatypes.Group)

    def test_create_flow(self):
        self._test_type(test_data.FLOW, datatypes.Flow)

    def test_create_cluster(self):
        self._test_type(test_data.CLUSTER, datatypes.Cluster)

    def test_create_link(self):
        self._test_type(test_data.LINK, datatypes.Link)

    def test_create_path(self):
        self._test_type(test_data.PATH, datatypes.Path)

    def test_create_node(self):
        self._test_type(test_data.NODE, datatypes.Node)

    def test_create_lldp(self):
        self._test_type(test_data.LLDP, datatypes.LldpProperties)

    def test_create_observation(self):
        self._test_type(test_data.OBSERVATION, datatypes.Observation)

    def test_create_packet(self):
        self._test_type(test_data.PACKET, datatypes.Packet)

    def test_create_next_hop(self):
        self._test_type(test_data.NEXT_HOP, datatypes.NextHop)
