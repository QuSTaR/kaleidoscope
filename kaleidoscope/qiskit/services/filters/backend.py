# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# pylint: disable=unused-argument

"""Backend filtering functionality"""

import threading
from datetime import datetime, timedelta
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from kaleidoscope.errors import KaleidoscopeError
from kaleidoscope.utils.hardware import local_hardware_info
from .reservation_helpers import (time_intervals, _get_reservations)

_NCPUS = local_hardware_info()['cpus']


class BackendCollection(list):
    """A list subclass that makes handling IBMQBackends easier.
    """
    def __init__(self, data):
        """BackendCollection constructor

        Parameters:
            data (list or BackendCollection): List of IBMQbackend instances.

        Raises:
            TypeError: Must be list of IBMQBackends only.
        """
        for dd in data:
            if not isinstance(dd, IBMQBackend):
                raise TypeError('Backend collection requires IBMQBackend instances.')
        super().__init__(data)

    def __and__(self, other):
        return BackendCollection(set(self) & set(other))

    def __or__(self, other):
        return BackendCollection(set(self) | set(other))

    def __add__(self, other):
        """Adds to BackendCollections together.
        """
        if not isinstance(other, (BackendCollection, list)):
            if isinstance(other, list):
                other = BackendCollection(other)
            else:
                raise TypeError('BackendCollection addition works only for collections and lists.')

        return BackendCollection(set(self) | set(other))

    def __radd__(self, other):
        """Adds to BackendCollections together.
        """
        if not isinstance(other, (BackendCollection, list)):
            if isinstance(other, list):
                other = BackendCollection(other)
            else:
                raise TypeError('BackendCollection addition works only for collections and lists.')

        return BackendCollection(set(self) | set(other))

    def __getattr__(self, name):
        if name == 'num_qubits':
            out = NumQubits(self)
        elif name == 'open_pulse':
            out = HasPulse(self)
        elif name == 'quantum_volume':
            out = QVCompare(self)
        elif name == 'operational':
            out = IsOperational(self)
        elif name == 'max_circuits':
            out = MaxCircuits(self)
        elif name == 'max_shots':
            out = MaxShots(self)
        elif name == 'reservations':
            out = Reservations(self)
        else:
            raise AttributeError("BackendCollection does not have attr '{}'.".format(name))
        return out


class Comparator(BackendCollection):
    """A skeleton constructor class built on BackendCollection.
    """
    def __eq__(self, other):
        raise KaleidoscopeError('Not implimented')

    def __ne__(self, other):
        raise KaleidoscopeError('Not implimented')

    def __gt__(self, other):
        raise KaleidoscopeError('Not implimented')

    def __ge__(self, other):
        raise KaleidoscopeError('Not implimented')

    def __lt__(self, other):
        raise KaleidoscopeError('Not implimented')

    def __le__(self, other):
        raise KaleidoscopeError('Not implimented')


class IsOperational(Comparator):
    """Implements a is operational check.
    """
    def __init__(self, data):
        """BackendCollection constructor

        Parameters:
            data (BackendCollection): Collection of IBMQbackend instances
        """
        self._full_data = data
        super().__init__([back for back in data if back.status().operational])

    def __eq__(self, other):
        if (other is not None) and not isinstance(other, (bool, int)):
            raise KaleidoscopeError('Can only compare against boolean and int values.')
        if isinstance(other, int) and other not in [0, 1]:
            raise KaleidoscopeError('Integer comparison must be against 0 or 1.')
        out = [back for back in self._full_data if back.status().operational == other]
        return BackendCollection(out)

    def __ne__(self, other):
        if (other is not None) and not isinstance(other, (bool, int)):
            raise KaleidoscopeError('Can only compare against boolean and int values.')
        if isinstance(other, int) and other not in [0, 1]:
            raise KaleidoscopeError('Integer comparison must be against 0 or 1.')
        out = [back for back in self._full_data if back.status().operational != other]
        return BackendCollection(out)


