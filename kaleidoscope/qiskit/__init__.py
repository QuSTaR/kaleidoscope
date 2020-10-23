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
# pylint: disable=wrong-import-position

"""Qiskit specific functionality"""

from kaleidoscope import HAS_QISKIT
from kaleidoscope.errors import KaleidoscopeError

if not HAS_QISKIT:
    raise KaleidoscopeError('Must install qiskit-terra, qiskit-aer, and qiskit-ibmq-provider.')

import kaleidoscope.qiskit.overload
from .backends.mpl import *
from .backends.interactive import system_error_map, system_gate_map
from .services import Account, Systems, Simulators
