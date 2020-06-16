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

import time
import warnings
import threading
import qiskit
from qiskit import IBMQ, Aer
from qiskit.providers import BaseBackend
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.models import QasmBackendConfiguration, PulseBackendConfiguration


def _version2int(version_string):
    str_list = version_string.split(
        "-dev")[0].split("rc")[0].split("a")[0].split("b")[0].split(
            "post")[0].split('.')
    return sum([int(d if len(d) > 0 else 0) * (100 ** (3 - n))
                for n, d in enumerate(str_list[:3])])


AER_VERSION = _version2int(qiskit.__qiskit_version__['qiskit-aer'])


class _Credentials():
    def __init__(self, token='', url=''):
        self.token = token
        self.url = url
        self.hub = 'hub'
        self.group = 'group'
        self.project = 'project'


class DeviceSimulator(BaseBackend):
    """This is a simulator for a real IBMQ system.

    This class can be used as a drop in replacement for a IBMQ quantum
    device.
    """

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
        if AER_VERSION >= 60000:
            self.noise_model = NoiseModel.from_backend(self, warnings=False)
        else:
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
    """
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
    if not any(IBMQ.providers()):
        try:
            IBMQ.load_account()
        except Exception:  # pylint: disable=broad-except
            pass
    systems = get_ibmq_systems()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
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

    service.refreshing = False


class KaleidoscopeSimulatorService():
    """A service for IBMQ device simulators.

    Simulators are constructed from noise models that correspond
    to the latest calibration data returned from the devices.

    System simulators are loaded async, and the name corresponds to
    which underlying simulator is doing the computation, e.g. :code:`aer_*`
    or :code:`ibmq_*`.

    Systems are attached to the service as attributes and the service
    object is available at the top-level via :code:`simulators`.
    For example, a :code:`ibmq_vigo` simulator using :code:`Aer` can be retrieved
    via:

    .. jupyter-execute::

        import kaleidoscope as kal
        sim = kal.simulators.aer_vigo_simulator

    Attributes:
        refreshing (bool): Is the service refreshing its simulators async.

    """
    def __init__(self):
        self.refreshing = False
        self.refresh()

    def __call__(self):
        return list(vars(self).keys())

    def __getattr__(self, attr):
        if 'aer' in attr or 'ibmq' in attr:
            while self.refreshing:
                time.sleep(0.1)
                if attr in self.__dict__:
                    return self.__dict__[attr]
            if attr not in self.__dict__:
                raise AttributeError("Couldn't load {}.".format(attr))
            return self.__dict__[attr]
        else:
            raise AttributeError("Simulators does not have attribute {}".format(attr))

    def refresh(self):
        """Refresh the service for new backends if IBMQ
        account was not loaded before init.
        """
        self.refreshing = True
        thread = threading.Thread(target=_system_loader,
                                  args=(self, ))
        thread.start()
