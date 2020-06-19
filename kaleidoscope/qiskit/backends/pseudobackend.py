# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

"""Routines for converting properties to pseudobackends for plotting."""


class Config():
    """Defines a just-good-enough configuration to use in plotting."""
    def __init__(self, name, num_qubits, cmap):
        """
        Parameters:
            name (str): Backend name.
            num_qubits (int): Number of qubits.
            cmap (list): Nested list for backend coupling map.
        """
        self.backend_name = name
        self.n_qubits = num_qubits
        self.coupling_map = cmap
        self.quantum_volume = None
        self.simulator = False


class PseudoBackend():
    """A pseudo-backend used for plotting passed properties."""
    def __init__(self, config, props):
        """
        Parameters:
            config (Config): A just enough configuration.
            props (BackendProperties): The backend properties.
        """
        self._config = config
        self._props = props

    def name(self):
        """Returns name of the backend.

        Returns:
            str: Backend name.
        """
        return self._config.backend_name

    def configuration(self):
        """Returns the backend configuration.

        Returns:
            Config: A just-good-enough configuration.
        """
        return self._config

    def properties(self):
        """Returns the backend properties.

        Returns:
            BackendProperties: The properties for a backend.
        """
        return self._props


def properties_to_pseudobackend(props):
    """Takes a BackendProperties object and makes a pseudobackend.

    Parameters:
        props (BackendProperties): The properties of a system.

    Returns:
        PseudoBackend: The corresponding pseudobackend.
    """
    name = props.backend_name
    num_qubits = len(props.qubits)
    cmap = []
    for gate in props.gates:
        if gate.gate == 'cx':
            cmap.append(gate.qubits)

    config = Config(name, num_qubits, cmap)

    return PseudoBackend(config, props)
