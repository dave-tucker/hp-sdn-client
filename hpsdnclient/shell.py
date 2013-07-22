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

import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

class HpSdnClient(App):

	log = logging.getLogger(__name__)

	def __init__(self):
		super(HpSdnClient, self).__init__(
			description='HP SDN Controller Client',
			version='0.1',
			command_manager=CommandManager('hpsdnclient.v2'))

	def initialize_app(self, argv):
		self.log.debug('initialize_app')

	def prepare_to_run_command(self, cmd):
		self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

	def clean_up(self, cmd, result, err):
		self.log.debug('clean_up %s', cmd.__class__.__name__)
		if err:
			self.log.debug('got an error: %s', err)

def main(argv=sys.argv[1:]):
    myapp = HpSdnClient()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))