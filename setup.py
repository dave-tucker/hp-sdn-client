#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Here lies the setup script for the hp-flare module"""

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
