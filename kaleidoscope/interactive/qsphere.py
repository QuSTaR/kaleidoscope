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
# pytest: disable=unnecessary-list-index-lookup, consider-using-generator

"""Interactive Qsphere"""

import numpy as np
import scipy.linalg as la
import scipy.special as spsp
import matplotlib as mpl
import colorcet as cc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from kaleidoscope.errors import KaleidoscopeError
from .plotly_wrapper import PlotlyWidget, PlotlyFigure
from .bloch.primitives import BSPHERE


def qsphere(state, state_labels=True,
            state_labels_kind='bits',
            as_widget=False):
    """Plots a statevector of qubits using the qsphere
    representation.

    Parameters:
        state (ndarray): Statevector as 1D NumPy array.
        state_labels (bool): Show state labels.
        state_labels_kind (str): 'bits' (default) or 'ints'.
        as_widget (bool): Return a widget instance.

    Returns:
        PlotlyFigure or PlotlyWidget: Figure instance.

    Raises:
        KaleidoscopeError: Invalid statevector input.

    Example:

        .. jupyter-execute::

            from qiskit import QuantumCircuit
            from qiskit.quantum_info import Statevector
            import kaleidoscope.qiskit
            from kaleidoscope.interactive import qsphere

            qc = QuantumCircuit(3)
            qc.h(range(3))
            qc.ch(0,1)
            qc.s(2)
            qc.cz(2,1)
            state = qc.statevector()

            qsphere(state)
    """
    if state.__class__.__name__ in ['Statevector'] \
            and 'qiskit' in state.__class__.__module__:
        state = state.data

    if state.__class__.__name__ in ['DensityMatrix'] \
            and 'qiskit' in state.__class__.__module__:

        if not abs(1-state.data.dot(state.data).trace().real) < 1e-6:
            raise KaleidoscopeError('Input density matrix is not a pure state.')
        # pylint: disable=unexpected-keyword-arg
        _, evecs = la.eig(state.data)
        state = evecs[0].ravel()

    if len(state.shape) == 2:
        if not abs(1-state.dot(state).trace().real) < 1e-6:
            raise KaleidoscopeError('Input density matrix is not a pure state.')
        # pylint: disable=unexpected-keyword-arg
        _, evecs = la.eig(state.data)
        state = evecs[0].ravel()

    if len(state.shape) != 1:
        raise KaleidoscopeError('Input state is not 1D array.')

    if np.log2(state.shape[0]) % 1:
        raise KaleidoscopeError('Input is not a valid statevector of qubits.')

    eps = 1e-8
    norm = mpl.colors.Normalize(vmin=0, vmax=2*np.pi)
    cmap = cc.cm.CET_C1s
    num_qubits = int(np.log2(state.shape[0]))

    xvals = []
    yvals = []
    zvals = []
    colors = []
    bases = []
    probs = []
    marker_sizes = []

    for idx in range(2**num_qubits):
        prob = (state[idx]*state[idx].conj()).real
        if prob > eps:
            elem = bin(idx)[2:].zfill(num_qubits)
            weight = elem.count("1")
            zvalue = -2 * weight / num_qubits + 1
            number_of_divisions = spsp.comb(num_qubits, weight)
            weight_order = _bit_string_index(elem)
            angle = (float(weight) / num_qubits) * (np.pi * 2) + \
                    (weight_order * 2 * (np.pi / number_of_divisions))

            if (weight > num_qubits / 2) or (((weight == num_qubits / 2) and
                                              (weight_order >= number_of_divisions / 2))):
                angle = np.pi - angle - (2 * np.pi / number_of_divisions)

            xvalue = np.sqrt(1 - zvalue ** 2) * np.cos(angle)
            yvalue = np.sqrt(1 - zvalue ** 2) * np.sin(angle)

            bases.append(elem)
            probs.append(prob)
            xvals.append(xvalue)
            yvals.append(yvalue)
            zvals.append(zvalue)

            phase = np.arctan2(state[idx].imag, state[idx].real)
            phase = phase if phase >= 0 else phase+2*np.pi
            colors.append(mpl.colors.rgb2hex(cmap(norm(phase))))
            marker_sizes.append(np.sqrt(prob) * 40)

    if state_labels_kind == 'ints':
        bases = [int(kk, 2) for kk in bases]

    # Output figure instance
    fig = make_subplots(rows=5, cols=5,
                        specs=[[{"type": "scene", "rowspan": 5, "colspan": 5},
                                None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None,
                                {"rowspan": 1, "colspan": 1, "type": "domain"}
                                ]
                               ]
                        )

    figsize = (350, 350)

    # List for vector annotations, if any
    fig_annotations = []

    fig.add_trace(BSPHERE(), row=1, col=1)

    # latitudes
    for kk in _qsphere_latitudes(zvals):
        fig.add_trace(kk, row=1, col=1)

    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0],
                               mode='markers',
                               opacity=0.6,
                               marker=dict(size=4,
                                           color='#555555'),
                               ),
                  row=1, col=1)

    for kk, _ in enumerate(xvals):
        fig.add_trace(go.Scatter3d(x=[0, xvals[kk]], y=[0, yvals[kk]], z=[0, zvals[kk]],
                                   mode="lines",
                                   hoverinfo=None,
                                   opacity=0.5,
                                   line=dict(color=colors[kk], width=3)
                                   ),
                      row=1, col=1
                      )

        if state_labels:
            xanc = 'center'
            if xvals[kk] != 0:
                if xvals[kk] < 0:
                    xanc = 'right'
                else:
                    pass

            yanc = 'middle'
            if zvals[kk] != 0:
                if zvals[kk] < 0:
                    yanc = 'top'
                else:
                    yanc = 'bottom'

            fig_annotations.append(dict(showarrow=False,
                                        x=xvals[kk]*1.1,
                                        y=yvals[kk]*1.1,
                                        z=zvals[kk]*1.1,
                                        text="<b>|{}\u3009</b>".format(bases[kk]),
                                        align='left',
                                        opacity=0.7,
                                        xanchor=xanc,
                                        yanchor=yanc,
                                        xshift=10,
                                        bgcolor="#ffffff",
                                        font=dict(size=10,
                                                  color="#000000",
                                                  ),
                                        )
                                   )

    fig.add_trace(go.Scatter3d(x=xvals, y=yvals, z=zvals,
                               mode='markers',
                               opacity=1,
                               marker=dict(size=marker_sizes,
                                           color=colors),
                               ),
                  row=1, col=1)

    slices = 128
    labels = ['']*slices
    values = [1]*slices

    phase_colors = [mpl.colors.rgb2hex(cmap(norm(2*np.pi*kk/slices))) for kk in range(slices)]

    fig.add_trace(go.Pie(labels=labels, values=values, hole=.6,
                         showlegend=False,
                         textinfo='none',
                         hoverinfo='none',
                         textposition="outside",
                         rotation=90,
                         textfont_size=12,
                         marker=dict(colors=phase_colors)
                         ),
                  row=5, col=5)

    pie_x = fig.data[-1]['domain']['x']
    pie_y = fig.data[-1]['domain']['y']

    fig['layout'].update(annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=(pie_x[1]-pie_x[0])/2+pie_x[0],
            y=(pie_y[1]-pie_y[0])/2+pie_y[0],
            text='Phase',
            xanchor="center",
            yanchor="middle",
            showarrow=False,
            font=dict(size=9),
        ),
        dict(
            xref='paper',
            yref='paper',
            x=pie_x[0]-0.03,
            y=(pie_y[1]-pie_y[0])/2+pie_y[0],
            text='\U0001D70B',
            xanchor="left",
            yanchor="middle",
            showarrow=False,
            font=dict(size=14),
        ),
        dict(
            xref='paper',
            yref='paper',
            x=pie_x[1]+0.03,
            y=(pie_y[1]-pie_y[0])/2+pie_y[0],
            text='0',
            xanchor="right",
            yanchor="middle",
            showarrow=False,
            font=dict(size=12),
        ),
        dict(
            xref='paper',
            yref='paper',
            x=(pie_x[1]-pie_x[0])/2+pie_x[0],
            y=pie_y[1]+0.05,
            text='\U0001D70B/2',
            xanchor="center",
            yanchor="top",
            showarrow=False,
            font=dict(size=12),
        ),
        dict(
            xref='paper',
            yref='paper',
            x=(pie_x[1]-pie_x[0])/2+pie_x[0],
            y=pie_y[0]-0.05,
            text='3\U0001D70B/2',
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=12),
        )
    ])

    fig.update_layout(width=figsize[0],
                      height=figsize[1],
                      autosize=False,
                      hoverdistance=50,
                      showlegend=False,
                      scene_aspectmode='cube',
                      margin=dict(r=15, b=15, l=15, t=15),
                      scene=dict(annotations=fig_annotations,
                                 xaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            showspikes=False,
                                            visible=False),
                                 yaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            showspikes=False,
                                            visible=False),
                                 zaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            showspikes=False,
                                            visible=False)),
                      scene_camera=dict(eye=dict(x=0,
                                                 y=-1.4,
                                                 z=0.3)
                                        )
                      )

    if as_widget:
        return PlotlyWidget(fig)

    return PlotlyFigure(fig, modebar=True)


