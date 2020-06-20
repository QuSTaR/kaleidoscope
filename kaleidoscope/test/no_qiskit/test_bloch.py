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

import numpy as np
from kaleidoscope.interactive.bloch.utils import bloch_components


def test_bloch_components():
    """Tests the Bloch components function"""

    # |0> state
    state = np.array([1, 0], dtype=complex)
    comp = bloch_components(state)[0]
    assert np.allclose(comp, [0, 0, 1])

    # |1> state
    state = np.array([0, 1], dtype=complex)
    comp = bloch_components(state)[0]
    assert np.allclose(comp, [0, 0, -1])

    # (|00> + |11>)/sqrt(2)
    state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=complex)
    comp = bloch_components(state)
    assert np.allclose(comp[0], [0.0, 0.0, 0.0])
    assert np.allclose(comp[1], [0.0, 0.0, 0.0])
