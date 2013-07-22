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

"""This fle implements the Flare Core REST API
/support GET
/licenses GET
/licenses POST
/licenses/installid GET
/licenses/{sno} GET
/licenses/{sno}/action POST
/configs GET
/configs/{component} GET
/configs/{component} PUT
/configs/{component} DELETE
/apps GET
/apps POST
/apps/{app_uid} DELETE
/apps/{app_uid} PUT
/apps/{app_uid} GET
/apps/{app_uid}/action POST
/apps/{app_uid}/health GET
/apps/{app_uid}/health HEAD
/logs GET
/logs/local GET
/auditlog GET
/systems GET
/systems/{system_uid} GET
/systems/{system_uid}/action POST
/systems/{system_uid}/backup GET
/systems/{system_uid}/backup POST
/regions GET
/regions POST
/regions/{region_uid} GET
/regions/{region_uid} PUT
/regions/{region_uid} DELETE
/team GET
/team POST
/teamD ELETE
/team/action POST
/backups GET
/backups/{session_uid} GET
/restores GET
/restores/{session_uid} GET
/alerts GET
/alerts/topics GET
/alerts/listeners GET
/alerts/listeners POST
/alerts/listeners/{listener_uid} GET
/alerts/listeners/{listener_uid} DELETE
/alerts/listeners/{listener_uid} PUT
/metrics/primaries GET
/metrics/secondaries GET
/metrics GET
/metrics/{metric_uid} GET
/metrics/{metric_uid}/values GET
"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.0.1'

import urllib
