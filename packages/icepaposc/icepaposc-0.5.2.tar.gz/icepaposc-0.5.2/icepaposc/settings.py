#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# This file is part of IcepapOCS link:
#        https://github.com/ALBA-Synchrotron/IcepapOCS
#
# Copyright 2017:
#       MAX IV Laboratory, Lund, Sweden
#       CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
#
# You should have received a copy of the GNU General Public License
# along with IcepapOCS. If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
from configparser import SafeConfigParser


class Settings:
    """Application settings."""

    def __init__(self):
        """Initializes an instance of class Settings."""
        user_path = os.path.expanduser("~")
        self.conf_file = os.path.join(user_path, ".icepaposc/settings.ini")
        if not os.path.exists(self.conf_file):
            self._create_file(user_path)

        # Settings for collector.
        self.sample_rate_min = 10  # [milliseconds]
        self.sample_rate_max = 1000  # [milliseconds]
        self.dump_rate_min = 1
        self.dump_rate_max = 100

        # Settings for GUI.
        self.default_x_axis_len_min = 5  # [Seconds]
        self.default_x_axis_len_max = 3600  # [Seconds]

        # Settings for auto save.
        self.as_interval_min = 1  # [Minutes]
        self.as_interval_max = 24 * 60  # [Minutes]

        self.sample_rate = 0
        self.dump_rate = 0
        self.default_x_axis_len = 0
        self.use_auto_save = False
        self.use_append = False
        self.as_interval = 5  # [Minutes]
        self.as_folder = user_path

        self._read_file()

    def _create_file(self, user_path):
        icepaosc_folder = os.path.join(user_path, '.icepaposc')
        if not os.path.exists(icepaosc_folder):
            os.mkdir(icepaosc_folder)
        conf = SafeConfigParser()
        conf.add_section('collector')
        conf.add_section('gui')
        conf.add_section('auto_save')
        conf.set('collector', 'tick_interval', '50')  # [milliseconds]
        conf.set('collector', 'sample_buf_len', '2')
        conf.set('gui', 'default_x_axis_len', '30')  # [Seconds]
        conf.set('auto_save', 'use', 'False')
        conf.set('auto_save', 'append', 'False')
        conf.set('auto_save', 'interval', '5')  # [Minutes]
        conf.set('auto_save', 'folder', user_path)
        with open(self.conf_file, 'w') as f:
            conf.write(f)

    def update(self):
        """Called when a setting has been changed."""
        conf = SafeConfigParser()
        conf.read(self.conf_file)
        conf.set('collector', 'tick_interval', str(self.sample_rate))
        conf.set('collector', 'sample_buf_len', str(self.dump_rate))
        conf.set('gui', 'default_x_axis_len', str(self.default_x_axis_len))
        conf.set('auto_save', 'use', str(self.use_auto_save))
        conf.set('auto_save', 'append', str(self.use_append))
        conf.set('auto_save', 'interval', str(self.as_interval))
        conf.set('auto_save', 'folder', str(self.as_folder))
        with open(self.conf_file, 'w') as f:
            conf.write(f)

    def _read_file(self):
        conf = SafeConfigParser()
        conf.read(self.conf_file)
        self.sample_rate = conf.getint('collector', 'tick_interval')
        self.dump_rate = conf.getint('collector', 'sample_buf_len')
        self.default_x_axis_len = conf.getint('gui', 'default_x_axis_len')
        self.use_auto_save = conf.getboolean('auto_save', 'use')
        self.use_append = conf.getboolean('auto_save', 'append')
        self.as_interval = conf.getint('auto_save', 'interval')
        self.as_folder = conf.get('auto_save', 'folder')
