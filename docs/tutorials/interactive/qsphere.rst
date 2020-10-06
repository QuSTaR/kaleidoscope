#######
Qsphere
#######

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
   import kaleidoscope.qiskit
   from kaleidoscope import qsphere

From a NumPy array
==================

.. jupyter-execute::

   state = np.array([1/np.sqrt(2), 0, 0, 0, 0, 0, 0, 1/np.sqrt(2)])
   qsphere(state)


From a Qiskit statevector
=========================

.. jupyter-execute::

   qc = QuantumCircuit(3)
   qc.h(range(3))
   qc.cz(0,1)
   state = Statevector.from_instruction(qc)

   qsphere(state)


From a Qiskit statevector using kaleidoscope overloading
========================================================

.. jupyter-execute::

   qsphere(qc.statevector())


From a Qiskit density matrix
============================

.. note::

   The input density matrix must be a pure state.


.. jupyter-execute::

   qc = QuantumCircuit(5)
   qc.x(4)
   qc.h(range(5))
   qc.cx(4, 1)
   qc.cx(4, 3)

   dm = DensityMatrix.from_instruction(qc)
   pdm = partial_trace(dm, [4])

   qsphere(pdm)


Turn off state labels
=====================

.. jupyter-execute::

   qsphere(qc.statevector(), state_labels=False)


Integer state labels
====================

.. jupyter-execute::

   qsphere(qc.statevector(), state_labels_kind='ints')
