HP SDN Client
=============
.. image:: https://travis-ci.org/dave-tucker/hp-sdn-client.png?branch=master
    :target: https://travis-ci.org/dave-tucker/hp-sdn-client
.. image:: https://badge.fury.io/py/hp-sdn-client.png
    :target: http://badge.fury.io/py/hp-sdn-client
.. image:: https://coveralls.io/repos/dave-tucker/hp-sdn-client/badge.png
  :target: https://coveralls.io/r/dave-tucker/hp-sdn-client

**A Python library that makes interaction with the HP SDN Controller REST API easy**

Author: Dave Tucker, Hewlett Packard

Documentation
_____________

Full documentation is available `here <https://hp-sdn-client.readthedocs.org/en/latest/index.html>`_

Usage Example
-------------

To use the library::

    import hpsdnclient as hp
    controller = '10.44.254.129'
    auth = hp.XAuthToken(user='sdn', password='skyline', server=controller)
    api = hp.Api(controller=controller, auth=auth)

    api.get_datapaths()


Running with Docker
-------------------

To run an interactive python prompt using Docker::

    docker run -it davetucker/hp-sdn-client

Sample Application
------------------

Please see examples/short_detour.py

Running the Tests
-----------------

The unit tests can be run with tox. Make sure you have modified hpsdnclient/tests/tests.py before you run::

    tox -e py27 -v -- -v

tox.ini has py26, py27 and py33 environments, but only py27 is supported today.

For functional testing, a working HP VAN SDN Controller is required. Mininet is used to generate a test topology.

Set your environment variables on your workstation and mininet VM as follows::

    export SDNCTL="10.44.254.129"
    export SDNUSER="sdn"
    export SDNPASS="skyline"

It is recommended to download the Mininet VM. On the VM, start the following topology::

    sudo mn --topo tree,2,6 --mac --switch ovsk --controller remote,ip=$SDNCTL

Run the functional tests using::

    tox -e functional

The functional test for applciation uploads requires access to the internet to donwload a sample appliction.

