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

from PyQt5 import QtWidgets, uic
import os
from pkg_resources import resource_filename


class DialogSettings(QtWidgets.QDialog):

    def __init__(self, parent, settings):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        ui_filename = resource_filename('icepaposc.ui',
                                        'dialog_settings.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.settings = settings
        self.apply_button = self.ui.bbApplyClose.button(
            QtWidgets.QDialogButtonBox.Apply)
        self.close_button = self.ui.bbApplyClose.button(
            QtWidgets.QDialogButtonBox.Close)
        self._connect_signals()
        self._update_gui_rate()
        self.ui.sbSampleRate.setMinimum(self.settings.sample_rate_min)
        self.ui.sbSampleRate.setMaximum(self.settings.sample_rate_max)
        self.ui.sbSampleRate.setValue(self.settings.sample_rate)
        self.ui.sbDumpRate.setMinimum(self.settings.dump_rate_min)
        self.ui.sbDumpRate.setMaximum(self.settings.dump_rate_max)
        self.ui.sbDumpRate.setValue(self.settings.dump_rate)
        self.ui.sbLenAxisX.setMinimum(self.settings.default_x_axis_len_min)
        self.ui.sbLenAxisX.setMaximum(self.settings.default_x_axis_len_max)
        self.ui.sbLenAxisX.setValue(self.settings.default_x_axis_len)
        self.ui.cbUseAutoSave.setChecked(self.settings.use_auto_save)
        self.ui.cbAppend.setChecked(self.settings.use_append)
        self.ui.sbAutoSaveInterval.setMinimum(self.settings.as_interval_min)
        self.ui.sbAutoSaveInterval.setMaximum(self.settings.as_interval_max)
        self.ui.sbAutoSaveInterval.setValue(self.settings.as_interval)
        self.ui.leDataFolder.setText(self.settings.as_folder)
        self._as_state_changed()
        self.apply_button.setDisabled(True)

    def _connect_signals(self):
        self.ui.sbSampleRate.valueChanged.connect(self._sample_rate_changed)
        self.ui.sbDumpRate.valueChanged.connect(self._dump_rate_changed)
        self.ui.sbLenAxisX.valueChanged.connect(self._x_axis_length_changed)
        self.ui.cbUseAutoSave.stateChanged.connect(self._as_state_changed)
        self.ui.cbAppend.stateChanged.connect(self._append_changed)
        self.ui.sbAutoSaveInterval.valueChanged.connect(self._as_intvl_changed)
        self.ui.btnOpenFolderDlg.clicked.connect(self._launch_folder_dialog)
        self.ui.leDataFolder.textChanged.connect(self._set_apply_state)
        self.apply_button.clicked.connect(self._apply)
        self.close_button.clicked.connect(self.close)

    def _sample_rate_changed(self):
        self._update_gui_rate()
        self._set_apply_state()

    def _dump_rate_changed(self):
        self._update_gui_rate()
        self._set_apply_state()

    def _x_axis_length_changed(self):
        self._set_apply_state()

    def _set_apply_state(self):
        eq = self.ui.sbSampleRate.value() == self.settings.sample_rate and \
           self.ui.sbDumpRate.value() == self.settings.dump_rate and \
           self.ui.sbLenAxisX.value() == self.settings.default_x_axis_len and \
           self.ui.cbUseAutoSave.isChecked() == \
           self.settings.use_auto_save and \
           self.ui.cbAppend.isChecked() == self.settings.use_append and \
           self.ui.sbAutoSaveInterval.value() == \
           self.settings.as_interval and \
           self.ui.leDataFolder.text() == self.settings.as_folder
        self.apply_button.setDisabled(eq)

    def _update_gui_rate(self):
        update_rate = self.ui.sbSampleRate.value() * self.ui.sbDumpRate.value()
        self.ui.leGuiUpdateRate.setText(str(update_rate))

    def _as_state_changed(self):
        use = self.ui.cbUseAutoSave.isChecked()
        self.ui.cbAppend.setEnabled(use)
        self.ui.sbAutoSaveInterval.setEnabled(use)
        self.ui.leDataFolder.setEnabled(use)
        self.ui.btnOpenFolderDlg.setEnabled(use)
        self._set_apply_state()

    def _append_changed(self):
        self._set_apply_state()

    def _as_intvl_changed(self):
        self._set_apply_state()

    def _launch_folder_dialog(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_name:
            self.ui.leDataFolder.setText(folder_name)
            self._set_apply_state()

    def _apply(self):
        auto_save_folder = self.ui.leDataFolder.text()
        if not self._is_valid_folder(auto_save_folder):
            return
        self.settings.sample_rate = self.ui.sbSampleRate.value()
        self.settings.dump_rate = self.ui.sbDumpRate.value()
        self.settings.default_x_axis_len = self.ui.sbLenAxisX.value()
        self.settings.use_auto_save = self.ui.cbUseAutoSave.isChecked()
        self.settings.use_append = self.ui.cbAppend.isChecked()
        self.settings.as_interval = self.ui.sbAutoSaveInterval.value()
        self.settings.as_folder = auto_save_folder
        self.settings.update()
        self.parent.settings_updated()
        self.apply_button.setDisabled(True)

    @staticmethod
    def _is_valid_folder(folder):
        # Make sure path exists.
        if not os.path.exists(folder):
            msg = 'Folder does not exist: {}\n'.format(folder)
            print(msg)
            QtWidgets.QMessageBox.critical(None, 'Set Data Folder', msg)
            return False
        # Create a dummy file name (hopefully unique for our test).
        fn = folder + '/IcePapOSCfolderTest.txt'
        # Create the dummy file for reading and writing.
        try:
            open(fn, "w+")
        except Exception as e:
            msg = 'Failed to create test file: {}\n{}'.format(fn, e)
            print(msg)
            QtWidgets.QMessageBox.critical(None, 'Bad Folder', msg)
            return False
        # Delete the dummy file.
        try:
            os.remove(fn)
        except OSError as e:
            msg = 'Failed to remove test file: {}\n{}'.format(fn, e)
            print(msg)
            QtWidgets.QMessageBox.critical(None, 'Remove Test File', msg)
            return False
        return True

    def done(self, r):
        """Overload of QDialog.done()."""
        self.parent.enable_action()
        QtWidgets.QDialog.done(self, r)
