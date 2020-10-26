# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# pylint: disable=broad-except, line-too-long

"""Device layout information."""
import os
import json
import requests

# Try remote first since can be more up to date.
LAYOUTS = None
try:
    REMOTE_JSON_URL = "https://github.com/nonhermitian/ibm_quantum_system_layouts/raw/main/layouts.json"
    req = requests.get(REMOTE_JSON_URL)
    req.raise_for_status()
except Exception:
    pass
else:
    LAYOUTS = req.json()

if LAYOUTS is None:
    LAYOUTS_DIR = os.path.dirname(os.path.realpath(__file__))
    with open(LAYOUTS_DIR+"/layouts.json", 'r') as f:
        LAYOUTS = json.load(f)
    f.close()
