HP SDN Client
-------------

**A Python library that makes interaction with the HP SDN Controller REST API easy**

Author: Dave Tucker, Hewlett Packard 

This library is currently developed against the HP SDN Controller v2.0 API

# Usage Example

	import hpsdnclient as hp

	f = hp.api(controller='10.10.10.10',user='sdn',password='skyline')
	f.get_datapaths()


# Sample Application

Please see short_detour.py

# Running the Tests

The unit tests can be run with tox. Make sure you have modified hpsdnclient/tests/tests.py before you run.

	tox -e py27 -v -- -v

tox.ini has py26, py27 and py33 environments. Only py26 and py27 have been tested right now

# ToDo

Items still to do

- Better unit test coverage
- Implement the cache
- Python 3.3 compatibility