#!/usr/bin/python

import visa

from instruments import px100


class Instruments:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.instruments = []
        print("instruments")
        for i in self.rm.list_resources():
            print(i)
            inst = self.rm.open_resource(i)
            try:
                driver = px100.PX100(
                    inst)  #Todo: loop over drivers if multiple
                if (driver.probe()):
                    self.instruments.append(driver)
                    print("found " + driver.name)
                else:
                    print("ko")
            except:
                print("err")
                inst.close()

    def list(self):
        return self.instruments

    def instr(self):
        return self.instruments[0]
