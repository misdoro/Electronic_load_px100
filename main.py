from instr_thread import InstrumentWorker
from data_store import DataStore
from gui import GUI
from PyQt5.QtCore import QThreadPool

import signal, sys


class Main:
    def __init__(self):
        self.threadpool = QThreadPool()
        self.instr_thread()
        self.datastore = DataStore()
        signal.signal(signal.SIGTERM, self.terminate_process)
        signal.signal(signal.SIGINT, self.terminate_process)
        GUI(self)

    def instr_thread(self):
        self.instr_worker = InstrumentWorker()
        self.instr_worker.signals.data_row.connect(self.data_callback)
        self.threadpool.start(self.instr_worker)
        self.instr_worker.signals.start.emit()

    def data_callback(self, data):
        self.datastore.append(data)

    def send_command(self, command):
        self.instr_worker.signals.command.emit(command)

    def at_exit(self):
        self.instr_worker.signals.exit.emit()
        self.threadpool.waitForDone()
        self.datastore.write('./tmp/')

    def terminate_process(self, signal, _stack):
        self.at_exit()
        sys.exit()


if __name__ == "__main__":
    Main()
