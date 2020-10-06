#######
Qsphere
#######

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   from qiskit.quantum_info import Statevector
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


Turn off state labels
=====================

.. jupyter-execute::

   qsphere(qc.statevector(), state_labels=False)


Integer state labels
====================

.. jupyter-execute::

   qsphere(qc.statevector(), state_labels_kind='ints')
