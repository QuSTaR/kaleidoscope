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

"""Interactive Bloch sphere"""

import numpy as np
import plotly.graph_objects as go
from kaleidoscope.colors import DARK2
from kaleidoscope.colors.utils import hex_to_rgb
from kaleidoscope.interactive.plotly_wrapper import PlotlyFigure, PlotlyWidget
from kaleidoscope.interactive.bloch.primitives import (BSPHERE, LATS, LONGS, ZAXIS, YAXIS, XAXIS,
                                                       Z0LABEL, Z1LABEL, YLABEL, XLABEL)


def bloch_sphere(vectors=None,
                 vectors_color=None,
                 vectors_alpha=None,
                 vectors_annotation=False,
                 points=None,
                 points_color=None,
                 points_alpha=None,
                 figsize=(350, 350),
                 label_fontsize=16,
                 annotation_fontsize=10,
                 as_widget=False):
    """Generates a Bloch sphere from a given collection of vector
    and/or points data expressed in cartesian coordinates, [x, y, z].

    Parameters:
        vectors (list, ndarray): Collection of one or more vectors to display.
        vectors_color (str or list): List of colors to use when plotting vectors.
        vectors_alpha (float or list): List of alphas to use when plotting vectors.
        vectors_annotation (bool or list): Boolean values to determine if a
                                           annotation should be displayed.
        points (list, ndarray): Collection of one or more points to display.
        points_color (str or list): List of colors to use when plotting points.
        points_alpha (float or list): List of alphas to use when plotting points.
        figsize (tuple): Figure size in pixels.
        label_fontsize (int): Font size for axes labels.
        annotation_fontsize (int): Font size for annotations.
        as_widget (bool): Return plot as a widget.

    Returns:
        PlotlyFigure or  PlotlyWidget: A Plotly figure or widget instance

    Raises:
        ValueError: Input lengths do not match.

    Example:
        .. jupyter-execute::

            import numpy as np
            from matplotlib.colors import LinearSegmentedColormap, rgb2hex
            from kaleidoscope.interactive import bloch_sphere

            cm = LinearSegmentedColormap.from_list('graypurple', ["#999999", "#AA00FF"])

            pointsx = [[0, -np.sin(th), np.cos(th)] for th in np.linspace(0, np.pi/2, 20)]
            pointsz = [[np.sin(th), -np.cos(th), 0] for th in np.linspace(0, 3*np.pi/4, 30)]

            points = pointsx + pointsz

            points_alpha = [np.linspace(0.8, 1, len(points))]

            points_color = [[rgb2hex(cm(kk)) for kk in np.linspace(-1,1,len(points))]]

            vectors_color = ["#777777", "#AA00FF"]

            bloch_sphere(points=points,
                         vectors=[[0, 0, 1], [1/np.sqrt(2), 1/np.sqrt(2), 0]],
                         vectors_color=vectors_color,
                         points_alpha=points_alpha,
                         points_color=points_color,
                         as_widget=True)
    """

    # Output figure instance
    fig = go.Figure()

    # List for vector annotations, if any
    fig_annotations = []

    idx = 0
    if points is not None:

        nest_depth = nest_level(points)
        # Take care of single point passed
        if nest_depth == 1:
            points = [[points]]
        # A single list of points passes
        elif nest_depth == 2:
            points = [points]
        # nest_depth = 3 means multiple lists passed

        if points_color is None:
            # passed a single point
            if nest_depth == 1:
                points_color = [DARK2[0]]
            elif nest_depth == 2:
                points_color = [[DARK2[kk % 8] for kk in range(len(points[0]))]]

            elif nest_depth == 3:
                points_color = []
                for kk, pnts in enumerate(points):
                    points_color.append(DARK2[kk % 8]*len(pnts))

        if nest_depth == 2 and nest_level(points_color) == 1:
            points_color = [points_color]

        if isinstance(points_color, str):
            points_color = [points_color]

        if points_alpha is None:
            points_alpha = [[1.0]*len(p) for p in points]

        if nest_depth == 2 and nest_level(points_alpha) == 1:
            points_alpha = [points_alpha]

        if isinstance(points_alpha, (int, float)):
            points_alpha = [[points_alpha]]

        for idx, point_collection in enumerate(points):
            x_pnts = []
            y_pnts = []
            z_pnts = []
            if isinstance(points_color[idx], str):
                _colors = [points_color[idx]]*len(point_collection)
            else:
                _colors = points_color[idx]

            if len(points_alpha[idx]) != len(point_collection):
                err_str = 'number of alpha values ({}) does not equal number of points ({})'
                raise ValueError(err_str.format(len(points_alpha[idx]), len(x_pnts)))

            mcolors = []
            for kk, point in enumerate(point_collection):
                x_pnts.append(point[0])
                y_pnts.append(point[1])
                z_pnts.append(point[2])

                mcolors.append("rgba({},{},{},{})".format(*hex_to_rgb(_colors[kk]),
                                                          points_alpha[idx][kk]))

            fig.add_trace(go.Scatter3d(x=x_pnts, y=y_pnts, z=z_pnts,
                                       mode='markers',
                                       marker=dict(size=7, color=mcolors),
                                       )
                          )
            idx += 1

    if vectors is not None:

        if vectors_color is None:
            vectors_color = [DARK2[kk+idx % 8] for kk in range(len(vectors))]

        if isinstance(vectors_color, str):
            vectors_color = [vectors_color]

        if vectors_alpha is None:
            vectors_alpha = [1.0]*len(vectors)

        if isinstance(vectors_alpha, (int, float)):
            vectors_alpha = [vectors_alpha]

        if vectors_annotation == True:
            vectors_annotation = [True]*len(vectors)
        elif not vectors_annotation:
            vectors_annotation = [False]*len(vectors)

        eps = 1e-12

        if not isinstance(vectors[0], (list, np.ndarray)):
            vectors = [[vectors[0], vectors[1], vectors[2]]]

        for idx, vec in enumerate(vectors):
            vec = np.asarray(vec)
            if np.linalg.norm(vec) > 1.0 + eps:
                raise ValueError('Vector norm must be <= 1.')
            # So that line does not go out of arrow head
            vec_line = vec / 1.05

            color_str = "rgba({},{},{},{})".format(*hex_to_rgb(vectors_color[idx]),
                                                   vectors_alpha[idx])

            fig.add_trace(go.Scatter3d(x=[0, vec_line[0]], y=[0, vec_line[1]], z=[0, vec_line[2]],
                                       mode="lines",
                                       hoverinfo=None,
                                       line=dict(color=color_str, width=10)
                                       )
                          )

            fig.add_trace(go.Cone(x=[vec[0]], y=[vec[1]], z=[vec[2]],
                                  u=[vec[0]], v=[vec[1]], w=[vec[2]],
                                  sizemode="absolute",
                                  showscale=False,
                                  opacity=vectors_alpha[idx],
                                  colorscale=[vectors_color[idx],
                                              vectors_color[idx]],
                                  sizeref=0.25,
                                  anchor="tip")
                          )

            if vectors_annotation[idx]:
                fig_annotations.append(dict(showarrow=False,
                                            x=vec[0]*1.05,
                                            y=vec[1]*1.05,
                                            z=vec[2]*1.05,
                                            text="[{},<br> {},<br> {}]".format(round(vec[0], 3),
                                                                               round(vec[1], 3),
                                                                               round(vec[2], 3)),
                                            align='left',
                                            borderpad=3,
                                            xanchor='right' if vec[1] <= 0 else "left",
                                            xshift=10,
                                            bgcolor="#53565F",
                                            font=dict(size=annotation_fontsize,
                                                      color="#ffffff",
                                                      family="Courier New, monospace",
                                                      ),
                                            )
                                       )
    # Start construction of sphere
    # Sphere
    fig.add_trace(BSPHERE())

    # latitudes
    for kk in LATS:
        fig.add_trace(kk)

    # longitudes
    for kk in LONGS:
        fig.add_trace(kk)

    # z-axis
    fig.add_trace(ZAXIS)
    # x-axis
    fig.add_trace(XAXIS)
    # y-axis
    fig.add_trace(YAXIS)

    # zaxis label
    fig.add_trace(Z0LABEL(fontsize=label_fontsize))
    fig.add_trace(Z1LABEL(fontsize=label_fontsize))
    # xaxis label
    fig.add_trace(XLABEL(fontsize=label_fontsize))
    # yaxis label
    fig.add_trace(YLABEL(fontsize=label_fontsize))

    fig.update_layout(width=figsize[0],
                      height=figsize[1],
                      autosize=False,
                      hoverdistance=50,
                      showlegend=False,
                      scene_aspectmode='cube',
                      margin=dict(r=0, b=0, l=0, t=0),
                      scene=dict(xaxis_showspikes=False,
                                 annotations=fig_annotations,
                                 yaxis_showspikes=False,
                                 xaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            visible=False),
                                 yaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            visible=False),
                                 zaxis=dict(showbackground=False,
                                            range=[-1.2, 1.2],
                                            visible=False)),
                      scene_camera=dict(eye=dict(x=1.5,
                                                 y=0.4,
                                                 z=0.4)
                                        )
                      )
    if as_widget:
        return PlotlyWidget(fig)

    return PlotlyFigure(fig)


def nest_level(lst):
    """Determine how much nesting is in a list/ ndarray.

    Parameters:
        lst (list or ndarray): Input array-like object.

    Returns:
        int: Level of nesting.
    """
    if not isinstance(lst, (list, np.ndarray)):
        return 0
    if isinstance(lst, list):
        if not lst:
            return 1
    else:
        if isinstance(lst, np.ndarray):
            if not all(lst):
                return 1
    return max(nest_level(item) for item in lst) + 1
