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

"""Tools for colors"""
import colorcet as cc

# The Blue->Magenta->White sequential color map
BMW = cc.cm.bmw
# The Black->Blue->Cyan sequential color map
KBC = cc.cm.kbc
# The Black->Gray->Yellow diverging color map
BJY = cc.cm.bjy

# Dark2 from colorbrewer
DARK2 = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a",
         "#66a61e", "#e6ab02", "#a6761d", "#666666"]

COLORS14 = ['#6929c4', '#1192e8', '#005d5d', '#9f1853', '#fa4d56',
            '#570408', '#198038', '#002d9c', '#ee538b', '#b28600',
            '#009d9a', '#012749', '#8a3800', '#a56eff']
COLORS5 = ['#6929c4', '#1192e8', '#005d5d', '#9f1853', '#570408']
COLORS4 = ['#6929c4', '#012749', '#009d9a', '#ee538b']
COLORS3 = ['#a56eff', '#005d5d', '#9f1853']
COLORS2 = ['#6929c4', '#009d9a']
COLORS1 = ['#6929c4']