class HasPulse(Comparator):
    """Implements a open_pulse check.
    """
    def __init__(self, data):
        """BackendCollection constructor

        Parameters:
            data (BackendCollection): Collection of IBMQbackend instances
        """
        self._full_data = data
        super().__init__([back for back in data if back.configuration().open_pulse])

    def __eq__(self, other):
        if (other is not None) and not isinstance(other, (bool, int)):
            raise KaleidoscopeError('Can only compare against boolean and int values.')
        if isinstance(other, int) and other not in [0, 1]:
            raise KaleidoscopeError('Integer comparison must be against 0 or 1.')
        out = [back for back in self._full_data if back.configuration().open_pulse == other]
        return BackendCollection(out)

    def __ne__(self, other):
        if (other is not None) and not isinstance(other, (bool, int)):
            raise KaleidoscopeError('Can only compare against boolean and int values.')
        if isinstance(other, int) and other not in [0, 1]:
            raise KaleidoscopeError('Integer comparison must be against 0 or 1.')
        out = [back for back in self._full_data if back.configuration().open_pulse != other]
        return BackendCollection(out)


class NumQubits(Comparator):
    """Implements a number of qubits comparator.
    """
    def __eq__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits == other]
        return BackendCollection(out)

    def __ne__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits != other]
        return BackendCollection(out)

    def __gt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits > other]
        return BackendCollection(out)

    def __ge__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits >= other]
        return BackendCollection(out)

    def __lt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits < other]
        return BackendCollection(out)

    def __le__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().num_qubits <= other]
        return BackendCollection(out)


class MaxCircuits(Comparator):
    """Implements a number of max circuits comparator.
    """
    def __eq__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments == other]
        return BackendCollection(out)

    def __ne__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments != other]
        return BackendCollection(out)

    def __gt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments > other]
        return BackendCollection(out)

    def __ge__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments >= other]
        return BackendCollection(out)

    def __lt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments < other]
        return BackendCollection(out)

    def __le__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_experiments <= other]
        return BackendCollection(out)


class MaxShots(Comparator):
    """Implements a number of max shots comparator.
    """
    def __eq__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots == other]
        return BackendCollection(out)

    def __ne__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots != other]
        return BackendCollection(out)

    def __gt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots > other]
        return BackendCollection(out)

    def __ge__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots >= other]
        return BackendCollection(out)

    def __lt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots < other]
        return BackendCollection(out)

    def __le__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = [back for back in self if back.configuration().max_shots <= other]
        return BackendCollection(out)


class QVCompare(Comparator):
    """Implements a quantum volume comparator.
    """
    def __eq__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val == other:
                    out.append(back)
        return BackendCollection(out)

    def __ne__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val != other:
                    out.append(back)
        return BackendCollection(out)

    def __gt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val > other:
                    out.append(back)
        return BackendCollection(out)

    def __ge__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val >= other:
                    out.append(back)
        return BackendCollection(out)

    def __lt__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val < other:
                    out.append(back)
        return BackendCollection(out)

    def __le__(self, other):
        if not isinstance(other, int):
            raise KaleidoscopeError('Can only compare against ints')
        out = []
        for back in self:
            if hasattr(back.configuration(), 'quantum_volume'):
                qv_val = back.configuration().quantum_volume
                if qv_val and qv_val <= other:
                    out.append(back)
        return BackendCollection(out)