def _lex_index(n, k, lst):
    """Return  the lex index of a combination..

    Args:
        n (int): the total number of options .
        k (int): The number of elements.
        lst (list): list

    Returns:
        int: returns int index for lex order

    Raises:
        KaleidoscopeError: if length of list is not equal to k
    """
    if len(lst) != k:
        raise KaleidoscopeError("list should have length k")
    comb = list(map(lambda x: n - 1 - x, lst))
    dualm = sum([spsp.comb(comb[k - 1 - i], i + 1) for i in range(k)])
    return int(dualm)


def _bit_string_index(s):
    """Return the index of a string of 0s and 1s.

    Parameters:
        s (str): Bitstring.

    Returns:
        int: Index.

    Raises:
        KaleidoscopeError: If string is not binary.
    """
    n = len(s)
    k = s.count("1")
    if s.count("0") != n - k:
        raise KaleidoscopeError("s must be a string of 0 and 1")
    ones = [pos for pos, char in enumerate(s) if char == "1"]
    return _lex_index(n, k, ones)


def _qsphere_latitudes(zvals):
    """Latitude lines for sphere.

    Parameters:
        zvals (int): Input zvals

    Returns:
        list: List of Plotly traces.
    """
    lats = []
    u = np.linspace(0, 2*np.pi, 100)

    if 0 not in zvals:
        zvals = [0] + zvals
    for zv in zvals:
        th = np.arctan2(np.sqrt(1 - zv ** 2), zv)
        xvals = np.sin(th)*np.cos(u)
        yvals = np.sin(th)*np.sin(u)
        zvals = zv*np.ones_like(u)
        lats.append(go.Scatter3d(
            x=xvals, y=yvals, z=zvals,
            mode="lines",
            hoverinfo='skip',
            line=dict(
                color='#1e1e1e' if th == np.pi/2 else '#373737',
                width=2 if th == np.pi/2 else 1
            )
        ))
    return lats
