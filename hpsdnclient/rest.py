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

from error import FlareApiError

import requests

DATA_TYPES = set(['json', 'zip'])

def get(url, token, data_type):
	r = requests.get(url, auth=token)
	if r.status_code == requests.codes.ok:
		if not data_type in DATA_TYPES:
			raise FlareApiError("Invalid Data Type")
		elif data_type == 'json': 
			data = r.json()
			for d in data:
				if 'error' in d:
					raise FlareApiError("No data returned")
			return data
		elif data_type == 'zip':
			pass
		else:
			raise FlareApiError("Oh noes! Something went wrong")
			r.raise_for_status()


def put(url, token, data, data_type):
	pass

def post(url, token, data, data_type):
	pass

def delete(url, token, data, data_type):
	pass

def head(url, token, data_types):
	pass
