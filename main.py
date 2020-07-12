from instruments import Instruments
from data_store import DataStore
from gui import GUI

import time


class Main:
    def __init__(self):
        instruments = Instruments()
        self.instr = instruments.instr()
        self.datastore = DataStore(self.instr.columns())
        self.datastore.append(self.instr.readAll())
        GUI(self)

    def callback(self):
        self.datastore.append(self.instr.readAll())
        return self.datastore.data


if __name__ == "__main__":
    Main()
