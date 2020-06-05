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

"""Module for creating device simulators automatically"""

import threading
from qiskit import IBMQ, Aer
from qiskit.providers import BaseBackend
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.ibmq.exceptions import IBMQAccountCredentialsNotFound
from qiskit.providers.models import QasmBackendConfiguration, PulseBackendConfiguration


class _Credentials():
    def __init__(self, token='', url=''):
        self.token = token
        self.url = url
        self.hub = 'hub'
        self.group = 'group'
        self.project = 'project'


class DeviceSimulator(BaseBackend):
    """This is a dummy backend just for testing purposes."""

    def __init__(self, backend, backend_name, local=True):
        """FakeBackend initializer.

        Args:
            backend (IBMQBackend): IBMQBackend instance
            backend_name (str): The name to give the backend.
            local (bool): Determines if Aer of IBMQ simulator should be used.
        """
        if backend.configuration().open_pulse:
            config = PulseBackendConfiguration.from_dict(backend.configuration().to_dict())
        else:
            config = QasmBackendConfiguration.from_dict(backend.configuration().to_dict())
        super().__init__(config)
        self._credentials = _Credentials()
        self._properties = backend.properties()
        self._configuration.simulator = True
        self._configuration.local = local
        self._configuration.backend_name = backend_name
        self.noise_model = NoiseModel.from_backend(self)

        if local:
            self.sim = Aer.get_backend('qasm_simulator')
        else:
            pro = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
            self.sim = pro.backends.ibmq_qasm_simulator

    def properties(self):
        """Return backend properties"""
        return self._properties

    def run(self, qobj, **kwargs):  # pylint: disable=unused-argument
        job = self.sim.run(qobj, noise_model=self.noise_model)
        return job

    def jobs(self, **kwargs):  # pylint: disable=unused-argument
        """Fake a job history"""
        return []


def get_ibmq_systems():
    """Get instances for all IBMQ systems that the user has access to.

    Returns:
        dict: A dict of all IBMQ systems that a user has access to.

    Raises:
        ValueError: No providers found.
    """
    if not any(IBMQ.providers()):
        raise ValueError('No providers found.  Try IBMQ.load_account() first.')
    ibmq_backends = {}
    for pro in IBMQ.providers():
        for back in pro.backends():
            if not back.configuration().simulator:
                if back.name() not in ibmq_backends \
                    and ('alt' not in back.name()) \
                        and back.name().startswith('ibmq'):
                    ibmq_backends[back.name()] = back
    return ibmq_backends


def _system_loader(service):
    systems = get_ibmq_systems()
    for name, system in systems.items():
        new_name = '{}_'+name.split('_')[-1]+'_simulator'
        system = DeviceSimulator(system,
                                 new_name.format('aer'),
                                 local=True)
        system2 = DeviceSimulator(system,
                                  new_name.format('ibmq'),
                                  local=False)

        setattr(service, system.name(), system)
        setattr(service, system2.name(), system2)


class KaleidoscopeSimulatorService():
    """A service for IBMQ device simulators

    Devices are loaded async, and the name corresponds to
    which simulator is doing the computation, e.g. `aer_*`
    or `ibmq_*`.
    """
    def __init__(self):
        self.refresh()

    def __call__(self):
        return list(vars(self).keys())

    def refresh(self):
        """Refresh the service for new backends if IBMQ
        account was not loaded before init.
        """
        if not any(IBMQ.providers()):
            try:
                IBMQ.load_account()
            except IBMQAccountCredentialsNotFound:
                pass

        thread = threading.Thread(target=_system_loader,
                                  args=(self, ))
        thread.start()
