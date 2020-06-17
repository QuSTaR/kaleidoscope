############
Bloch sphere
############

.. jupyter-execute::

   import numpy as np
   from kaleidoscope import bloch_sphere

Vectors on the Bloch sphere
===========================

Single vector
~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [0, 1/np.sqrt(2) , 1/np.sqrt(2)]
   bloch_sphere(vec, as_widget=True)


Single vector with custom color
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(vec, vectors_color='#ff0000', as_widget=True)


Single vector with custom color as list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(vec, vectors_color=['#ff0000'], as_widget=True)


Single vector with custom color and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(vec, vectors_color='#ff0000', vectors_alpha=0.25,
                as_widget=True)


Single vector with custom color and alpha as lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   bloch_sphere(vec, vectors_color=['#002e63'], vectors_alpha=[0.5],
                as_widget=True)


A single vector with annotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), -1/np.sqrt(2), 0]
   bloch_sphere(vec, vectors_annotation=True, as_widget=True)


Multiple vectors
~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4], as_widget=True)


Multiple vectors with custom colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4],
                vectors_color=['#e34234', '#6f4e37', '#00008b', '#ff1493'],
                as_widget=True)


Multiple vectors with custom colors and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4],
                vectors_color=['#e34234', '#6f4e37', '#00008b', '#ff1493'],
                vectors_alpha=[1.0,0.35, 0.1, 0.95],
                as_widget=True)


Multiple vectors with annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4], vectors_annotation=True,
                as_widget=True)


Multiple vectors with annotations specified by list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4],
                vectors_annotation=[False, True, False, True],
                as_widget=True)


Points on the Bloch sphere
==========================

Single point
~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=vec, as_widget=True)


Single point with custom color
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=vec, points_color='#ff0000',
                as_widget=True)


Single point as a list with custom color
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=[vec], points_color='#ff0000',
                as_widget=True)


Single point and custom color as lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=[vec], points_color=['#ff0000'],
                as_widget=True)


Multiple points
~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4], as_widget=True)


Multiple points with colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4],
               points_color=['#e34234', '#6f4e37', '#00008b', '#8014ff'],
               as_widget=True)


Multiple points and colors as nested list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2, vec3, vec4]],
               points_color=[['#e34234', '#6f4e37', '#00008b', '#8014ff']],
               as_widget=True)


Single point with alpha
~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=vec, points_alpha=0.5, as_widget=True)


Multiple points as two groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]], as_widget=True)


Multiple points in two groups colors by group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]],
               points_color=['#e34234', '#8014ff'],
               as_widget=True)


Multiple points in two groups with point by point colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]],
               points_color=[['#e34234', '#ff8014'], ['#8014ff', '#93ff14']],
               as_widget=True)


Multiple points as single group with colors and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4],
               points_color=['#e34234', '#6f4e37', '#00008b', '#8014ff'],
               points_alpha=[1.0, 0.5, 1.0, 0.6], as_widget=True)


Pulling it all together
=======================
.. jupyter-execute::

   from matplotlib.colors import LinearSegmentedColormap, rgb2hex
   cm = LinearSegmentedColormap.from_list('graypurple', ["#999999", "#AA00FF"])

   pointsx = [[0, -np.sin(th), np.cos(th)] for th in np.linspace(0,np.pi/2,20)]
   pointsz = [[np.sin(th), -np.cos(th), 0] for th in np.linspace(0,3*np.pi/4,30)]
   points = pointsx+pointsz

   points_alpha = [np.linspace(0.8,1, len(points))]
   points_color = [[rgb2hex(cm(kk)) for kk in np.linspace(-1,1,len(points))]]
   vectors_color = ["#777777", "#AA00FF"]

   bloch_sphere(points=points,
               vectors=[[0,0,1], [1/np.sqrt(2),1/np.sqrt(2),0]],
               vectors_color=vectors_color,
               points_alpha=points_alpha,
               points_color=points_color,
               as_widget=True)
