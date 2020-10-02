from os import path

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QGroupBox, QFileDialog


class LogControl(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(LogControl, self).__init__(*args, **kwargs)
        uic.loadUi("gui/log_control.ui", self)
        self._load_settings()
        self._map_controls()

    def save_settings(self):
        settings = QSettings()

        settings.setValue("LogControl/enabled", self.isChecked())
        settings.setValue("LogControl/path", path.abspath(self.logPath.text()))

        settings.sync()

    def _map_controls(self):
        self.logPath.textChanged.connect(self._path_changed)
        self.selectLogPath.clicked.connect(self._select_path)

    def _load_settings(self):
        settings = QSettings()
        self.setChecked(settings.value("LogControl/enabled", True, type=bool))
        self.full_path = settings.value("LogControl/path", path.abspath("tmp"))
        self.logPath.setText(path.relpath(self.full_path))

    def _path_changed(self):
        full_path = path.abspath(self.logPath.text())
        if path.isdir(full_path):
            self.full_path = full_path
            self.pathExists.setText("✓")
        else:
            self.pathExists.setText("")

    def _select_path(self):
        dialog = self.dialog()
        if dialog.exec_():
            s_path = dialog.selectedFiles()[0]
            if path.isdir(s_path):
                self.full_path = s_path
                self.logPath.setText(path.relpath(self.full_path))

    def dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setDirectory(self.full_path)
        return dialog
