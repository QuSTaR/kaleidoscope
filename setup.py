# -*- coding: utf-8 -*-

#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Kaleidoscope

Quantum visualization package.
"""

import os
import sys
import setuptools

REQUIREMENTS = []

PACKAGES = ['kaleidoscope']
PACKAGE_DATA = {
    'kaleidoscope': ['version.txt']
}

DOCLINES = __doc__.split('\n')
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])

VERSION_PATH = os.path.abspath(
    os.path.join(os.path.join(os.path.dirname(__file__), 'kaleidoscope', 'VERSION.txt')))
with open(VERSION_PATH, 'r') as fd:
    VERSION = fd.read().rstrip()

setuptools.setup(
    name='kaleidoscope',
    version=VERSION,
    packages=PACKAGES,
    cmake_source_dir='.',
    description=DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    url="",
    author="kaleidoscope Development Team",
    author_email="nonhermitian@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=REQUIREMENTS,
    package_data = PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False
)
