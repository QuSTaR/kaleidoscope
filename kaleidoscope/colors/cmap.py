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

"""Colormap routines"""
import numpy as np

def cmap_to_plotly(cmap):
    """Convert a color map to a plotly color scale.

    Parameters:
        cmap (matplotlib.colors.Colormap): Color map to be converted.

    Returns:
        Color scale.
    """
    pl_entries = 255
    hgt = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        clr = list(map(np.uint8, np.array(cmap(k*hgt)[:3])*255))
        pl_colorscale.append([k*hgt, 'rgba'+str((clr[0], clr[1], clr[2], 1.0))])

    return pl_colorscale
