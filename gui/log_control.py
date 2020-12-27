from os import path

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QGroupBox, QFileDialog


class LogControl(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(LogControl, self).__init__(*args, **kwargs)
        uic.loadUi("gui/log_control.ui", self)
        self.home = path.expanduser('~')
        self._load_settings()
        self._map_controls()

    def save_settings(self):
        settings = QSettings()

        settings.setValue("LogControl/enabled", self.isChecked())
        settings.setValue("LogControl/path", self.full_path)

        settings.sync()

    def _map_controls(self):
        self.logPath.textChanged.connect(self._path_changed)
        self.selectLogPath.clicked.connect(self._select_path)

    def _load_settings(self):
        settings = QSettings()
        self.setChecked(settings.value("LogControl/enabled", False, type=bool))
        self.full_path = settings.value("LogControl/path", self.home)
        self._display_path(self.full_path)

    def _path_changed(self):
        text = self.logPath.text()
        if path.isdir(text):
            self.full_path = text
            self.pathExists.setText("✓")
        elif path.isdir(path.join(self.home, text)):
            self.full_path = path.join(self.home, text)
            self.pathExists.setText("✓")
        else:
            self.pathExists.setText("")

    def _select_path(self):
        dialog = self.dialog()
        if dialog.exec_():
            s_path = path.normpath(dialog.selectedFiles()[0])
            if path.isdir(s_path):
                self._display_path(s_path)

    def _display_path(self, sel_path):
        try:
            common = path.commonpath([self.home, sel_path])
            print("common {} home {} sel {}".format(common, self.home, sel_path))
            if common == self.home and sel_path != self.home:
                pretty_path = path.relpath(sel_path, start=self.home)
            else:
                pretty_path = sel_path
        except:
            pretty_path = sel_path
        self.logPath.setText(pretty_path)

    def dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setDirectory(self.full_path)
        return dialog
