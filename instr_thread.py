from time import sleep

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from instruments import Instruments


class InstrumentSignals(QObject):
    exit = pyqtSignal()
    start = pyqtSignal()
    stop = pyqtSignal()
    data_row = pyqtSignal(dict)
    status_update = pyqtSignal(str)
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
            self.signals.status_update.emit("No devices found")
            return

        self.signals.status_update.emit("Connected to {} on {}".format(self.instr.name, self.instr.port))

        consecutive_errors = 0
        max_consecutive_errors = 10

        while self.loop:
            if len(self.commands) > 0:
                self.handle_command(self.commands.pop(0))

            if self.running:
                try:
                    data = self.instr.readAll()
                    if data:  # Only emit if we got valid data
                        self.signals.data_row.emit(data)
                        consecutive_errors = 0  # Reset error counter on success
                    else:
                        consecutive_errors += 1
                except Exception as e:
                    consecutive_errors += 1
                    if consecutive_errors % 5 == 1:  # Print every 5th error
                        print(f"Data read error (consecutive: {consecutive_errors}): {e}")

                    # If too many consecutive errors, try to reconnect
                    if consecutive_errors >= max_consecutive_errors:
                        print("Too many consecutive errors, attempting reconnection...")
                        try:
                            self.instr.close()
                            sleep(1)
                            instruments = Instruments()
                            new_instr = instruments.instr()
                            if new_instr:
                                self.instr = new_instr
                                consecutive_errors = 0
                                self.signals.status_update.emit("Reconnected to device")
                            else:
                                self.signals.status_update.emit("Reconnection failed")
                        except:
                            print("Reconnection attempt failed")

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
