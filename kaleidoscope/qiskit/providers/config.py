# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

"""Configrc file functionality"""

from qiskit.providers.ibmq.accountprovider import AccountProvider
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from kaleidoscope.configrc import has_kal_rc, has_rc_key, write_rc_key, get_rc_key
from kaleidoscope.errors import KaleidoscopeError


def set_default_provider(provider, overwrite=False):
    """Set the default provider for IBM Q systems.

    Parameters:
        provider (AccountProvider, IBMQBackend): A Qiskit provider instance or IBMQbackend.
        overwrite (bool): Overwrite if already set.

    Raises:
        KaleidoscopeError: Input not a valid provider.
        KaleidoscopeError: Could not load kalrc.
        KaleidoscopeError: Default provider found and overwrite=False.
    """
    if not isinstance(provider, (AccountProvider, IBMQBackend)):
        raise KaleidoscopeError('Input provider is not a valid instance.')
    if isinstance(provider, IBMQBackend):
        provider = provider.provider()
    hub = provider.credentials.hub
    group = provider.credentials.group
    project = provider.credentials.project
    provider_str = "//".join([hub, group, project])

    has_rc, rc_file = has_kal_rc()
    if not has_rc:
        raise KaleidoscopeError('Could not load kalrc.')

    if has_rc_key(rc_file, 'default_provider'):
        if not overwrite:
            raise KaleidoscopeError('Default provider already set, use overwrite=True.')

    write_rc_key(rc_file, 'default_provider', provider_str)

    # Trigger a refresh of the Systems provider
    from kaleidoscope.qiskit.providers import Systems  # pylint: disable=cyclic-import
    Systems._refresh()


def get_default_provider():
    """Return the default provider, if any.

    Returns:
        str: Default provider.

    Raises:
        KaleidoscopeError: Could not load rcfile.
    """
    has_rc, rc_file = has_kal_rc()
    if not has_rc:
        raise KaleidoscopeError('Could not load kalrc.')
    return get_rc_key(rc_file, 'default_provider')
