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

"""General plotting utility functions"""


def hex_to_rgb(hex_color):
    """Converts a HEX color to a tuple of RGB values.

    Parameters:
        hex_color (str): Input hex color string.

    Returns:
        tuple: RGB color values.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = hex_color * 2
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def find_text_color(hex_str):
    """Return correct text color, black or white,
    based on the background color.

    Parameters:
        hex_str (str): Hex color

    Returns:
        str: Output hex color for text
    """
    (r, g, b) = (hex_str[1:3], hex_str[3:5], hex_str[5:])
    color = "#ffffff"
    if 1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255 < 0.5:
        color = '#000000'
    return color
