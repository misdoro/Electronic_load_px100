from time import sleep

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from instruments import Instruments


class InstrumentSignals(QObject):
    exit = pyqtSignal()
    start = pyqtSignal()
    stop = pyqtSignal()
    data_row = pyqtSignal(dict)
    command = pyqtSignal(dict)


class InstrumentWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = InstrumentSignals()
        self.signals.command.connect(self.add_command)
        self.signals.exit.connect(self.handle_exit)
        self.signals.start.connect(self.handle_start)
        self.signals.stop.connect(self.handle_stop)

        self.loop = True
        self.running = False
        self.commands = []

    @pyqtSlot()
    def run(self):
        instruments = Instruments()
        self.instr = instruments.instr()
        if not self.instr:
            return

        while self.loop:
            if len(self.commands) > 0:
                self.handle_command(self.commands.pop(0))
            if self.running:
                self.signals.data_row.emit(self.instr.readAll())
            sleep(.5)

        self.instr.close()

    def handle_command(self, command):
        for k, v in command.items():
            self.instr.command(k, v)

    def handle_start(self):
        self.running = True

    def handle_stop(self):
        self.running = False

    def handle_exit(self):
        self.loop = False

    def add_command(self, cmd):
        self.commands.append(cmd)