class Reservations(Comparator):
    """Implements a upcoming reservations comparator.
    """
    def __eq__(self, other):
        if not isinstance(other, (str, datetime)):
            raise KaleidoscopeError('Equality can only be checked against a string or datetime')

        if isinstance(other, datetime):
            tvals = (other, other)
        else:
            tvals = time_intervals(other)

        num_sys = len(self)
        grouped_systems = [self[i:i+_NCPUS] for i in range(0, num_sys, _NCPUS)]

        threads = []
        collected_sys = []
        for kk, _ in enumerate(grouped_systems):
            thread = threading.Thread(target=_get_reservations,
                                      args=(grouped_systems[kk], tvals, collected_sys))
            thread.start()
            threads.append(thread)

        for kk in range(len(grouped_systems)):
            threads[kk].join()

        return BackendCollection(collected_sys)

    def __lt__(self, other):
        if not isinstance(other, (str, datetime)):
            raise KaleidoscopeError('Equality can only be checked against a string or datetime')

        if isinstance(other, datetime):
            if other <= datetime.now():
                raise KaleidoscopeError('Datetime must be in the future.')
            tvals = (None, other-timedelta(seconds=1))
        else:
            tvals = (None, time_intervals(other)[0]-timedelta(seconds=1))

        num_sys = len(self)
        grouped_systems = [self[i:i+_NCPUS] for i in range(0, num_sys, _NCPUS)]

        threads = []
        collected_sys = []
        for kk, _ in enumerate(grouped_systems):
            thread = threading.Thread(target=_get_reservations,
                                      args=(grouped_systems[kk], tvals, collected_sys))
            thread.start()
            threads.append(thread)

        for kk in range(len(grouped_systems)):
            threads[kk].join()

        return BackendCollection(collected_sys)

    def __le__(self, other):
        if not isinstance(other, (str, datetime)):
            raise KaleidoscopeError('Equality can only be checked against a string or datetime')

        if isinstance(other, datetime):
            if other < datetime.now():
                raise KaleidoscopeError('Datetime must be in the future.')
            tvals = (None, other)
        else:
            tvals = (None, time_intervals(other)[1])

        num_sys = len(self)
        grouped_systems = [self[i:i+_NCPUS] for i in range(0, num_sys, _NCPUS)]

        threads = []
        collected_sys = []
        for kk, _ in enumerate(grouped_systems):
            thread = threading.Thread(target=_get_reservations,
                                      args=(grouped_systems[kk], tvals, collected_sys))
            thread.start()
            threads.append(thread)

        for kk in range(len(grouped_systems)):
            threads[kk].join()

        return BackendCollection(collected_sys)

    def __gt__(self, other):
        if not isinstance(other, (str, datetime)):
            raise KaleidoscopeError('Equality can only be checked against a string or datetime')

        if isinstance(other, datetime):
            if other <= datetime.now():
                raise KaleidoscopeError('Datetime must be in the future.')
            tvals = (other+timedelta(seconds=1), None)
        else:
            tvals = (time_intervals(other)[1]+timedelta(seconds=1), None)

        num_sys = len(self)
        grouped_systems = [self[i:i+_NCPUS] for i in range(0, num_sys, _NCPUS)]

        threads = []
        collected_sys = []
        for kk, _ in enumerate(grouped_systems):
            thread = threading.Thread(target=_get_reservations,
                                      args=(grouped_systems[kk], tvals, collected_sys))
            thread.start()
            threads.append(thread)

        for kk in range(len(grouped_systems)):
            threads[kk].join()

        return BackendCollection(collected_sys)

    def __ge__(self, other):
        if not isinstance(other, (str, datetime)):
            raise KaleidoscopeError('Equality can only be checked against a string or datetime')

        if isinstance(other, datetime):
            if other <= datetime.now():
                raise KaleidoscopeError('Datetime must be in the future.')
            tvals = (other, None)
        else:
            tvals = (time_intervals(other)[0], None)

        num_sys = len(self)
        grouped_systems = [self[i:i+_NCPUS] for i in range(0, num_sys, _NCPUS)]

        threads = []
        collected_sys = []
        for kk, _ in enumerate(grouped_systems):
            thread = threading.Thread(target=_get_reservations,
                                      args=(grouped_systems[kk], tvals, collected_sys))
            thread.start()
            threads.append(thread)

        for kk in range(len(grouped_systems)):
            threads[kk].join()

        return BackendCollection(collected_sys)
