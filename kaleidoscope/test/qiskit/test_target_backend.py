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
# pylint: disable=unused-import

"""Tests for Bloch routines"""

from qiskit import IBMQ, QuantumCircuit
import kaleidoscope.qiskit

PROVIDER = IBMQ.load_account()
backend = PROVIDER.backends.ibmq_vigo


def test_target_backend_attach():
    """Tests attaching target backend"""

    qc = QuantumCircuit(5, 5) >> backend
    qc.h(0)
    qc.cx(0, range(1, 5))
    qc.measure(range(5), range(5))

    assert qc.target_backend == backend


def test_target_backend_transpile():
    """Tests target backend attached to transpiled circuit"""

    qc = QuantumCircuit(5, 5) >> backend
    qc.h(0)
    qc.cx(0, range(1, 5))
    qc.measure(range(5), range(5))

    new_qc = qc.transpile()

    assert new_qc.target_backend == backend
