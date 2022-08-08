########################
Probability distribution
########################

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   import kaleidoscope.qiskit
   from kaleidoscope import probability_distribution


Plotting theoretical probabilities
==================================

.. jupyter-execute::

   counts = {'000': 0.5, '111': 0.5}

   probability_distribution(counts)


Change all bar colors
=====================

.. jupyter-execute::

   probability_distribution(counts, colors='#2c3d63')


Change each bar color
======================

.. jupyter-execute::

   probability_distribution(counts, colors=[['#2c3d63', '#ff6f5e']*4])


Change background color
=======================

.. jupyter-execute:: 

   probability_distribution(counts, background_color='#000000')
