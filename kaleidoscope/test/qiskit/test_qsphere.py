# -*- coding: utf-8 -*-

# This code is part of Kaleidoscope.
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

"""Tests for Bloch routines"""

import pytest
from qiskit import QuantumCircuit
from qiskit. quantum_info import DensityMatrix, partial_trace
from kaleidoscope import qsphere
from kaleidoscope.errors import KaleidoscopeError


def test_qsphere_bad_dm_input():
    """Tests the qsphere raises when passed impure dm"""

    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    dm = DensityMatrix.from_instruction(qc)
    pdm = partial_trace(dm, [0, 1])
    with pytest.raises(KaleidoscopeError):
        assert qsphere(pdm)
