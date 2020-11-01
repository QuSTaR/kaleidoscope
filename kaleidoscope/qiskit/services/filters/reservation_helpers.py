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
# pylint: disable=wrong-import-position, too-many-return-statements

"""Functions that help for filtering reservations."""
import calendar
from datetime import datetime, timedelta, timezone
from kaleidoscope.errors import KaleidoscopeError


def time_intervals(interval):
    """Computes the start and ending datetimes for a set of commonly used intervals.

    All times are converted into the local timezone by applying the UTC offset
    for the locality.

    Current allowed ``interval`` values are:

    - 'now'
    - 'today'
    - 'tomorrow'
    - 'this week'
    - 'next week'
    - 'this month'
    - 'next month'

    Parameters:
        interval (str): A string representing the human readable interval.

    Returns:
        tuple: Start and end datetimes for specified time interval.

    Raises:
        KaleidoscopeError: Input string does not correspond to a known time interval.
    """
    now = datetime.now(timezone.utc)
    week_day = datetime.today().weekday()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # Get UTC offset in hours
    dd = now.astimezone()
    utc_offset = dd.utcoffset() // timedelta(hours=1)

    today_start = datetime(year=now.year,
                           month=now.month,
                           day=now.day,
                           hour=0,
                           minute=0,
                           second=0)

    today_end = datetime(year=now.year,
                         month=now.month,
                         day=now.day,
                         hour=23,
                         minute=59,
                         second=59)

    if interval == 'now':
        return now, now
    elif interval == 'today':
        return now, today_end - timedelta(hours=utc_offset)
    elif interval == 'tomorrow':
        start = today_end + timedelta(seconds=1)
        end = datetime(year=start.year, month=start.month, day=start.day,
                       hour=23, minute=59, second=59)
        return start - timedelta(hours=utc_offset), end - timedelta(hours=utc_offset)
    elif interval == 'this week':
        start = now
        end = today_end + timedelta(days=6-week_day)
        return start, end - timedelta(hours=utc_offset)
    elif interval == 'next week':
        start = today_start - timedelta(days=week_day-7)
        end = today_end + timedelta(days=13-week_day)
        return start - timedelta(hours=utc_offset), end - timedelta(hours=utc_offset)
    elif interval == 'this month':
        start = now
        end = datetime(year=now.year, month=now.month, day=days_in_month,
                       hour=23, minute=59, second=59)
        return start, end - timedelta(hours=utc_offset)
    elif interval == 'next month':
        start = today_start + timedelta(days=days_in_month-now.day+1)
        _days_in_month = calendar.monthrange(now.year, start.month)[1]
        end = datetime(year=start.year, month=start.month, day=_days_in_month,
                       hour=23, minute=59, second=59)
        return start - timedelta(hours=utc_offset), end - timedelta(hours=utc_offset)
    else:
        raise KaleidoscopeError("Interval must be 'now', 'today', 'tomorrow', 'this week', \
                                'next week', 'this month', or 'next month'.")


def _get_reservations(systems, time_interval, collected_sys):
    """Get the reservations in the given time interval and
    add it to the collected reservations list.

    This is meant to be run in a different thread.

    Parameters:
        systems (list): A list of system instances.
        time_interval (tuple): A tuple of datetimes.
        collected_sys (list): A list of collected systems with reservations.
    """
    for system in systems:
        if any(system.reservations(*time_interval)):
            collected_sys.append(system)
