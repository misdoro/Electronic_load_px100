#!/usr/bin/python
"""
written by Mikhail Doronin
licensed as GPLv3
"""

import time
import math
from datetime import time as tm

from instruments.instrument import Instrument


class PX100(Instrument):

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

    FREQ_VALS = [
        'is_on',
        'voltage',
        'current',
        'time',
        'cap_ah',
    ]

    AUX_VALS = [
        'cap_wh',
        'temp',
        'set_current',
        'set_voltage',
        'set_timer',
    ]

    COMMANDS = {
        Instrument.COMMAND_ENABLE: OUTPUT,
        Instrument.COMMAND_SET_VOLTAGE: SETVCUT,
        Instrument.COMMAND_SET_CURRENT: SETCURR,
        Instrument.COMMAND_SET_TIMER: SETTMR,
        Instrument.COMMAND_RESET: RESETCNT,
    }

    def __init__(self, device):
        print(device)
        self.device = device
        self.name = "PX100"
        self.device.timeout = 500
        self.device.baud_rate = 9600
        self.aux_index = 0
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
        if (self.getVal(PX100.TEMP)):
            return True
        else:
            return False

    def readAll(self):
        print("readAll")
        self.device.clear()
        for key in PX100.FREQ_VALS:
            self.updateVal(key)
        self.updateVal(PX100.AUX_VALS[self.aux_index])
        self.aux_index += 1
        if self.aux_index >= len(PX100.AUX_VALS):
            self.aux_index = 0
        return self.data

    def updateVal(self, key):
        value = self.getVal(PX100.KEY_CMDS[key])
        if (value is not False):
            self.data[key] = value

    def command(self, command, value):
        if command in (PX100.COMMANDS.keys()):
            self.setVal(PX100.COMMANDS[command], value)

    def getVal(self, command):
        ret = self.writeFunction(command, [0, 0])
        if (not ret or len(ret) == 0):
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
            mult = PX100.MUL[command]
        except:
            mult = 1000.

        if (command == PX100.TIME or command == PX100.TIMER):
            hh = ret[2]
            mm = ret[3]
            ss = ret[4]
            return tm(hh, mm, ss)  #'{:02d}:{:02d}:{:02d}'.format(hh, mm, ss)
        else:
            return int.from_bytes(ret[2:5], byteorder='big') / mult

    def setVal(self, command, value):
        if (command == PX100.SETCURR or command == PX100.SETVCUT):
            f, i = math.modf(value)
            value = [int(i), round(f * 100)]
        else:
            value = value.to_bytes(2, byteorder='big')
        ret = self.writeFunction(command, value)
        return ret == 0x6F

    def writeFunction(self, command, value):
        self.constructFrame(command, value)
        self.device.write_raw(bytearray(self.frame))
        if command >= 0x10:
            resp_len = 7
        else:
            resp_len = 1
        try:
            return self.device.read_bytes(resp_len)
        except:
            return False

    def constructFrame(self, command, value):
        self.frame = [0xB1, 0xB2, command, *value, 0xB6]

    def turnOFF(self):
        print("turnoff")
        self.setVal(PX100.OUTPUT, PX100.DISABLED)

    def close(self):
        self.turnOFF()
        time.sleep(.2)
        self.device.close()
