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

"""Tests for system filtering"""

from kaleidoscope.qiskit import Systems


def test_num_qubits_filter():
    """Tests filtering by number of qubits"""
    systems = Systems.num_qubits == 5
    for system in systems:
        assert system.configuration().num_qubits == 5


def test_num_qubits_filter2():
    """Tests filtering by number of qubits 2"""
    systems = Systems.num_qubits > 5
    for system in systems:
        assert system.configuration().num_qubits > 5


def test_openpulse_filter():
    """Tests filtering by pulse access"""
    systems = Systems.open_pulse
    for system in systems:
        assert system.configuration().open_pulse


def test_qv_filter():
    """Tests filtering by quantum volume"""
    systems = Systems.quantum_volume >= 16
    for system in systems:
        assert system.configuration().quantum_volume >= 16
