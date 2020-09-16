# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Qiskit providers"""
from qiskit.exceptions import QiskitError
from qiskit.providers.ibmq.ibmqfactory import IBMQFactory
from ._config import set_default_provider, get_default_provider

IBMQFactory.set_default_provider = set_default_provider
IBMQFactory.get_default_provider = get_default_provider

Account = IBMQFactory()
try:
    Account.load_account()
except QiskitError:
    pass

from ._systems import KaleidoscopeSystemService as _KALSysService
from ._simulators import KaleidoscopeSimulatorService as _KALSimService
Systems = _KALSysService()
Simulators = _KALSimService()
