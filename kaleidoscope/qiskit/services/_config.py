# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# pylint: disable=unused-argument

"""Configrc file functionality"""

from qiskit.providers.ibmq.accountprovider import AccountProvider
from kaleidoscope.configrc import has_kal_rc, has_rc_key, write_rc_key, get_rc_key
from kaleidoscope.errors import KaleidoscopeError


def set_default_provider(self, hub=None, group=None, project=None, overwrite=False):
    """Set the default provider for IBM Q systems.

    Parameters:
        hub (str, AccountProvider): A hub name, or Qiskit provider instance
        group (str): A group name.
        project (str): A project name.
        overwrite (bool): Overwrite if already set.

    Raises:
        KaleidoscopeError: Input not a valid provider.
        KaleidoscopeError: Could not load kalrc.
        KaleidoscopeError: Default provider found and overwrite=False.
    """
    if isinstance(hub, AccountProvider):
        hub = hub.credentials.hub
        group = hub.credentials.group
        project = hub.credentials.project
    else:
        pro = self.providers(hub, group, project)
        if not pro:
            raise KaleidoscopeError('Input hub, group, and/or project not valid.')
        if len(pro) > 1:
            raise KaleidoscopeError('Inputs do not specify a unique provider.')
        pro = pro[0]
        hub = pro.credentials.hub
        group = pro.credentials.group
        project = pro.credentials.project

    provider_str = "//".join([hub, group, project])

    has_rc, rc_file = has_kal_rc()
    if not has_rc:
        raise KaleidoscopeError('Could not load kalrc.')

    if has_rc_key(rc_file, 'default_provider'):
        if not overwrite:
            raise KaleidoscopeError('Default provider already set, use overwrite=True.')

    write_rc_key(rc_file, 'default_provider', provider_str)

    # Trigger a refresh of the Systems provider
    from kaleidoscope.qiskit.services import Systems  # pylint: disable=cyclic-import
    Systems._refresh()


def get_default_provider(self):
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
