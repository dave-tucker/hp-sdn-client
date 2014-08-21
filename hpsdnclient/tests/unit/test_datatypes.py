#!/usr/bin/env python
#
#   Copyright 2014 Hewlett-Packard Development Company, L.P.
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

import unittest
import hpsdnclient.tests.data as test_data
import hpsdnclient.datatypes as datatypes


class JsonObjectTests(unittest.TestCase):
    """ Tests the JsonObject Class """

    def setUp(self):
        self.json_object = datatypes.JsonObject()
        self.json_object.a = 0
        self.json_object.b = [1, 2, 3, 4]
        self.json_object.c = {"d": 5, "e": "six", "f": [7, "eight", 9]}
        metric_app = datatypes.JsonObjectFactory.create('MetricApp',
                                                        test_data.METRIC_APP)
        self.json_object.metric_app = metric_app
        self.string = ('{\n'
                       '    "a": 0,\n'
                       '    "b": [\n'
                       '        1,\n'
                       '        2,\n'
                       '        3,\n'
                       '        4\n'
                       '    ],\n'
                       '    "c": {\n'
                       '        "d": 5,\n'
                       '        "e": "six",\n'
                       '        "f": [\n'
                       '            7,\n'
                       '            "eight",\n'
                       '            9\n'
                       '        ]\n'
                       '    },\n'
                       '    "metric_app": {\n'
                       '        "app_id": "com.hp.sdn.cloud",\n'
                       '        "app_name": "HP VAN SDN Cloud Controller"\n'
                       '    }\n'
                       '}')

    def test_to_json_string(self):
        result = self.json_object.to_json_string()
        expected = self.string
        self.assertEquals(result, expected)

    def test_to_dict(self):
        result = self.json_object.to_dict()
        expected = {"a": 0,
                    "b": [1, 2, 3, 4],
                    "c": {"d": 5, "e": "six", "f": [7, "eight", 9]},
                    "metric_app": {
                        "app_id": "com.hp.sdn.cloud",
                        "app_name": "HP VAN SDN Cloud Controller",
                    }
                    }
        self.assertEquals(result, expected)

# Omitted test case for test_factory....
#factory method is tested by the child classes in the suite below

class FactoryTests(unittest.TestCase):
    """ Tests the JsonObjectFactory """

    def _test_type(self, data, datatype):
        """ Tests that the provided data is cast to the correct class.
        If attributes within the class are also mapped to Python objects,
        these are also checked """

        type_name = datatype.__name__
        obj = datatypes.JsonObjectFactory.create(type_name, data)
        self.assertTrue(isinstance(obj, datatype))

        try:
            class_map = datatypes.CLASS_MAP[type_name]

            for key in class_map:
                if eval('obj.%s' % key) is None:
                    continue
                else:
                    attribute = eval('obj.%s' % key)
                    if type(attribute) is None:
                        break
                    elif type(attribute) == list:
                        for item in attribute:
                            cls = eval('datatypes.%s' % class_map[key])
                            self.assertTrue(isinstance(item, cls))

                    else:
                        cls = eval('datatypes.%s' % class_map[key])
                        self.assertTrue(isinstance(attribute, cls))
        except KeyError:
            pass

        return obj

    def test_add_factory(self):
        datatypes.JsonObjectFactory.add_factory('Datapath', datatypes.Datapath)
        self.assertIn('Datapath', datatypes.JsonObjectFactory.factories)
        self.assertEquals(datatypes.JsonObjectFactory.factories['Datapath'],
                          datatypes.Datapath)

    def test_factory_create(self):
        obj = self._test_type(test_data.SYSTEM, datatypes.System)
        self.assertIn('self_', dir(obj))
        self.assertIn('System', datatypes.JsonObjectFactory.factories)

    def test_create_license(self):
        self._test_type(test_data.LICENSE, datatypes.License)

    def test_create_app(self):
        self._test_type(test_data.APP, datatypes.App)

    def test_create_app_health(self):
        self._test_type(test_data.APP_HEALTH, datatypes.AppHealth)

    def test_create_audit_log(self):
        self._test_type(test_data.AUDIT_LOG, datatypes.AuditLogEntry)

    def test_create_system(self):
        self._test_type(test_data.SYSTEM, datatypes.System)

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
        obj = self._test_type(test_data.FLOW, datatypes.Flow)
        self.assertEquals(obj.actions.output, 2)

    def test_create_flow_multiple_action(self):
        obj = self._test_type(test_data.FLOW_MA, datatypes.Flow)
        self.assertEquals(obj.actions.output, [1,2,3])

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
