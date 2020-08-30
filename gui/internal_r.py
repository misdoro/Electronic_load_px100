from PyQt5.QtWidgets import QWidget, QGroupBox, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QSettings, Qt
from PyQt5 import uic

from pandas import DataFrame

from instruments.instrument import Instrument

MODE_IDLE = 0
MODE_PREPARE = 1
MODE_DROP = 2
MODE_AFTER = 3
ACQ_SIZE = 2


class InternalRTableModel(QAbstractTableModel):
    def __init__(self):
        super(InternalRTableModel, self).__init__()
        self.reset()

    def append(self, row):
        self._data = self._data.append(row, ignore_index=True)
        print(self._data)
        print(self.rowCount(1))
        self.beginInsertRows(QModelIndex(),
                             self.rowCount(1) - 1,
                             self.rowCount(1) - 1)
        self.endInsertRows()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def reset(self):
        self._data = DataFrame(columns=['step', 'r_a', 'r_b'])

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class InternalR(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(InternalR, self).__init__(*args, **kwargs)
        uic.loadUi("gui/internal_r.ui", self)
        self.measurePeriod.valueChanged.connect(self.param_changed)
        self.tableModel = InternalRTableModel()
        self.resultsTable.setModel(self.tableModel)
        self.resultsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        self.load_settings()
        self.reset()

    def load_settings(self):
        settings = QSettings()

        self.setChecked(settings.value("InternalR/enabled", True, type=bool))
        self.measurePeriod.setValue(
            settings.value("InternalR/period", 0.1, type=float))

    def save_settings(self):
        settings = QSettings()

        settings.setValue("InternalR/enabled", self.isChecked())
        settings.setValue("InternalR/period", self.measurePeriod.value())

        settings.sync()

    def param_changed(self):
        self.v_period = self.measurePeriod.value()

    def set_backend(self, backend):
        self.backend = backend
        backend.subscribe(self)

    def reset(self):
        self.acq_steps = []
        self.idle()
        self.tableModel.reset()

    def idle(self):
        self.mode = MODE_IDLE
        self.stateLabel.setText('Idle')
        self.pre_current = 0.
        self.pre_acq = []
        self.zero_acq = []
        self.after_acq = []

    def data_row(self, data, row):
        if data and self.isChecked() and data.lastval('is_on'):
            if self.mode == MODE_IDLE and data.lastval(
                    'current') > 0 and self._next_step(
                        data.lastval('voltage')):
                self.mode = MODE_PREPARE
                self.stateLabel.setText('Prepare')
                self.pre_current = data.lastval('set_current')
                self.pre_acq.append(data.lastval('voltage'))
            elif self.mode == MODE_PREPARE:
                self.pre_acq.append(data.lastval('voltage'))
                if len(self.pre_acq) >= ACQ_SIZE:
                    self.mode = MODE_DROP
                    self.stateLabel.setText('Drop')
                    self.backend.send_command(
                        {Instrument.COMMAND_SET_CURRENT: 0.0})
            elif self.mode == MODE_DROP and data.lastval('current') == 0.:
                self.zero_acq.append(data.lastval('voltage'))
                if len(self.zero_acq) >= ACQ_SIZE:
                    self.mode = MODE_AFTER
                    self.stateLabel.setText('Ramp-up')
                    self.backend.send_command(
                        {Instrument.COMMAND_SET_CURRENT: self.pre_current})
            elif self.mode == MODE_AFTER and round(
                    data.lastval('current'), 1) == round(self.pre_current, 1):
                self.after_acq.append(data.lastval('voltage'))
                if len(self.after_acq) >= ACQ_SIZE:
                    self.calc_r()
                    self.idle()

    def calc_r(self):
        print("-- Internal R --")
        print(self.pre_acq)
        print(self.zero_acq)
        print(self.after_acq)
        print(self.pre_current)

        r_a = (sum(self.zero_acq) - sum(self.pre_acq)) / (ACQ_SIZE *
                                                          self.pre_current)
        r_b = (sum(self.zero_acq) - sum(self.after_acq)) / (ACQ_SIZE *
                                                            self.pre_current)

        row = {
            'step': round((self.acq_steps[-1] + 1) * self.v_period, 2),
            'r_a': round(r_a, 4),
            'r_b': round(r_b, 4),
        }
        self.tableModel.append(row)

    def _next_step(self, volt):
        new_step = int(divmod(volt, self.v_period)[0])
        if new_step not in self.acq_steps:
            self.acq_steps.append(new_step)
            return True
        return False
