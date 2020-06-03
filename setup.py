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

A visualization toolkit for Qiskit and the IBM Quantum devices.
"""

import os
import subprocess
import setuptools

REQUIREMENTS = ['qiskit-terra>=0.14',
                'qiskit-ibmq-provider>=0.7',
                'numpy>=1.15',
                'scipy>=1.3',
                'numba>=0.46',
                'matplotlib>=3.1',
                'seaborn>=0.9.0',
                'jupyter',
                'plotly>=4.6',
                'colorcet',

               ]

PACKAGES = ['kaleidoscope',
            'kaleidoscope/backends',
            'kaleidoscope/backends/interactive',
            'kaleidoscope/backends/mpl',
            'kaleidoscope/colors',
            'kaleidoscope/interactive',
            'kaleidoscope/interactive/bloch'
            ]

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


# Add command for running pylint from setup.py
class PylintCommand(setuptools.Command):
    """Run Pylint on all Kaleidoscope Python source files."""
    description = 'Run Pylint on Kaleidoscope Python source files'
    user_options = [
        # The format is (long option, short option, description).
        ('pylint-rcfile=', None, 'path to Pylint config file')]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.pylint_rcfile = ''  # pylint: disable=attribute-defined-outside-init

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Pylint config file %s does not exist.' % self.pylint_rcfile)

    def run(self):
        """Run command."""
        command = ['pylint']
        if self.pylint_rcfile:
            command.append('--rcfile=%s' % self.pylint_rcfile)
        command.append(os.getcwd()+"/kaleidoscope")
        subprocess.run(command, stderr=subprocess.STDOUT, check=False)


setuptools.setup(
    name='kaleidoscope',
    version=VERSION,
    packages=PACKAGES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="",
    author="Paul Nation",
    author_email="paul.nation@ibm.com",
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
    cmdclass={'lint': PylintCommand},
    install_requires=REQUIREMENTS,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False
)
