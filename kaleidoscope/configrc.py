# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

"""Configrc file functionality"""

import os
import warnings
import configparser


def has_kal_rc():
    """
    Checks to see if the kalrc file exists in the default
    location, i.e. HOME/.kaleidoscope/kalrc
    """
    kal_conf_dir = os.path.join(os.path.expanduser("~"), '.kaleidoscope')
    if os.path.exists(kal_conf_dir):
        kal_rc_file = os.path.join(kal_conf_dir,'kalrc')
        rc_exists = os.path.isfile(kal_rc_file) 
        if rc_exists:
            return True, kal_rc_file
        else:
            return False, None
    else:
        return False, None


def generate_kal_rc():
    """
    Generate a blank kalrc file.
    """
    # Check for write access to home dir
    if not os.access(os.path.expanduser("~"), os.W_OK):
        return False
    kal_conf_dir = os.path.join(os.path.expanduser("~"), '.kaleidoscope')
    if not os.path.exists(kal_conf_dir):
        try:
            os.mkdir(kal_conf_dir)
        except Exception:  # pylint: disable=broad-except
            warnings.warn('Cannot write config file to user home dir.')
            return False
    kal_rc_file = os.path.join(kal_conf_dir, 'kalrc')
    rc_exists = os.path.isfile(kal_rc_file)
    if rc_exists:
        #Do not overwrite
        return False
    else:
        #Write a basic file with qutip section
        cfgfile = open(kal_rc_file, 'w')
        config = configparser.ConfigParser()
        config.add_section('kaleidoscope')
        config.write(cfgfile)
        cfgfile.close()
        return True


def has_rc_key(rc_file, key):
    """Checks if a given key exists in
    a given rc_file.

    Parameters:
        rc_file (str): Specified rc file.
        key (str): The key.

    Returns:
        bool: Does the key exist.

    Raises:
        NoSectionError: Kaleidoscope section does
                        not exist.
    """
    config = configparser.ConfigParser()
    config.read(rc_file)
    if config.has_section('kaleidoscope'):
        opts = config.options('kaleidoscope')
        return key in opts
    else:
        raise configparser.NoSectionError('kaleidoscope')


def write_rc_key(rc_file, key, value):
    """
    Writes a single key value to the qutiprc file

    Parameters:
        rc_file (str): String specifying file location.
        key (str): The key name to be written.
        value (str): Value corresponding to given key.
    """
    if not os.access(os.path.expanduser("~"), os.W_OK):
        return
    cfgfile = open(rc_file, 'w')
    config = configparser.ConfigParser()
    if not config.has_section('kaleidoscope'):
        config.add_section('kaleidoscope')
    config.set('kaleidoscope', key, value)
    config.write(cfgfile)
    cfgfile.close()
