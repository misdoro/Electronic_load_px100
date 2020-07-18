class Instrument:
    COMMAND_ENABLE = 'cmd_enable'
    COMMAND_SET_VOLTAGE = 'cmd_set_voltage'
    COMMAND_SET_CURRENT = 'cmd_set_current'
    COMMAND_SET_TIMER = 'cmd_set_timer'
    COMMAND_RESET = 'cmd_reset'

    def probe(self):
        pass

    def readAll(self):
        pass

    def command(self):
        pass
