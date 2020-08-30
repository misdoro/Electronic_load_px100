import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, uic

from PyQt5.QtCore import (
    QSettings,
    Qt,
    QSize,
    QPoint,
    QTime,
    QTimer,
)

from PyQt5.QtWidgets import (
    QWidget,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from datetime import time

from instruments.instrument import Instrument
from gui.swcccv import SwCCCV
from gui.internal_r import InternalR


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('gui/main.ui', self)
        self.load_settings()

        self.plot_placeholder.setLayout(self.plot_layout())
        self.map_controls()
        self.tab2 = uic.loadUi("gui/settings.ui")
        self.swCCCV = SwCCCV()
        self.internal_r = InternalR()
        self.controlsLayout.insertWidget(3, self.internal_r)
        self.tab2.layout().addWidget(self.swCCCV)
        self.tabs.addTab(self.tab2, "Settings")
        self.show()

    def plot_layout(self):
        self.canvas = MplCanvas(self, width=8, height=4, dpi=100)
        self.ax = self.canvas.axes
        self.twinax = self.ax.twinx()

        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        return layout

    def map_controls(self):
        self.en_checkbox.stateChanged.connect(self.enabled_changed)
        self.set_voltage.valueChanged.connect(self.voltage_changed)
        self.set_current.valueChanged.connect(self.current_changed)
        self.set_timer.timeChanged.connect(self.timer_changed)
        self.resetButton.clicked.connect(self.reset_dev)

        self.set_voltage_timer = QTimer(singleShot=True,
                                        timeout=self.voltage_set)
        self.set_current_timer = QTimer(singleShot=True,
                                        timeout=self.current_set)
        self.set_timer_timer = QTimer(singleShot=True, timeout=self.timer_set)

    def data_row(self, data, row):
        if data:
            set_voltage = data.lastval('set_voltage')
            if not self.set_voltage.hasFocus():
                self.set_voltage.setValue(set_voltage)

            set_current = data.lastval('set_current')
            if not self.set_current.hasFocus():
                self.set_current.setValue(set_current)

            is_on = data.lastval('is_on')
            if is_on:
                self.en_checkbox.setCheckState(Qt.Checked)
            else:
                self.en_checkbox.setCheckState(Qt.Unchecked)

            voltage = data.lastval('voltage')
            current = data.lastval('current')
            self.setWindowTitle("Battery tester {:4.2f}V {:4.2f}A ".format(
                voltage, current))
            self.readVoltage.setText("{:5.3f} V".format(voltage))
            self.readCurrent.setText("{:5.3f} A".format(current))
            self.readCapAH.setText("{:5.3f} AH".format(data.lastval('cap_ah')))
            self.readCapWH.setText("{:5.3f} WH".format(data.lastval('cap_wh')))
            self.readTime.setText(data.lastval('time').strftime("%H:%M:%S"))

            xlim = (time(0), max([time(0, 1, 0), data.lastval('time')]))
            self.ax.cla()
            self.twinax.cla()
            data.plot(ax=self.ax, x='time', y=['voltage'], xlim=xlim)
            self.ax.legend(loc='center left')
            self.ax.set_ylabel('Voltage, V')
            self.ax.set_ylim(bottom=set_voltage)
            data.plot(ax=self.twinax, x='time', y=['current'], style='r')
            self.twinax.legend(loc='center right')
            self.twinax.set_ylabel('Current, A')
            self.twinax.set_ylim(0, 10)
            self.canvas.draw()

    def set_backend(self, backend):
        self.backend = backend
        backend.subscribe(self)
        self.swCCCV.set_backend(backend)
        self.internal_r.set_backend(backend)

    def closeEvent(self, event):
        self.swCCCV.save_settings()
        self.internal_r.save_settings()
        self.save_settings()
        self.internal_r.write('./tmp', self.cellLabel.text())
        self.backend.datastore.write('./tmp', self.cellLabel.text())
        self.backend.at_exit()
        event.accept()

    def enabled_changed(self):
        if self.en_checkbox.hasFocus():
            value = self.en_checkbox.isChecked()
            self.en_checkbox.clearFocus()
            self.backend.send_command({Instrument.COMMAND_ENABLE: value})

    def voltage_changed(self):
        if self.set_voltage.hasFocus():
            self.set_voltage_timer.start(1000)

    def voltage_set(self):
        value = round(self.set_voltage.value(), 2)
        self.set_voltage.clearFocus()
        self.backend.send_command({Instrument.COMMAND_SET_VOLTAGE: value})

    def current_changed(self):
        if self.set_current.hasFocus():
            self.set_current_timer.start(1000)

    def current_set(self):
        value = round(self.set_current.value(), 2)
        self.set_current.clearFocus()
        self.backend.send_command({Instrument.COMMAND_SET_CURRENT: value})

    def timer_changed(self):
        if self.set_timer.hasFocus():
            self.set_timer_timer.start(1000)

    def timer_set(self):
        set_time = self.set_timer.time()
        value = time(set_time.hour(), set_time.minute(), set_time.second())
        self.set_timer.clearFocus()
        self.backend.send_command({Instrument.COMMAND_SET_TIMER: value})

    def reset_dev(self, s):
        self.resetButton.clearFocus()
        self.swCCCV.reset()
        self.internal_r.write('./tmp', self.cellLabel.text())
        self.backend.datastore.write('./tmp', self.cellLabel.text())
        self.internal_r.reset()
        self.backend.datastore.reset()
        self.backend.send_command({Instrument.COMMAND_RESET: 0.0})

    def load_settings(self):
        settings = QSettings()

        self.resize(settings.value("MainWindow/size", QSize(1024, 600)))
        self.move(settings.value("MainWindow/pos", QPoint(0, 0)))
        self.cellLabel.setText(settings.value("MainWindow/cellLabel",
                                              'Cell x'))

    def save_settings(self):
        settings = QSettings()

        settings.setValue("MainWindow/size", self.size())
        settings.setValue("MainWindow/pos", self.pos())
        settings.setValue("MainWindow/cellLabel", self.cellLabel.text())

        settings.sync()


class GUI:
    def __init__(self, backend):
        app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.set_backend(backend)
        app.exec_()
