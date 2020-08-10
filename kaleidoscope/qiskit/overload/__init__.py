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

"""
====================================================
Qiskit add-ons (:mod:`kaleidoscope.qiskit.overload`)
====================================================

.. currentmodule:: kaleidoscope.qiskit.overload

.. important::

   All of these routines are automatically integrated
   into Qiskit when using ``import kaleidoscope.qiskit``.


QuantumCircuit
==============

.. autosummary::
   :toctree: ../stubs/

   rshift
   transpile
   sample
   statevector
   unitary


Statevector
===========

.. autosummary::
   :toctree: ../stubs/

   bloch_components

"""

import kaleidoscope.qiskit.overload.circuit
import kaleidoscope.qiskit.overload.statevector

from kaleidoscope.qiskit.overload.circuit import (rshift, sample,
                                                  statevector, unitary,
                                                  transpile)

from kaleidoscope.qiskit.overload.statevector import bloch_components
