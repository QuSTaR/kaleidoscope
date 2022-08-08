################
Bloch multi-disc
################

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   from qiskit.quantum_info import Statevector
   import kaleidoscope.qiskit
   from kaleidoscope import bloch_multi_disc


From a Qiskit statevector
=========================

.. jupyter-execute::

   N = 2
   qc = QuantumCircuit(N)
   qc.h(range(N))
   for kk in range(N):
      qc.ry(2*np.pi*np.random.random(), kk)
   for kk in range(N-1):
      qc.cx(kk,kk+1)
   for kk in range(N):
      qc.rz(2*np.pi*np.random.random(), kk)

   state = Statevector.from_instruction(qc)
   bloch_multi_disc(state)


Change colormap
===============

.. jupyter-execute::

   from matplotlib.cm import cool_r

   bloch_multi_disc(Statevector.from_instruction(qc), colormap=cool_r)


Turn off qubit labels
=====================

.. jupyter-execute::

   bloch_multi_disc(Statevector.from_instruction(qc), titles=False)
