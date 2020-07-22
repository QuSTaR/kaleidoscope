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

"""Overloading of the Statevector class in Qiskit"""

from qiskit.quantum_info.states.statevector import Statevector
from kaleidoscope.interactive.bloch.utils import bloch_components as bcomp


def bloch_components(self):
    """Returns the Bloch components of the statevector.
    """
    return bcomp(self.data)


# Add methods to Statevector class
Statevector.bloch_components = bloch_components
