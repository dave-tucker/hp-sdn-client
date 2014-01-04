#!/usr/bin/env python
#
#   Copyright 2013 Hewlett-Packard Development Company, L.P.
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

import setuptools
from hpsdnclient import __version__

def readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(name='hp-sdn-client',
                 version=__version__,
                 description="A python library for the HP SDN Controller REST API",
                 long_description=readme(),
                 classifiers=[
                     'Environment :: HP SDN Controller'
                     'Development Status :: 3 - Alpha',
                     'License :: OSI Approved :: MITs License',
                     'Programming Language :: Python : 2.7',
                 ],
                 keywords='hp sdn api',
                 url='https://githib.com/dave-tucker/hp-sdn-client',
                 author="Dave Tucker, Hewlett-Packard Development Company, L.P",
                 author_email="dave.j.tucker@hp.com",
                 license='MIT Licence',
                 packages=['hpsdnclient'],
                 include_package_data=True,
                 install_requires=[
                     'requests',
                     'distribute'
                 ],
                 test_suite='nose.collector',
                 tests_require=[
                     'nose',
                     'mock',
                     'httpretty>=0.7.0'
                 ],
                 dependency_links=[
                     'https://github.com/gabrielfalcao/HTTPretty/tarball/python-3.3-support#egg=httpretty-0.7.0'
                 ],
                 zip_safe=False,
)
