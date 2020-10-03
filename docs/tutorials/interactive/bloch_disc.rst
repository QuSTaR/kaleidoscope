############
Bloch disc
############

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   from qiskit.quantum_info import Statevector
   import kaleidoscope.qiskit
   from kaleidoscope import bloch_disc



From a vector of Bloch components
=================================

.. jupyter-execute::

   vec = [1/np.sqrt(2), 1/np.sqrt(2), 0]
   bloch_disc(vec)


From a Qiskit statevector
=========================

.. jupyter-execute::

   qc = QuantumCircuit(1)
   qc.ry(np.pi*np.random.random(), 0)
   qc.rz(np.pi*np.random.random(), 0)

   state = Statevector.from_instruction(qc)
   bloch_disc(state)


From a Qiskit statevector using kaleidoscope overloading
========================================================

.. jupyter-execute::

   qc = QuantumCircuit(1)
   qc.ry(np.pi*np.random.random(), 0)
   qc.rz(np.pi*np.random.random(), 0)

   bloch_disc(qc.statevector())


Change colormap
===============

.. jupyter-execute::

   from matplotlib.cm import cool_r
   
   qc = QuantumCircuit(1)
   qc.ry(1, 0)
   qc.t(0)

   bloch_disc(qc.statevector(), colormap=cool_r)


Adding a title
==============

.. jupyter-execute::

   vec = [1/np.sqrt(3), 1/np.sqrt(3), -1/np.sqrt(3)]
   bloch_disc(vec, title='My qubit')
