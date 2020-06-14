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

"""Primitives for building a 3D sphere"""

import numpy as np
import plotly.graph_objects as go

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, 2*np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))


def BSPHERE(color="#F1EBEA", opacity=0.15):
    """Surface of sphere.

    Parameters:
        color (str): Hex color for sphere.
        opacity (float): Opacity of sphere.

    Returns:
        surface: Plotly Surface trace.
    """
    surface = go.Surface(x=x, y=y, z=z,
                         opacity=opacity,
                         showscale=False,
                         hoverinfo='skip',
                         colorscale=[[0, color],
                                     [1, color]]
                        )
    return surface


def latitudes(num_lines=7):
    """Latitude lines for sphere.

    Parameters:
        num_lines (int): Number of lines to draw.

    Returns:
        list: List of Plotly traces.
    """
    lats = []
    for th in np.linspace(0, np.pi, num_lines):
        xvals = np.sin(th)*np.cos(u)
        yvals = np.sin(th)*np.sin(u)
        zvals = np.cos(th)*np.ones_like(u)
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

LATS = latitudes()


def longitudes(num_lines=7):
    """Longitude lines for sphere.

    Parameters:
        num_lines (int): Number of lines to draw.

    Returns:
        list: List of Plotly traces.
    """
    longi = []
    for th in np.linspace(0, 2*np.pi, num_lines):
        xvals = np.cos(th)*np.sin(u)*np.ones_like(u)
        yvals = np.sin(th)*np.sin(u)*np.ones_like(u)
        zvals = np.cos(u)
        longi.append(go.Scatter3d(x=xvals, y=yvals, z=zvals,
                                  mode="lines",
                                  hoverinfo='skip',
                                  line=dict(color='#373737',
                                            width=1)
                                 )
                    )
    return longi

LONGS = longitudes()

ZAXIS = go.Scatter3d(x=[0, 0], y=[0, 0], z=[-1, 1],
                     mode="lines",
                     hoverinfo='skip',
                     line=dict(color='#1e1e1e',
                               width=3)
                    )


YAXIS = go.Scatter3d(x=[0, 0], y=[-1, 1], z=[0, 0],
                     mode="lines",
                     hoverinfo='skip',
                     line=dict(color='#1e1e1e',
                               width=3)
                    )

XAXIS = go.Scatter3d(x=[-1, 1], y=[0, 0], z=[0, 0],
                     mode="lines",
                     hoverinfo='skip',
                     line=dict(color='#1e1e1e',
                               width=3)
                    )

def Z0LABEL(fontsize=16):
    """Z0 state label for sphere.

    Parameters:
        fontsize (int): Fontsize for label.

    Returns:
        label: Plotly Scatter3d trace.

    """
    label = go.Scatter3d(x=[0], y=[0], z=[1.1],
                         mode="text",
                         textposition='middle center',
                         hoverinfo='skip',
                         text='\u007C0\u3009',
                         textfont=dict(size=fontsize)
                        )
    return label

def Z1LABEL(fontsize=16):
    """Z1 state label for sphere.

    Parameters:
        fontsize (int): Fontsize for label.

    Returns:
        label: Plotly Scatter3d trace.

    """
    label = go.Scatter3d(x=[0], y=[0], z=[-1],
                         mode="text",
                         textposition='bottom center',
                         hoverinfo='skip',
                         text='\u007C1\u3009',
                         textfont=dict(size=fontsize)
                        )
    return label


def XLABEL(fontsize=16):
    """X+ state label for sphere.

    Parameters:
        fontsize (int): Fontsize for label.

    Returns:
        label: Plotly Scatter3d trace.
    """
    label = go.Scatter3d(x=[1.2], y=[0], z=[0],
                         mode="text",
                         textposition='middle center',
                         hoverinfo='skip',
                         text='\u007C\u002Bx\u3009',
                         textfont=dict(size=fontsize)
                        )
    return label

def YLABEL(fontsize=16):
    """Y+ state label for sphere.

    Parameters:
        fontsize (int): Fontsize for label.

    Returns:
        label: Plotly Scatter3d trace.
    """
    label = go.Scatter3d(x=[0], y=[1.2], z=[0],
                         mode="text",
                         textposition='middle center',
                         hoverinfo='skip',
                         text='\u007C\u002By\u3009',
                         textfont=dict(size=fontsize)
                        )
    return label
