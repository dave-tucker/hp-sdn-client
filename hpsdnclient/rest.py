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

""" Here is the implementation for the REST verbs using the Requests API """

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.1.0'

from error import FlareApiError

import requests

DATA_TYPES = set(['json', 'zip'])

def get(url, token, data_type):
	""" get()

		Implements the REST GET verb using the Requests API.

	"""
	r = requests.get(url, auth=token, verify=False)
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
		raise FlareApiError("Oh No! Something went wrong")
		r.raise_for_status()

def put(url, token, data):
	""" put()

		Implements the REST PUT verb using the Requests API.

	"""
	r = requests.put(url, auth=token, params=data, verify=False)
	if r.status_code in (requests.codes.ok, requests.codes.accepted, requsts.codes.no_content):
		return
	else:
		raise FlareApiError("Oh No! Something went wrong")
		r.raise_for_status()

def post(url, token, data):
	""" post()

		Implements the REST POST verb using the Requests API.

	"""
	r = requests.post(url, auth=token, params=data, verify=False)
	if r.status_code in (requests.codes.ok, requests.codes.accepted, requsts.codes.no_content):
		return
	else:
		raise FlareApiError("Oh No! Something went wrong")
		r.raise_for_status()
		
def delete(url, token, data):
	""" delete()

		Implements the REST DELETE verb using the Requests API.

	"""
	r = requests.delete(url, auth=token, params=data, verify=False)
	if r.status_code in (requests.codes.ok, requests.codes.accepted, requsts.codes.no_content):
		return
	else:
		raise FlareApiError("Oh No! Something went wrong")
		r.raise_for_status()
		
def head(url, token):
	""" head()

		Implements the REST HEAD verb using the Requests API.

	"""
	r = requests.head(url, auth=token, verify=False)
	if r.status_code in (requests.codes.ok, requests.codes.accepted, requsts.codes.no_content):
		return
	else:
		raise FlareApiError("Oh No! Something went wrong")
		r.raise_for_status()
		