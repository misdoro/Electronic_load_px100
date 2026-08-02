from datetime import time
from time import monotonic

from instruments.instrument import Instrument


class DemoPX100(Instrument):
    COMMANDS = {
        Instrument.COMMAND_ENABLE,
        Instrument.COMMAND_SET_VOLTAGE,
        Instrument.COMMAND_SET_CURRENT,
        Instrument.COMMAND_SET_TIMER,
        Instrument.COMMAND_RESET,
    }

    def __init__(self):
        self.name = "PX100 Demo"
        self.port = "SIM"
        self._start_voltage = 4.2
        self._voltage_drop_per_ah = 0.55
        self._sim_elapsed_s = 0.0
        self._last_tick = monotonic()
        self._timer_seconds = 0
        self.data = {}
        self._reset_cycle()

    def probe(self):
        return True

    def readAll(self):
        now = monotonic()
        dt = max(0.0, now - self._last_tick)
        self._last_tick = now

        if self.data['is_on']:
            self._sim_elapsed_s += dt
            set_current = self.data['set_current']
            dt_hours = dt / 3600.0
            self.data['current'] = set_current
            self.data['cap_ah'] += set_current * dt_hours
            self.data['voltage'] = max(
                self.data['set_voltage'],
                self._start_voltage - self.data['cap_ah'] * self._voltage_drop_per_ah,
            )
            self.data['cap_wh'] += self.data['voltage'] * set_current * dt_hours
            self.data['temp'] = round(min(55.0, 25.0 + set_current * 3.0 + self.data['cap_ah'] * 0.5), 1)

            if self._timer_seconds and self._sim_elapsed_s >= self._timer_seconds:
                self.data['is_on'] = 0.0
                self.data['current'] = 0.0
            elif self.data['voltage'] <= self.data['set_voltage']:
                self.data['is_on'] = 0.0
                self.data['current'] = 0.0
        else:
            self.data['current'] = 0.0

        self.data['time'] = self._seconds_to_time(self._sim_elapsed_s)
        self.data['set_timer'] = self._seconds_to_time(self._timer_seconds)
        return self.data.copy()

    def command(self, command, value):
        if command not in self.COMMANDS:
            return False

        if command == Instrument.COMMAND_ENABLE:
            if value and not self.data['is_on']:
                self._reset_cycle()
                self.data['is_on'] = 1.0
            elif not value:
                self.data['is_on'] = 0.0
                self.data['current'] = 0.0
        elif command == Instrument.COMMAND_SET_CURRENT:
            self.data['set_current'] = round(float(value), 2)
        elif command == Instrument.COMMAND_SET_VOLTAGE:
            self.data['set_voltage'] = round(float(value), 2)
        elif command == Instrument.COMMAND_SET_TIMER:
            self._timer_seconds = value.hour * 3600 + value.minute * 60 + value.second
            self.data['set_timer'] = value
        elif command == Instrument.COMMAND_RESET:
            self._reset_cycle()

        return True

    def close(self):
        self.data['is_on'] = 0.0
        self.data['current'] = 0.0

    def _reset_cycle(self):
        self._sim_elapsed_s = 0.0
        self._last_tick = monotonic()
        self.data = {
            'is_on': 0.0,
            'voltage': self._start_voltage,
            'current': 0.0,
            'time': time(0, 0, 0),
            'cap_ah': 0.0,
            'cap_wh': 0.0,
            'temp': 25.0,
            'set_current': 1.0,
            'set_voltage': 2.9,
            'set_timer': self._seconds_to_time(self._timer_seconds),
        }

    @staticmethod
    def _seconds_to_time(seconds):
        total = max(0, int(round(seconds)))
        total %= 24 * 3600
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return time(hh, mm, ss)
