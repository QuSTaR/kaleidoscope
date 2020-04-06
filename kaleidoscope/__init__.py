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

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT_DIR, "version.txt"), "r") as version_file:
    VERSION = version_file.read().strip()

__version__ = VERSION

from .interactive import *
from .backends.mpl import *
