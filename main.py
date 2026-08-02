from multiprocessing import freeze_support
from signal import signal, SIGTERM, SIGINT
from sys import exit

from PySide6.QtCore import QCoreApplication, QThreadPool

from data_store import DataStore
from gui.gui import GUI
from instr_thread import InstrumentWorker


class Main:
    def __init__(self):
        QCoreApplication.setOrganizationName('github.com/misdoro')
        QCoreApplication.setApplicationName('Battery tester')
        self.terminating = False
        self.threadpool = QThreadPool()
        self.instr_thread()
        self.datastore = DataStore()
        signal(SIGTERM, self.terminate_process)
        signal(SIGINT, self.terminate_process)
        self.data_receivers = set()
        self.gui = GUI(self)
        self.gui.run()

    def instr_thread(self):
        self.instr_worker = InstrumentWorker()
        self.instr_worker.signals.data_row.connect(self.data_callback)
        self.instr_worker.signals.status_update.connect(self.status_callback)
        self.threadpool.start(self.instr_worker)
        self.instr_worker.signals.start.emit()

    def subscribe(self, receiver):
        self.data_receivers.add(receiver)

    def data_callback(self, data):
        self.datastore.append(data)
        for r in self.data_receivers:
            r.data_row(self.datastore, data)

    def status_callback(self, status):
        for r in self.data_receivers:
            if hasattr(r, 'status_update'):
                r.status_update(status)

    def send_command(self, command):
        self.instr_worker.signals.command.emit(command)

    def at_exit(self):
        self.instr_worker.signals.exit.emit()
        self.threadpool.waitForDone()

    def terminate_process(self, signal, _stack):
        if self.terminating:
            return
        self.terminating = True
        if hasattr(self, 'gui') and hasattr(self.gui, 'window'):
            try:
                self.gui.window.write_logs()
            except Exception as e:
                print(f"Error writing logs during termination: {e}")
        self.at_exit()
        exit()


if __name__ == "__main__":
    freeze_support()
    Main()
