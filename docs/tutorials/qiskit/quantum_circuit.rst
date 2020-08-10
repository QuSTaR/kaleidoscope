########################
QuantumCircuit addons
########################

.. jupyter-execute::

   import numpy as np
   from qiskit import QuantumCircuit
   import kaleidoscope.qiskit
   from kaleidoscope.qiskit.providers import Simulators


Adding a target backend to a circuit
====================================

.. jupyter-execute::

   sim = Simulators.aer_vigo_simulator
   qc = QuantumCircuit(5, 5) >> sim

   print(qc.target_backend)


Transpiling for assigned target backend
=======================================

.. jupyter-execute::

   qc = QuantumCircuit(5, 5) >> sim
   qc.h(0)
   qc.cx(0, range(1,5))
   qc.measure(range(5), range(5))

   new_qc = qc.transpile()

   new_qc.draw('mpl')


Transpiling for different backend
=================================

.. jupyter-execute::

   new_sim = Simulators.aer_rome_simulator

   new_qc = qc.transpile(backend=new_sim)

   print(new_qc.target_backend)
   new_qc.draw('mpl')


Sampling from a target backend
===============================

.. jupyter-execute::

   counts = new_qc.sample(shots=2048).result_when_done()
   print(counts)


Getting a statevector
=====================

.. jupyter-execute::

   qc = QuantumCircuit(3, 3)
   qc.h(0)
   qc.cx(0, range(1,3))
   qc.measure(range(3), range(3))

   qc.statevector()


Getting a unitary
=================

.. jupyter-execute::

   qc = QuantumCircuit(3, 3)
   qc.h(0)
   qc.cx(0, range(1,3))
   qc.measure(range(3), range(3))

   qc.unitary()
