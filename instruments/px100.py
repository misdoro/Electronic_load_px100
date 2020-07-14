#!/usr/bin/python
"""
written by Mikhail Doronin
licensed as GPLv3
"""

import time
import math
from datetime import time as tm

ISON = 0x10
VOLTAGE = 0x11
CURRENT = 0x12
TIME = 0x13
CAP_AH = 0x14
CAP_WH = 0x15
TEMP = 0x16
LIM_CURR = 0x17
LIM_VOLT = 0x18
TIMER = 0x19

OUTPUT = 0x01
SETCURR = 0x02
SETVCUT = 0x03
SETTMR = 0x04
RESETCNT = 0x05

ENABLED = 0x0100
DISABLED = 0x0000

MUL = {
    ISON: 1,
    VOLTAGE: 1000.,
    CURRENT: 1000.,
    CAP_AH: 1000.,
    CAP_WH: 1000.,
    TEMP: 1,
    LIM_CURR: 100.,
    LIM_VOLT: 100.,
}

KEY_CMDS = {
    'is_on': ISON,
    'voltage': VOLTAGE,
    'current': CURRENT,
    'time': TIME,
    'cap_ah': CAP_AH,
    'cap_wh': CAP_WH,
    'temp': TEMP,
    'set_current': LIM_CURR,
    'set_voltage': LIM_VOLT,
    'set_timer': TIMER,
}


class PX100:
    def __init__(self, device):
        print(device)
        self.device = device
        self.name = "PX100"
        self.device.timeout = 1000
        self.data = {
            'is_on': 0.,
            'voltage': 0.,
            'current': 0.,
            'time': tm(0),
            'cap_ah': 0.,
            'cap_wh': 0.,
            'temp': 0,
            'set_current': 0.,
            'set_voltage': 0.,
            'set_timer': tm(0),
        }

    def probe(self):
        print("probe")
        if (self.getVal(TEMP)):
            return True
        else:
            return False

    def columns(self):
        self.data.keys()

    def readAll(self):
        for key in self.data.keys():
            self.updateVal(key)
        return self.data

    def updateVal(self, key):
        value = self.getVal(KEY_CMDS[key])
        if (value is not False):
            self.data[key] = value

    def getVal(self, command):
        ret = self.writeFunction(command, [0, 0])
        if (len(ret) == 0):
            print("no answer")
            return False
        elif (len(ret) == 1 and ret[0] == 0x6F):
            print("setval")
            return False
        elif (len(ret) < 7 or ret[0] != 0xCA or ret[1] != 0xCB
              or ret[5] != 0xCE or ret[6] != 0xCF):
            print("Receive error")
            return False

        try:
            mult = MUL[command]
        except:
            mult = 1000.

        if (command == TIME or command == TIMER):
            hh = ret[2]
            mm = ret[3]
            ss = ret[4]
            return tm(hh, mm, ss)  #'{:02d}:{:02d}:{:02d}'.format(hh, mm, ss)
        else:
            return int.from_bytes(ret[2:5], byteorder='big') / mult

    def setVal(self, command, value):
        if (command == SETCURR or command == SETVCUT):
            f, i = math.modf(value)
            value = [int(i), round(f * 100)]
        else:
            value = value.to_bytes(2, byteorder='big')
        ret = self.writeFunction(command, value)
        #print(ret)
        time.sleep(0.5)
        return ret == 0x6F

    def clear(self):
        try:
            self.device.clear()
        except:
            return

    def writeFunction(self, command, value):
        self.constructFrame(command, value)
        self.device.write_raw(bytearray(self.frame))
        time.sleep(.1)
        return self.device.read_bytes(self.device.bytes_in_buffer)

    def constructFrame(self, command, value):
        self.frame = [0xB1, 0xB2, command, *value, 0xB6]
        #print(self.frame)

    def setMode(self, mode):
        print(mode)

    def setVoltage(self, voltage):
        print(voltage)

    def setCurrent(self, current):
        self.amperage = current
        print(current)

    def getCurrent(self):
        print("getCurrent")
        self.amperage = self.getVal(CURRENT)
        return self.amperage

    def getVoltage(self):
        print("getVoltage")
        self.voltage = self.getVal(VOLTAGE)
        print(self.voltage)
        return self.voltage

    def getIdentifier(self):
        return self.name

    def getPower(self):
        print("getPower")
        self.power = self.voltage * self.amperage
        return self.power

    def setOutput(self, state):
        print("SetOut")
        print(state)
        self.output = state
        if (state):
            self.turnON()
        else:
            self.turnOFF()

    def turnON(self):
        print("turnon")
        self.setVal(OUTPUT, ENABLED)

    def turnOFF(self):
        print("turnoff")
        self.setVal(OUTPUT, DISABLED)

    def quit(self):
        self.turnOFF()
        time.sleep(.2)
        self.device.close()
