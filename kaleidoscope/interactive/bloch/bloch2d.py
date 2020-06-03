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

"""Interactive Bloch discs"""

import math
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.colors
import colorcet as cc

from qiskit.circuit.tools import pi_check
from qiskit.quantum_info.states import Statevector, DensityMatrix
from kaleidoscope.interactive.plotly_wrapper import PlotlyFigure, PlotlyWidget
from kaleidoscope.interactive.bloch.utils import bloch_components
from kaleidoscope.colors.utils import hex_to_rgb
from kaleidoscope.colors import BMY_PLOTLY

NORM = plt.Normalize(-1, 1)
CMAP = cmap = cc.cm.bmy


def bloch_sunburst(vec):
    """Create a Bloch disc using a Plotly sunburst.

    Parameters:
        vec (ndarray): A vector of Bloch components.

    Returns:
        go.Figure: A Plotly figure instance,

    Raises:
        ValueError: Input vector is not normalized.
    """
    eps = 1e-6
    vec = np.asarray(vec)
    vec_norm = np.linalg.norm(vec)
    if vec_norm > 1.0 + eps:
        raise ValueError('Input vector has length {} greater than 1.0'.format(vec_norm))

    for idx, val in enumerate(vec):
        if abs(val) < 1e-15:
            vec[idx] = 0

    th = math.atan2(vec[1], vec[0])

    if th < 0:
        th = 2*np.pi+th

    z_hex = matplotlib.colors.rgb2hex(CMAP(NORM(vec[2])))

    z_color = "rgba({},{},{},{})".format(*hex_to_rgb(z_hex), 0.95*vec_norm+0.05)
    ring_color = "rgba({},{},{},{})".format(*hex_to_rgb('#000000'), 0.95*vec_norm+0.05)

    wedge_str = "\u2329X\u232A= {x}<br>"
    wedge_str += "\u2329Y\u232A= {y}<br>"
    wedge_str += "\u2329Z\u232A= {z}<br>"
    wedge_str += "  \u03B8 = {th}<br>"
    wedge_str += " |\u03C8|= {nrm}"

    th_str = pi_check(th)
    th_str = th_str.replace('pi', '\u03C0')

    hover_text = [wedge_str.format(x=round(vec[0], 4),
                                   y=round(vec[1], 4),
                                   z=round(vec[2], 4),
                                   th=th_str,
                                   nrm=np.round(vec_norm, 4))] + [None]

    bloch = go.Sunburst(labels=[" ", "  "],
                        parents=["", " "],
                        values=[2*np.pi-th, th],
                        hoverinfo="text",
                        hovertext=hover_text,
                        marker=dict(colors=[z_color, ring_color]))
    return bloch


def bloch_disc(rho, figsize=None, title=False, as_widget=False):
    """Plot a Bloch disc for a single qubit.

    Parameters:
        rho (list or ndarray or Statevector or DensityMatrix): Input statevector or density matrix.
        figsize (tuple): Figure size in pixels, default=(200,375).
        title (bool): Display title.
        as_widget (bool): Return plot as a widget.

    Returns:
        PlotlyFigure: A Plotly figure instance
        PlotlyWidget : A Plotly widget if `as_widget=True`.

    """
    if isinstance(rho, (Statevector, DensityMatrix)):
        rho = rho.data
    if len(rho) != 3:
        rho = np.asarray(rho, dtype=complex)
        comp = bloch_components(rho)
    else:
        comp = [rho]

    if title:
        title = ["Qubit 0"] + ["\u2329Z\u232A"]
    else:
        title = [""] + ["\u2329Z\u232A"]

    if figsize is None:
        figsize = (200, 275)

    fig = make_subplots(rows=1, cols=2,
                        specs=[[{'type': 'domain'}]+[{'type': 'xy'}]],
                        subplot_titles=title,
                        column_widths=[0.93]+[0.07])

    fig.add_trace(bloch_sunburst(comp[0]), row=1, col=1)

    zrange = [k*np.ones(1) for k in np.linspace(-1, 1, 100)]

    idx = (np.abs(np.linspace(-1, 1, 100) - comp[0][2])).argmin()

    tickvals = np.array([0, 49, 99, idx])
    idx_sort = np.argsort(tickvals)
    tickvals = tickvals[idx_sort]
    ticktext = [-1, 0, 1, "\u25C0"+str(np.round(comp[0][2], 3))]
    ticktext = [ticktext[kk] for kk in idx_sort]

    fig.append_trace(go.Heatmap(z=zrange,
                                colorscale=BMY_PLOTLY,
                                showscale=False,
                                hoverinfo='none',
                               ),
                     row=1, col=2)

    fig.update_yaxes(row=1, col=2, tickvals=tickvals,
                     ticktext=ticktext)

    fig.update_yaxes(row=1, col=2, side="right")
    fig.update_xaxes(row=1, col=2, visible=False)

    fig.update_layout(margin=dict(t=30, l=10, r=0, b=0),
                      height=figsize[0],
                      width=figsize[1],
                      hoverlabel=dict(font_size=14,
                                      font_family="monospace"
                                     )
                      )
    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=14)

    if as_widget:
        PlotlyWidget(fig)

    return PlotlyFigure(fig)
