#!/usr/bin/python

try:
    import pyvisa as visa
except ModuleNotFoundError:
    visa = None

from instruments.demo import DemoPX100


class Instruments:
    def __init__(self):
        self.instruments = []
        self.rm = None
        if visa is not None:
            try:
                self.rm = visa.ResourceManager('@py')
            except Exception:
                print("Unable to initialize PyVISA resource manager")
        self.discover()

    def list(self):
        return self.instruments

    def instr(self):
        if self.instruments:
            return self.instruments[0]

    def discover(self):
        print("Detecting instruments...")
        if self.rm is None:
            print("PyVISA not available, using demo instrument")
            self.instruments.append(DemoPX100())
            return

        for i in self.rm.list_resources():
            print(i)
            try:
                inst = self.rm.open_resource(i)
            except Exception:
                print("err opening instrument")
                continue

            if not isinstance(inst, visa.resources.Resource):
                continue

            try:
                from instruments import px100
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
                print("No instruments found, using demo instrument")
                self.instruments.append(DemoPX100())
