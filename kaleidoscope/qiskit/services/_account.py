# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# pylint: disable=unused-argument

"""Account functionality"""

from qiskit.exceptions import QiskitError
from qiskit.providers.ibmq.ibmqfactory import IBMQFactory
from ._config import set_default_provider, get_default_provider


def refresh(self):
    """Refresh the Account object
    """
    self.disable_account()
    self.load_account()

    # Trigger a refresh of the Systems provider
    from kaleidoscope.qiskit.services import Systems  # pylint: disable=cyclic-import
    Systems._refresh()


IBMQFactory.refresh = refresh
IBMQFactory.set_default_provider = set_default_provider
IBMQFactory.get_default_provider = get_default_provider

Account = IBMQFactory()
try:
    Account.load_account()
except QiskitError:
    pass
