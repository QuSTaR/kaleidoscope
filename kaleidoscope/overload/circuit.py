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

import copy
from types import MethodType
import qiskit
from qiskit.compiler.assemble import assemble
from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector, Operator
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit.providers.basebackend import BaseBackend
from qiskit.tools.monitor import job_monitor as aer_monitor
from qiskit.providers.ibmq.job import job_monitor as ibmq_monitor


class QuantumCircuit(qiskit.circuit.quantumcircuit.QuantumCircuit):
    """A QuantumCircuit class that contains additional functionality.

    Attributes:
        target_backend (BaseBackend): A backend to target.
    """

    def __rshift__(self, target):
        """Add a target backend to circuit.

        Parameters:
            target (BaseBackend): The target backend

        Returns:
            QuantumCircuit: QuantumCircuit with attached target_backend.

        Raises:
            TypeError: Input is not a valid backend instance.
        """
        if not isinstance(target, BaseBackend):
            raise TypeError('Target is not a valid backend instance.')
        self.target_backend = target  # pylint: disable=attribute-defined-outside-init
        return self

    def _wrap_circuit(self, circ, inplace=False):
        """Make an overloaded circuit from a standard Qiskit one.

        Parameters:
            circ (QuantumCircuit): Input QuantumCircuit.
            inplace (bool): Return a copy of the circuit data.

        Returns:
            QuantumCircuit: Returns overloaded QuantumCircuit.

        Raises:
            TypeError: Input is not a QuantumCircuit instance.
        """
        if not isinstance(circ, qiskit.circuit.quantumcircuit.QuantumCircuit):
            raise TypeError('Input should be a QuantumCircuit')
        out_qc = QuantumCircuit()
        if inplace:
            out_qc.name = copy.copy(circ.name)
            out_qc.qregs = copy.copy(circ.qregs)
            out_qc.cregs = copy.copy(circ.cregs)
            out_qc._data = copy.deepcopy(circ._data)
            out_qc._parameter_table = copy.deepcopy(circ._parameter_table)
            out_qc._layout = copy.copy(circ._layout)
        else:
            out_qc.name = circ.name
            out_qc.qregs = circ.qregs
            out_qc.cregs = circ.cregs
            out_qc._data = circ._data
            out_qc._parameter_table = circ._parameter_table
            out_qc._layout = circ._layout
        return out_qc

    def sample(self, backend=None, shots=1024, seed_simulator=None, memory=False):
        """Sample a the output distribution from a quantum circuit.

        Parameters:
            backend (BaseBackend): Backend to use.  Default is Aer QASM simulator.
            shots (imt): Number of times to sample.  Default is 1024.
            seed_simulator (int):  Seed to use for simulator (if backend is a simulator).
            memory (bool): Return individual measurement results.

        Returns:
            job: A job instance with `block_until_ready` attribute.
        """
        if not backend:
            backend = qiskit.Aer.get_backend('qasm_simulator')

        qobj = assemble(self,
                        shots=shots,
                        memory=memory,
                        seed_simulator=seed_simulator,
                        backend=backend)

        job = backend.run(qobj)

        if isinstance(backend, IBMQBackend):
            job.block_until_ready = MethodType(ibmq_wait, job)
        else:
            job.block_until_ready = MethodType(aer_wait, job)
        return job

    def statevector(self, include_final_measurements=False):
        """Return output statevector for the circuit.

        Parameters:
            include_final_measurements (bool): Include final measurements
                                               in the circuit.

        Returns:
            StateVector: Output statevector object.
        """
        new_circ = self
        if not include_final_measurements:
            new_circ = self.remove_final_measurements(inplace=False)
        return Statevector.from_instruction(new_circ)

    def unitary(self):
        """Return the unitary for the circuit (if any).

        Returns:
            Operator: Unitary for the circuit.
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

        Returns:

        """
        if backend is None:
            if self.target_backend:
                backend = self.target_backend
        new_qc = transpile(self, backend=backend, **kwargs)
        return self.wrap_circuit(new_qc)


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
