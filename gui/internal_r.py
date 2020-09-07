from PyQt5.QtWidgets import QWidget, QGroupBox, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QSettings, Qt
from PyQt5 import uic

from datetime import datetime

from pandas import DataFrame

from instruments.instrument import Instrument

MODE_IDLE = 0
MODE_PREPARE = 1
MODE_DROP = 2
MODE_AFTER = 3
ACQ_SIZE = 2
MAX_BAD_ROWS = 3


class InternalRTableModel(QAbstractTableModel):
    def __init__(self):
        super(InternalRTableModel, self).__init__()
        self.reset()

    def append(self, row):
        self.beginInsertRows(QModelIndex(), self.rowCount(1), self.rowCount(1))
        self._data = self._data.append(row, ignore_index=True)
        self.endInsertRows()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def write(self, path, prefix):
        if self.rowCount(1):
            filename = path + "/" + prefix + "_internal_r_" + datetime.now(
            ).isoformat() + ".csv"
            self._data.drop_duplicates().to_csv(filename)

    def reset(self):
        self.beginResetModel()
        self._data = DataFrame(columns=['step', 'r_a', 'r_b'])
        self.endResetModel()

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
        self.resultsTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.load_settings()
        self.reset()

    def load_settings(self):
        settings = QSettings()

        self.setChecked(settings.value("InternalR/enabled", True, type=bool))
        self.v_period = settings.value("InternalR/period", 0.1, type=float)
        self.measurePeriod.setValue(self.v_period)

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
        self._idle()
        self.tableModel.reset()

    def write(self, path, prefix):
        self.tableModel.write(path, prefix)

    def data_row(self, data, row):
        if not self.isChecked() or not self.v_period:
            return

        if self._valid_data(data):
            self._data_loop(data)
        else:
            self.ignored_rows += 1
            if self.ignored_rows > MAX_BAD_ROWS:
                self._idle()

    def _idle(self):
        self.mode = MODE_IDLE
        self.stateLabel.setText('Idle')
        self.pre_current = 0.
        self.ignored_rows = 0
        self.pre_acq = []
        self.zero_acq = []
        self.after_acq = []

    def _data_loop(self, data):
        if self.mode == MODE_IDLE and data.lastval(
                'current') > 0 and self._next_step(data.lastval('voltage')):
            self.mode = MODE_PREPARE
            self.stateLabel.setText('Prepare')
            self.pre_current = data.lastval('set_current')
            self.meas_pre_current = data.lastval('current')
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
        elif self.mode == MODE_AFTER and self._stable_current(data, 0.01):
            self.after_acq.append(data.lastval('voltage'))
            if len(self.after_acq) >= ACQ_SIZE:
                self._calc_r()
                self._idle()

    def _calc_r(self):
        print("-- Internal R --")
        print(self.pre_acq)
        print(self.zero_acq)
        print(self.after_acq)
        print(self.meas_pre_current)

        if self.meas_pre_current > 0:
            r_a = (sum(self.zero_acq) -
                   sum(self.pre_acq)) / (ACQ_SIZE * self.meas_pre_current)
            r_b = (sum(self.zero_acq) -
                   sum(self.after_acq)) / (ACQ_SIZE * self.meas_pre_current)

            row = {
                'step': self.acq_steps[-1],
                'r_a': round(r_a, 4),
                'r_b': round(r_b, 4),
            }
            self.tableModel.append(row)

    def _valid_data(self, data):
        return data and data.lastval('is_on') and self._stable_current(
            data, 0.01)

    def _stable_current(self, data, tolerance):
        return abs(data.lastval('current') -
                   data.lastval('set_current')) < tolerance

    def _next_step(self, volt):
        v_period = self.v_period
        new_step = int(divmod(volt, v_period)[0])
        new_step_value = round((new_step + 1) * v_period, 2)
        if new_step_value not in self.acq_steps:
            self.acq_steps.append(new_step_value)
            return True
        return False
