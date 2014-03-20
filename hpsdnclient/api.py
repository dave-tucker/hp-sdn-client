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

"""This library provides a Python interface to the HP SDN
Controller API"""


from hpsdnclient.apibase import ApiBase
from hpsdnclient.core import CoreMixin
from hpsdnclient.net import NetMixin
from hpsdnclient.of import OfMixin
from hpsdnclient.rest import RestClient


class Api(CoreMixin, OfMixin, NetMixin, ApiBase):
    """ The container class for the HP SDN Controller Api """
    def __init__(self, controller, auth):
        self.restclient = RestClient(auth)
        super(Api, self).__init__(controller, self.restclient)
