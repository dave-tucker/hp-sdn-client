HP SDN Client
=============

.. image:: https://badge.fury.io/py/hp-sdn-client.png
    :target: http://badge.fury.io/py/hp-sdn-client

**A Python library that makes interaction with the HP SDN Controller REST API easy**

Author: Dave Tucker, Hewlett Packard

Documentation
_____________

Full documentation is available `here <https://hp-sdn-client.readthedocs.org/en/latest/index.html>`_

Usage Example
-------------

To use the library ::

    import hpsdnclient as hp
    controller = '10.44.254.129'
    auth = hp.XAuthToken(user='sdn', password='skyline', server=controller)
    api = hp.Api(controller=controller, auth=auth)
    
    api.get_datapaths()


Sample Application
------------------

Please see examples/short_detour.py

Running the Tests
-----------------

The unit tests can be run with tox. Make sure you have modified hpsdnclient/tests/tests.py before you run ::

tox -e py27 -v -- -v

tox.ini has py26, py27 and py33 environments, but only py27 is supported today.
