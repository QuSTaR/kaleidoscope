# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
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

"""Overloading of the QuantumCircuit class in Qiskit"""

from types import MethodType
from qiskit import Aer
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.compiler.assemble import assemble
from qiskit.compiler import transpile as trans
from qiskit.quantum_info import Statevector, Operator
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit.providers.basebackend import BaseBackend
from qiskit.tools.monitor import job_monitor as aer_monitor
from qiskit.providers.ibmq.job import job_monitor as ibmq_monitor
from kaleidoscope.errors import KaleidoscopeError


def rshift(self, target):
    """Add a target backend to circuit.

    Parameters:
        target (BaseBackend): The target backend

    Returns:
        QuantumCircuit: QuantumCircuit with attached target_backend.

    Raises:
        KaleidoscopeError: Input is not a valid backend instance.
        KaleidoscopeError: Number of qubits larger than target backend.

    Example:

        .. jupyter-execute::

            from qiskit import QuantumCircuit
            import kaleidoscope.qiskit
            from kaleidoscope.qiskit.providers import Simulators

            qc = QuantumCircuit(5, 5) >> Simulators.aer_vigo_simulator
            print(qc.target_backend)
    """
    if not isinstance(target, BaseBackend):
        raise KaleidoscopeError('Target is not a valid backend instance.')
    if self.num_qubits > target.configuration().num_qubits:
        raise KaleidoscopeError('Number of qubits larger than target backend.')
    self.target_backend = target  # pylint: disable=attribute-defined-outside-init
    return self


def sample(self, backend=None, shots=1024, seed_simulator=None, memory=False):
    """Sample a the output distribution from a quantum circuit.

    Parameters:
        backend (BaseBackend): Backend to use.  Default is Aer QASM simulator.
        shots (imt): Number of times to sample.  Default is 1024.
        seed_simulator (int):  Seed to use for simulator (if backend is a simulator).
        memory (bool): Return individual measurement results.

    Returns:
        job: A job instance with `result_when_done` attribute.
    """
    if backend is None:
        if self.target_backend:
            backend = self.target_backend
        else:
            backend = Aer.get_backend('qasm_simulator')

    qobj = assemble(self,
                    shots=shots,
                    memory=memory,
                    seed_simulator=seed_simulator,
                    backend=backend)

    job = backend.run(qobj)

    if isinstance(backend, IBMQBackend):
        job.result_when_done = MethodType(ibmq_wait, job)
    else:
        job.result_when_done = MethodType(aer_wait, job)
    return job


def statevector(self, include_final_measurements=False):
    """Return output statevector for the circuit.

    Parameters:
        include_final_measurements (bool): Include final measurements
                                            in the circuit.

    Returns:
        StateVector: Output statevector object.

    Example:

        .. jupyter-execute::

            from qiskit import QuantumCircuit
            import kaleidoscope.qiskit

            qc = QuantumCircuit(3)
            qc.h(0)
            qc.cx(0, range(1,2))

            qc.statevector()
    """
    new_circ = self
    if not include_final_measurements:
        new_circ = self.remove_final_measurements(inplace=False)
    return Statevector.from_instruction(new_circ)


def unitary(self):
    """Return the unitary for the circuit (if any).

    Returns:
        Operator: Unitary for the circuit.

    Example:

        .. jupyter-execute::

            from qiskit import QuantumCircuit
            import kaleidoscope.qiskit

            qc = QuantumCircuit(3)
            qc.h(0)
            qc.cx(0, range(1,2))

            qc.unitary()
    """
    new_circ = self.remove_final_measurements(inplace=False)
    return Operator(new_circ)


def transpile(self, backend=None, **kwargs):
    """Transpile the circuit.

    If the circuit has a `target_backend` assigned
    and `backend=None` then the target backend is
    used for transpilation.  All other `transpile`
    functionality remains unchanged.

    Parameters:
        backend (BaseBackend): Backend to transpile for.
        kwargs: any other transpiler kwargs.

    Returns:
        QuantumCircuit: Transpiled quantum circuit.

    Example:

        .. jupyter-execute::

            from qiskit import QuantumCircuit
            import kaleidoscope.qiskit
            from kaleidoscope.qiskit.providers import Simulators

            qc = QuantumCircuit(5) >> Simulators.aer_vigo_simulator
            qc.h(0)
            qc.cx(0, range(1,5))

            new_qc = qc.transpile()
            new_qc.draw('mpl')
    """
    if backend is None:
        if self.target_backend:
            backend = self.target_backend
    new_qc = trans(self, backend=backend, **kwargs)
    new_qc.target_backend = backend
    return new_qc


def aer_wait(self, monitor=False):
    """Monitor air jobs

    Parameters:
        monitor (bool): Monitor the job.

    Returns:
        dict: Counts data
    """
    if monitor:
        aer_monitor(self, interval=1e-3)
    return self.result().get_counts()


def ibmq_wait(self, monitor=False):
    """Monitor IBMQ jobs

    Parameters:
        monitor (bool): Monitor the job.

    Returns:
        dict: Counts data
    """
    if monitor:
        ibmq_monitor(self)
    return self.result().get_counts()


# Add attributes to QuantumCircuit class:
QuantumCircuit.target_backend = None
# Add methods to QuantumCircuit class:
QuantumCircuit.__rshift__ = rshift
QuantumCircuit.sample = sample
QuantumCircuit.statevector = statevector
QuantumCircuit.transpile = transpile
QuantumCircuit.unitary = unitary
