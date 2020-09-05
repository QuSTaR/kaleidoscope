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
# pylint: disable=invalid-name

# Modified to also take backend parameters object, as well as the
# simulators objects from the Kaleidoscope providers.

"""Interactive error map for IBM Quantum Experience devices."""

import math
import numpy as np
import matplotlib as mpl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from qiskit.providers.models.backendproperties import BackendProperties
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit.test.mock.fake_backend import FakeBackend
import colorcet as cc
from kaleidoscope.errors import KaleidoscopeError
from kaleidoscope.qiskit.providers.simulators import DeviceSimulator
from kaleidoscope.interactive.plotly_wrapper import PlotlyWidget, PlotlyFigure
from kaleidoscope.qiskit.backends.device_layouts import DEVICE_LAYOUTS
from kaleidoscope.qiskit.backends.pseudobackend import properties_to_pseudobackend
from kaleidoscope.colors import BMY_PLOTLY

CMAP = cc.cm.bmy


def system_error_map(backend,
                     figsize=(800, 500),
                     show_title=True,
                     remove_badcal_edges=True,
                     background_color='white',
                     as_widget=False):
    """Plot the error map of a device.

    Args:
        backend (IBMQBackend or FakeBackend or DeviceSimulator or Properties): Plot the error map
                                                                               for a backend.
        figsize (tuple, optional): Figure size in pixels.
        show_title (bool, optional): Whether to show figure title.
        remove_badcal_edges (bool, optional): Whether to remove bad CX gate calibration data.
        background_color (str, optional): Background color, either 'white' or 'black'.
        as_widget (bool, optional): ``True`` if the figure is to be returned as a ``PlotlyWidget``.
            Otherwise the figure is to be returned as a ``PlotlyFigure``.

    Returns:
        PlotlyFigure or PlotlyWidget: The error map figure.

    Raises:
        KaleidoscopeError: Invalid input type.

    Example:
        .. jupyter-execute::

            from qiskit import *
            from kaleidoscope.qiskit.backends import system_error_map

            pro = IBMQ.load_account()
            backend = pro.backends.ibmq_vigo
            system_error_map(backend)

    """
    if not isinstance(backend, (IBMQBackend, DeviceSimulator,
                                FakeBackend, BackendProperties)):
        raise KaleidoscopeError('Input is not a valid backend or properties object.')

    if isinstance(backend, BackendProperties):
        backend = properties_to_pseudobackend(backend)

    meas_text_color = '#000000'
    if background_color == 'white':
        color_map = CMAP
        text_color = '#000000'
        plotly_cmap = BMY_PLOTLY
    elif background_color == 'black':
        color_map = CMAP
        text_color = '#FFFFFF'
        plotly_cmap = BMY_PLOTLY
    else:
        raise KaleidoscopeError(
            '"{}" is not a valid background_color selection.'.format(background_color))

    if backend.configuration().simulator and not isinstance(backend, DeviceSimulator):
        raise KaleidoscopeError('Requires a device backend, not a simulator.')

    config = backend.configuration()
    n_qubits = config.n_qubits
    cmap = config.coupling_map

    if n_qubits in DEVICE_LAYOUTS.keys():
        grid_data = DEVICE_LAYOUTS[n_qubits]
    else:
        fig = go.Figure()
        fig.update_layout(showlegend=False,
                          plot_bgcolor=background_color,
                          paper_bgcolor=background_color,
                          width=figsize[0], height=figsize[1],
                          margin=dict(t=60, l=0, r=0, b=0)
                          )
        out = PlotlyWidget(fig)
        return out

    props = backend.properties()

    freqs = []
    t1s = []
    t2s = []
    alphas = []
    for qubit_props in props.qubits:
        for item in qubit_props:
            if item.name == 'frequency':
                freqs.append(item.value)
            elif item.name == 'T1':
                t1s.append(item.value)
            elif item.name == 'T2':
                t2s.append(item.value)
            elif item.name == 'anharmonicity':
                alphas.append(item.value)

    # U2 error rates
    single_gate_errors = [0]*n_qubits
    single_gate_times = [0]*n_qubits
    for gate in props.gates:
        if gate.gate == 'u2':
            _qubit = gate.qubits[0]
            for gpar in gate.parameters:
                if gpar.name == 'gate_error':
                    single_gate_errors[_qubit] = gpar.value
                elif gpar.name == 'gate_length':
                    single_gate_times[_qubit] = gpar.value
                    

    # Convert to percent
    single_gate_errors = 100 * np.asarray(single_gate_errors)
    avg_1q_err = np.mean(single_gate_errors)
    max_1q_err = max(single_gate_errors)

    single_norm = mpl.colors.Normalize(
        vmin=min(single_gate_errors), vmax=max_1q_err)

    q_colors = [mpl.colors.rgb2hex(color_map(single_norm(err))) for err in single_gate_errors]

    if n_qubits > 1:
        line_colors = []
        if cmap:
            cx_errors = []
            cx_times = []
            for line in cmap:
                for gate in props.gates:
                    if gate.qubits == line:
                        for gpar in gate.parameters:
                            if gpar.name == 'gate_error':
                                cx_errors.append(gpar.value)
                            elif gpar.name == 'gate_length':
                                cx_times.append(gpar.value)

            # Convert to percent
            cx_errors = 100 * np.asarray(cx_errors)

            # remove bad cx edges
            if remove_badcal_edges:
                cx_idx = np.where(cx_errors != 100.0)[0]
            else:
                cx_idx = np.arange(len(cx_errors))

            avg_cx_err = np.mean(cx_errors[cx_idx])

            cx_norm = mpl.colors.Normalize(
                vmin=min(cx_errors[cx_idx]), vmax=max(cx_errors[cx_idx]))

            for err in cx_errors:
                if err != 100.0 or not remove_badcal_edges:
                    line_colors.append(mpl.colors.rgb2hex(color_map(cx_norm(err))))
                else:
                    line_colors.append("#ff0000")

    # Measurement errors
    read_err = []

    for qubit in range(n_qubits):
        for item in props.qubits[qubit]:
            if item.name == 'readout_error':
                read_err.append(item.value)

    read_err = 100 * np.asarray(read_err)
    avg_read_err = np.mean(read_err)
    max_read_err = np.max(read_err)

    if n_qubits < 10:
        num_left = n_qubits
        num_right = 0
    else:
        num_left = math.ceil(n_qubits / 2)
        num_right = n_qubits - num_left

    x_max = max([d[1] for d in grid_data])
    y_max = max([d[0] for d in grid_data])
    max_dim = max(x_max, y_max)

    qubit_size = 32
    font_size = 14
    offset = 0
    if cmap:
        if y_max / max_dim < 0.33:
            qubit_size = 24
            font_size = 10
            offset = 1

    if n_qubits > 5:
        right_meas_title = "Readout Error (%)"
    else:
        right_meas_title = None

    if cmap:
        cx_title = "CNOT Error Rate [Avg. {}%]".format(np.round(avg_cx_err, 3))
    else:
        cx_title = None
    fig = make_subplots(rows=2, cols=11, row_heights=[0.95, 0.05],
                        vertical_spacing=0.15,
                        specs=[[{"colspan": 2}, None, {"colspan": 6},
                                None, None, None,
                                None, None, {"colspan": 2},
                                None, None],
                               [{"colspan": 4}, None, None,
                                None, None, None,
                                {"colspan": 4}, None, None,
                                None, None]],
                        subplot_titles=("Readout Error (%)", None, right_meas_title,
                                        "Hadamard Error Rate [Avg. {}%]".format(
                                            np.round(avg_1q_err, 3)),
                                        cx_title)
                        )

    # Add lines for couplings
    if cmap and n_qubits > 1:
        for ind, edge in enumerate(cmap):
            is_symmetric = False
            if edge[::-1] in cmap:
                is_symmetric = True
            y_start = grid_data[edge[0]][0] + offset
            x_start = grid_data[edge[0]][1]
            y_end = grid_data[edge[1]][0] + offset
            x_end = grid_data[edge[1]][1]

            if is_symmetric:
                if y_start == y_end:
                    x_end = (x_end - x_start) / 2 + x_start
                    x_mid = x_end
                    y_mid = y_start

                elif x_start == x_end:
                    y_end = (y_end - y_start) / 2 + y_start
                    x_mid = x_start
                    y_mid = y_end

                else:
                    x_end = (x_end - x_start) / 2 + x_start
                    y_end = (y_end - y_start) / 2 + y_start
                    x_mid = x_end
                    y_mid = y_end
            else:
                if y_start == y_end:
                    x_mid = (x_end - x_start) / 2 + x_start
                    y_mid = y_end

                elif x_start == x_end:
                    x_mid = x_end
                    y_mid = (y_end - y_start) / 2 + y_start

                else:
                    x_mid = (x_end - x_start) / 2 + x_start
                    y_mid = (y_end - y_start) / 2 + y_start

            cx_str = 'cnot<sub>err</sub> = {err}'
            cx_str += '<br>&#120591;<sub>cx</sub>     = {tau} ns'
            fig.append_trace(
                go.Scatter(x=[x_start, x_mid, x_end],
                           y=[-y_start, -y_mid, -y_end],
                           mode="lines",
                           line=dict(width=6,
                                     color=line_colors[ind]),
                           hoverinfo='text',
                           hovertext=cx_str.format(
                               err=np.round(cx_errors[ind], 3),
                               tau=np.round(cx_times[ind], 2))
                           ),
                row=1, col=3)

    # Add the qubits themselves
    qubit_text = []
    qubit_str = "<b>Qubit {idx}</b>"
    qubit_str += "<br>freq = {freq} GHz"
    qubit_str += "<br>T<sub>1</sub>   = {t1} \u03BCs"
    qubit_str += "<br>T<sub>2</sub>   = {t2} \u03BCs"
    qubit_str += "<br>&#945;    = {anh} GHz"
    qubit_str += "<br>sx<sub>err</sub> = {err} %"
    qubit_str += "<br>&#120591;<sub>sx</sub>   = {tau} ns"
    for kk in range(n_qubits):
        qubit_text.append(qubit_str.format(idx=kk,
                                           freq=np.round(freqs[kk], 5),
                                           t1=np.round(t1s[kk], 2),
                                           t2=np.round(t2s[kk], 2),
                                           anh=np.round(alphas[kk], 3),
                                           err=np.round(single_gate_errors[kk], 3),
                                           tau=np.round(single_gate_times[kk],2)))

    if n_qubits > 20:
        qubit_size = 23
        font_size = 11

    if n_qubits > 50:
        qubit_size = 20
        font_size = 9

    qtext_color = []
    for ii in range(n_qubits):
        if single_gate_errors[ii] > 0.8*max_1q_err:
            qtext_color.append('black')
        else:
            qtext_color.append('white')

    fig.append_trace(go.Scatter(
        x=[d[1] for d in grid_data],
        y=[-d[0]-offset for d in grid_data],
        mode="markers+text",
        marker=go.scatter.Marker(size=qubit_size,
                                 color=q_colors,
                                 opacity=1),
        text=[str(ii) for ii in range(n_qubits)],
        textposition="middle center",
        textfont=dict(size=font_size, color=qtext_color),
        hoverinfo="text",
        hovertext=qubit_text), row=1, col=3)

    fig.update_xaxes(row=1, col=3, visible=False)
    _range = None
    if offset:
        _range = [-3.5, 0.5]
    fig.update_yaxes(row=1,
                     col=3,
                     visible=False,
                     range=_range)

    # H error rate colorbar
    min_1q_err = min(single_gate_errors)
    max_1q_err = max(single_gate_errors)
    if n_qubits > 1:
        fig.append_trace(go.Heatmap(z=[np.linspace(min_1q_err,
                                                   max_1q_err, 100),
                                       np.linspace(min_1q_err,
                                                   max_1q_err, 100)],
                                    colorscale=plotly_cmap,
                                    showscale=False,
                                    hoverinfo='none'), row=2, col=1)

        fig.update_yaxes(row=2,
                         col=1,
                         visible=False)

        fig.update_xaxes(row=2,
                         col=1,
                         tickvals=[0, 49, 99],
                         ticktext=[np.round(min_1q_err, 3),
                                   np.round((max_1q_err-min_1q_err)/2+min_1q_err, 3),
                                   np.round(max_1q_err, 3)])

    # CX error rate colorbar
    if cmap and n_qubits > 1:
        min_cx_err = min(cx_errors)
        max_cx_err = max(cx_errors)
        fig.append_trace(go.Heatmap(z=[np.linspace(min_cx_err,
                                                   max_cx_err, 100),
                                       np.linspace(min_cx_err,
                                                   max_cx_err, 100)],
                                    colorscale=plotly_cmap,
                                    showscale=False,
                                    hoverinfo='none'), row=2, col=7)

        fig.update_yaxes(row=2, col=7, visible=False)

        min_cx_idx_err = min(cx_errors[cx_idx])
        max_cx_idx_err = max(cx_errors[cx_idx])
        fig.update_xaxes(row=2, col=7,
                         tickvals=[0, 49, 99],
                         ticktext=[np.round(min_cx_idx_err, 3),
                                   np.round((max_cx_idx_err-min_cx_idx_err)/2+min_cx_idx_err, 3),
                                   np.round(max_cx_idx_err, 3)])

    hover_text = "<b>Qubit {}</b><br>M<sub>err</sub> = {} %"
    # Add the left side meas errors
    for kk in range(num_left-1, -1, -1):
        fig.append_trace(go.Bar(x=[read_err[kk]], y=[kk],
                                orientation='h',
                                marker=dict(color='#c7c7c5'),
                                hoverinfo="text",
                                hoverlabel=dict(font=dict(color=meas_text_color)),
                                hovertext=[hover_text.format(kk,
                                                             np.round(read_err[kk], 3)
                                                             )]
                                ),
                         row=1, col=1)

    fig.append_trace(go.Scatter(x=[avg_read_err, avg_read_err],
                                y=[-0.25, num_left-1+0.25],
                                mode='lines',
                                hoverinfo='none',
                                line=dict(color=text_color,
                                          width=2,
                                          dash='dot')), row=1, col=1)

    fig.update_yaxes(row=1, col=1,
                     tickvals=list(range(num_left)),
                     autorange="reversed")

    fig.update_xaxes(row=1, col=1,
                     range=[0, 1.1*max_read_err],
                     tickvals=[0, np.round(avg_read_err, 2),
                               np.round(max_read_err, 2)],
                     showline=True, linewidth=1, linecolor=text_color,
                     tickcolor=text_color,
                     ticks="outside",
                     showgrid=False,
                     zeroline=False)

    # Add the right side meas errors, if any
    if num_right:
        for kk in range(n_qubits-1, num_left-1, -1):
            fig.append_trace(go.Bar(x=[-read_err[kk]],
                                    y=[kk],
                                    orientation='h',
                                    marker=dict(color='#c7c7c5'),
                                    hoverinfo="text",
                                    hoverlabel=dict(font=dict(color=meas_text_color)),
                                    hovertext=[hover_text.format(kk,
                                                                 np.round(read_err[kk], 3))]
                                    ),
                             row=1, col=9)

        fig.append_trace(go.Scatter(x=[-avg_read_err, -avg_read_err],
                                    y=[num_left-0.25, n_qubits-1+0.25],
                                    mode='lines',
                                    hoverinfo='none',
                                    line=dict(color=text_color,
                                              width=2,
                                              dash='dot')
                                    ), row=1, col=9)

        fig.update_yaxes(row=1,
                         col=9,
                         tickvals=list(range(n_qubits-1, num_left-1, -1)),
                         side='right',
                         autorange="reversed",
                         )

        fig.update_xaxes(row=1,
                         col=9,
                         range=[-1.1*max_read_err, 0],
                         tickvals=[0, -np.round(avg_read_err, 2), -np.round(max_read_err, 2)],
                         ticktext=[0, np.round(avg_read_err, 2), np.round(max_read_err, 2)],
                         showline=True, linewidth=1, linecolor=text_color,
                         tickcolor=text_color,
                         ticks="outside",
                         showgrid=False,
                         zeroline=False)

    # Makes the subplot titles smaller than the 16pt default
    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=13)

    title_text = "{} Error Map".format(backend.name()) if show_title else ''
    fig.update_layout(showlegend=False,
                      plot_bgcolor=background_color,
                      paper_bgcolor=background_color,
                      width=figsize[0], height=figsize[1],
                      title=dict(text=title_text, x=0.452),
                      title_font_size=20,
                      font=dict(color=text_color),
                      margin=dict(t=60, l=0, r=40, b=0),
                      hoverlabel=dict(font_size=14,
                                      font_family="courier,monospace",
                                      align='left'
                                      )
                      )
    if as_widget:
        return PlotlyWidget(fig)
    return PlotlyFigure(fig)
