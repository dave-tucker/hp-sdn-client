.. HP SDN Client documentation master file, created by
   sphinx-quickstart on Sat Jan  4 17:11:04 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HP SDN Client
=============

**A Python library that makes interaction with the HP VAN SDN Controller REST API easy**

Release v\ |version|. (:ref:`Installation <install>`)

Created by Dave Tucker, Hewlett Packard

HP SDN Client is an Apache2 Licensed Python library, designed to make interacting with the HP VAN SDN Controller's REST API easy.

The `requests library by Kenneth Reitz <http://www.python-requests.org/>`_ makes it easy to use HTTP in Python.
Making RESTful API interactions easy requires a little bit of extra work...
Enter the HP SDN Client library

Features
--------

The HP SDN Client provides the following features:
    - Authentication
    - Error Handling
    - Serializing Python Objects to JSON and back again

This makes interacting with the HP VAN SDN Contoller REST API a simple method call.

Usage Example
-------------

::

    import hpsdnclient as hp

    controller = '10.44.254.129'
    auth = hp.XAuthToken(user='sdn', password='skyline', server=controller)
    api = hp.Api(controller=controller, auth=auth)

    datapaths = api.get_datapaths()
    links = api.get_links()

Sample Application
------------------

Please see examples/short_detour.py

User Documentation
------------------

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api/core
   api/of
   api/net
   api/errors
   api/auth
   api/datatypes
