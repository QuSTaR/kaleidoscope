############
Bloch sphere
############

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   from qiskit.quantum_info import DensityMatrix
   import kaleidoscope.qiskit
   from kaleidoscope import bloch_sphere

Vectors on the Bloch sphere
===========================

Single vector
~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [0, 1/np.sqrt(2) , 1/np.sqrt(2)]
   bloch_sphere(vec)


Single vector with custom color and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(vec, vectors_color='#ff0000', vectors_alpha=0.25)


Single vector from a Qiskit statevector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. jupyter-execute::

   qc = QuantumCircuit(1)
   qc.h(0)
   qc.t(0)

   bloch_sphere(qc.statevector())


Single vector from a Qiskit density matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. jupyter-execute::

   qc = QuantumCircuit(1)
   qc.h(0)
   qc.t(0)

   dm = DensityMatrix.from_instruction(qc)
   bloch_sphere(dm)


Multiple vectors
~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4])


Multiple vectors from Qiskit statevectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. jupyter-execute::

   qc = QuantumCircuit(1)
   qc.h(0)
   qc.t(0)

   qc2 = QuantumCircuit(1)
   qc2.ry(np.pi/4, 0)
   qc2.s(0)

   bloch_sphere([qc.statevector(), qc2.statevector()])


Multiple vectors with custom colors and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4],
                vectors_color=['#e34234', '#6f4e37', '#00008b', '#ff1493'],
                vectors_alpha=[1.0,0.35, 0.1, 0.95])


Multiple vectors with annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4], vectors_annotation=True)


Multiple vectors with annotations specified by list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere([vec1, vec2, vec3, vec4],
                vectors_annotation=[False, True, False, True])


Points on the Bloch sphere
==========================

Single point
~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=vec)


Single point with custom color
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec = [1/np.sqrt(2), 0, 1/np.sqrt(2)]
   bloch_sphere(points=vec, points_color='#ff0000')


Multiple points
~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4])


Multiple points with colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4],
               points_color=['#e34234', '#6f4e37', '#00008b', '#8014ff'])


Multiple points and colors as nested list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2, vec3, vec4]],
               points_color=[['#e34234', '#6f4e37', '#00008b', '#8014ff']])


Multiple points as two groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]])


Multiple points in two groups colors by group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]],
               points_color=['#e34234', '#8014ff'])


Multiple points in two groups with point by point colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[[vec1, vec2], [vec3, vec4]],
               points_color=[['#e34234', '#ff8014'], ['#8014ff', '#93ff14']])


Multiple points as single group with colors and alpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. jupyter-execute::

   vec1 = [0, 0, 1]
   vec2 = [1, 0, 0]
   vec3 = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   vec4 = [0, 1/np.sqrt(2), 1/np.sqrt(2)]

   bloch_sphere(points=[vec1, vec2, vec3, vec4],
               points_color=['#e34234', '#6f4e37', '#00008b', '#8014ff'],
               points_alpha=[1.0, 0.5, 1.0, 0.6])


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
               points_color=points_color)
