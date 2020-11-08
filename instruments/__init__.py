#!/usr/bin/python

import pyvisa as visa

from instruments import px100


class Instruments:
    def __init__(self):
        self.rm = visa.ResourceManager('@py')
        self.instruments = []
        self.discover()

    def list(self):
        return self.instruments

    def instr(self):
        if self.instruments:
            return self.instruments[0]

    def discover(self):
        print("Detecting instruments...")
        for i in self.rm.list_resources():
            print(i)
            try:
                inst = self.rm.open_resource(i)
            except:
                print("err opening instrument")
                continue

            if not isinstance(inst, visa.resources.Resource):
                continue

            try:
                driver = px100.PX100(inst)  #Todo: loop over drivers if multiple
                if driver.probe():
                    self.instruments.append(driver)
                    print("found " + driver.name)
                else:
                    print("ko")
            except Exception as inst:
                print(type(inst))  # the exception instance
                print(inst.args)  # arguments stored in .args
                print(inst)
                print("err")
                try:
                    inst.close()
                except Exception as inst:
                    print(type(inst))  # the exception instance
                    print(inst.args)  # arguments stored in .args
                    print(inst)
                    print("no close")

        else:
            if len(self.instruments) == 0:
                print("No instruments found")
