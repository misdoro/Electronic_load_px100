from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QGroupBox

from instruments.instrument import Instrument


class SwCCCV(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(SwCCCV, self).__init__(*args, **kwargs)
        uic.loadUi("gui/swcccv.ui", self)
        self._load_settings()
        self._reset()

    def _load_settings(self):
        settings = QSettings()

        self.setChecked(
            settings.value("SwCCCV/enabled", True, type=bool))
        self.baseCurrent.setValue(
            settings.value("SwCCCV/baseCurrent", 5., type=float))
        self.minCurrent.setValue(
            settings.value("SwCCCV/minCurrent", .4, type=float))
        self.stepMultiplier.setValue(
            settings.value("SwCCCV/stepMultiplier", .9, type=float))
        self.targetVoltage.setValue(
            settings.value("SwCCCV/targetVoltage", 2.9, type=float))

    def save_settings(self):
        settings = QSettings()

        settings.setValue("SwCCCV/enabled", self.isChecked())
        settings.setValue("SwCCCV/baseCurrent", self.baseCurrent.value())
        settings.setValue("SwCCCV/minCurrent", self.minCurrent.value())
        settings.setValue("SwCCCV/stepMultiplier", self.stepMultiplier.value())
        settings.setValue("SwCCCV/targetVoltage", self.targetVoltage.value())

        settings.sync()

    def _reset(self):
        print("swcccv_reset")
        self.tick = 0
        self.action_tick = 0

    def set_backend(self, backend):
        self.backend = backend
        backend.subscribe(self)

    def data_row(self, data, row):
        if data and self.isChecked() and data.lastval('is_on'):
            self.tick += 1

            minCurrent = round(self.minCurrent.value(), 2)
            stepMultiplier = round(self.stepMultiplier.value(), 2)
            targetVoltage = round(self.targetVoltage.value(), 2)
            if (data.lastval('voltage') < targetVoltage) and (
                    data.lastval('set_current') > minCurrent) and self._can_act():
                self.action_tick = self.tick
                new_current = round(
                    max(data.lastval('current') * stepMultiplier, minCurrent),
                    2)
                print("== Software CC-CV ==")
                print("last_voltage {:4.3f} V, targetVoltage {:4.3f} V".format(
                    data.lastval('voltage'), targetVoltage))
                print("new current {:4.3f}A".format(new_current))
                self.backend.send_command(
                    {Instrument.COMMAND_SET_CURRENT: new_current})

    def _can_act(self):
        return self.action_tick + 2 < self.tick
