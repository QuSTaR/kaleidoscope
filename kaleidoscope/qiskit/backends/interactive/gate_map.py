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

"""Interactive gate map for IBM Quantum Experience devices."""

import plotly.graph_objects as go
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit.test.mock.fake_backend import FakeBackend
from qiskit.providers.models.backendproperties import BackendProperties
from kaleidoscope.errors import KaleidoscopeError
from kaleidoscope.qiskit.services._simulators import DeviceSimulator
from kaleidoscope.qiskit.backends.pseudobackend import properties_to_pseudobackend
from kaleidoscope.interactive.plotly_wrapper import PlotlyWidget, PlotlyFigure
from kaleidoscope.qiskit.backends.device_layouts import DEVICE_LAYOUTS


def system_gate_map(
        backend,
        figsize=(None, None),
        label_qubits=True,
        qubit_size=None,
        line_width=None,
        font_size=None,
        qubit_colors="#2f4b7c",
        qubit_labels=None,
        line_colors="#2f4b7c",
        font_color="white",
        background_color='white',
        as_widget=False):
    """Plots an interactive gate map of a device.

    Args:
        backend (IBMQBackend or FakeBackend or DeviceSimulator or Properties): Plot the error map
                                                                               for a backend.
        figsize (tuple): Output figure size (wxh) in pixels.
        label_qubits (bool): Labels for the qubits.
        qubit_size (float): Size of qubit marker.
        line_width (float): Width of lines.
        font_size (float): Font size of qubit labels.
        qubit_colors (str or list): A list of colors for the qubits. If a single color is given,
                                    it's used for all qubits.
        qubit_labels (list): A list of qubit labels
        line_colors (str or list): A list of colors for each line from the coupling map. If a
                                   single color is given, it's used for all lines.
        font_color (str): The font color for the qubit labels.
        background_color (str): The background color, either 'white' or 'black'.
        as_widget (bool): Return the figure as a widget.

    Returns:
        PlotlyFigure or PlotlyWidget: Returned figure instance.

    Raises:
        KaleidoscopeError: Invalid input object.

    Example:
        .. jupyter-execute::

           from qiskit import *
           from kaleidoscope.qiskit.backends import system_gate_map

           pro = IBMQ.load_account()
           backend = pro.backends.ibmq_vigo
           system_gate_map(backend)
    """
    if not isinstance(backend, (IBMQBackend, DeviceSimulator,
                                FakeBackend, BackendProperties)):
        raise KaleidoscopeError('Input is not a valid backend or properties object.')

    if isinstance(backend, BackendProperties):
        backend = properties_to_pseudobackend(backend)

    config = backend.configuration()
    n_qubits = config.n_qubits
    cmap = config.coupling_map

    # set coloring
    if isinstance(qubit_colors, str):
        qubit_colors = [qubit_colors] * n_qubits
    if isinstance(line_colors, str):
        line_colors = [line_colors] * len(cmap) if cmap else []

    if n_qubits in DEVICE_LAYOUTS.keys():
        grid_data = DEVICE_LAYOUTS[n_qubits]
    else:
        fig = go.Figure()
        fig.update_layout(showlegend=False,
                          plot_bgcolor=background_color,
                          paper_bgcolor=background_color,
                          width=figsize[0], height=figsize[1],
                          margin=dict(t=30, l=0, r=0, b=0))

        if as_widget:
            return PlotlyWidget(fig)
        return PlotlyFigure(fig)

    offset = 0
    if cmap:
        if n_qubits in [14, 15, 16]:
            offset = 1
            if qubit_size is None:
                qubit_size = 24
            if font_size is None:
                font_size = 10
            if line_width is None:
                line_width = 4
            if figsize == (None, None):
                figsize = (400, 200)
        elif n_qubits == 27:
            if qubit_size is None:
                qubit_size = 24
            if font_size is None:
                font_size = 10
            if line_width is None:
                line_width = 4
            if figsize == (None, None):
                figsize = (400, 300)
        else:
            if qubit_size is None:
                qubit_size = 32
            if font_size is None:
                font_size = 14
            if line_width is None:
                line_width = 6
            if figsize == (None, None):
                figsize = (300, 300)
    else:
        if figsize == (None, None):
            figsize = (300, 300)
        if qubit_size is None:
            qubit_size = 30

    fig = go.Figure()

    # Add lines for couplings
    if cmap:
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

            fig.add_trace(
                go.Scatter(x=[x_start, x_mid, x_end],
                           y=[-y_start, -y_mid, -y_end],
                           mode="lines",
                           hoverinfo='none',
                           line=dict(width=line_width,
                                     color=line_colors[ind])))

    # Add the qubits themselves
    qubit_text = []
    qubit_str = "<b>Qubit {}"
    for num in range(n_qubits):
        qubit_text.append(qubit_str.format(qubit_labels[num] if qubit_labels else num))

    if qubit_labels is None:
        qubit_labels = [str(ii) for ii in range(n_qubits)]

    if n_qubits > 50:
        if qubit_size is None:
            qubit_size = 20
        if font_size is None:
            font_size = 9

    fig.add_trace(go.Scatter(
        x=[d[1] for d in grid_data],
        y=[-d[0]-offset for d in grid_data],
        mode="markers+text",
        marker=go.scatter.Marker(size=qubit_size,
                                 color=qubit_colors,
                                 opacity=1),
        text=qubit_labels if label_qubits else '',
        textposition="middle center",
        textfont=dict(size=font_size, color=font_color),
        hoverinfo="text" if label_qubits else 'none',
        hovertext=qubit_text))

    fig.update_xaxes(visible=False)
    _range = None
    if offset:
        _range = [-3.5, 0.5]
    fig.update_yaxes(visible=False, range=_range)

    fig.update_layout(showlegend=False,
                      plot_bgcolor=background_color,
                      paper_bgcolor=background_color,
                      width=figsize[0], height=figsize[1],
                      margin=dict(t=30, l=0, r=0, b=0))

    if as_widget:
        return PlotlyWidget(fig)
    return PlotlyFigure(fig)
