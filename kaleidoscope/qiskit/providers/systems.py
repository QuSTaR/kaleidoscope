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

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=unexpected-keyword-arg

"""Module for easily getting IBMQ systems"""

import warnings
from qiskit import IBMQ


class KaleidoscopeSystemService():
    """The service class for systems.

    All attributes are dynamically attached to
    this class.

    This class is much simpler than the simulators
    one because there is no processing that needs
    to be done async.
    """

    def __init__(self):
        self._added_attr = None
        _system_loader(self)

    def __call__(self):
        return list(vars(self).keys())

    def refresh(self):
        """Refresh the service in place.
        """
        for key in self._added_attr:
            try:
                del self.__dict__[key]
            except AttributeError:
                pass
        self._added_attr = []
        _system_loader(self)


class KaleidoscopeSystemDispatcher():
    """Contains all the backend instances
    corresponding to the providers for a given
    system.

    All attributes are dynamically attached to
    this class.
    """
    def __call__(self):
        return list(vars(self).keys())


def _system_loader(service):
    """Attaches system dispatchers to the service
    """
    if not any(IBMQ.providers()):
        try:
            IBMQ.load_account()
        except Exception:  # pylint: disable=broad-except
            pass
    systems = _get_ibmq_systems()
    added_attr = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for name, back_list in systems.items():
            reference = back_list[0]
            num_qubits = reference._configuration.num_qubits
            system_name = "{}𖼯{}Q𖼞".format(name, num_qubits)
            dispatcher = KaleidoscopeSystemDispatcher()
            for backend in back_list:
                hub = backend.hub
                group = backend.group
                project = backend.project
                max_shots = backend._configuration.max_shots
                max_circuits = backend._configuration.max_experiments
                pulse = '_P' if backend._configuration.open_pulse else ''
                pro_str = "𖼯{}_{}{}𖼞{}_{}_{}".format(max_circuits, max_shots, pulse,
                                                     hub, group, project)
                pro_str = pro_str.replace('-', 'ー')
                setattr(dispatcher, pro_str, backend)
            setattr(service, system_name, dispatcher)
            added_attr.append(system_name)
    service._added_attr = added_attr


def _get_ibmq_systems():
    """Get instances for all IBMQ systems that the user has access to.

    Returns:
        dict: A dict of all IBMQ systems that a user has access to.
    """
    ibmq_backends = {}
    for pro in IBMQ.providers():
        for back in pro.backends():
            if not back.configuration().simulator:
                if ('alt' not in back.name()) \
                        and back.name().startswith('ibmq'):
                    if back.name() not in ibmq_backends:
                        ibmq_backends[back.name()] = [back]
                    else:
                        ibmq_backends[back.name()].append(back)
    return ibmq_backends
