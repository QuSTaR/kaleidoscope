########################
QuantumCircuit addons
########################

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   import kaleidoscope.qiskit
   from kaleidoscope.qiskit.services import Simulators


Get Bloch components of a statevector
=====================================

.. jupyter-execute::

   qc = QuantumCircuit(3)
   qc.h(range(3))
   qc.ch(0,1)
   qc.s(2)
   qc.cz(2,1)

   qc.statevector().bloch_components()
