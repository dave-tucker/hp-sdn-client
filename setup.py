#!/usr/bin/env python
#
#   Copyright 2014 Hewlett-Packard Development Company, L.P.
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

import os
from setuptools import setup
from pip.req import parse_requirements

# Get version from hpsdclient.version in a PY3 safe manner
with open("hpsdnclient/version.py") as f:
    code = compile(f.read(), "hpsdnclient/version.py", 'exec')
    exec(code)


def requires(filename):
    requirements = parse_requirements(os.path.abspath(filename))
    return [str(r.req) for r in requirements]


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='hp-sdn-client',
    version=__version__,  # pylint: disable E0602
    description=("A python library to make interacting with the"
                 "SDN Controller REST API easy"),
    long_description=readme(),
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['hp', 'sdn', 'rest', 'api'],
    url='https://github.com/dave-tucker/hp-sdn-client',
    author="Dave Tucker, Hewlett-Packard Development Company, L.P",
    author_email="dave.j.tucker@hp.com",
    license='Apache License, Version 2.0',
    packages=['hpsdnclient'],
    include_package_data=True,
    install_requires=requires('requirements.txt'),
    test_suite='nose.collector',
    tests_require=requires('test-requirements.txt'),
    zip_safe=False,
)
