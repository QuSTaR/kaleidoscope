# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# pylint: disable=wrong-import-position

"""Kaleidoscope"""

import os

# This is needed because version info is only generated
# at setup.  This should only fall back when not using
# setup.py lint or style to check.
try:
    from .version import version as __version__
except ImportError:
    __version__ = '0.0.0'

from kaleidoscope.interactive import *
from kaleidoscope.backends.mpl import *

from kaleidoscope.backends.simulators import KaleidoscopeSimulatorService

Simulators = KaleidoscopeSimulatorService()
