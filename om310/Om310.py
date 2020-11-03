#!/usr/bin/env python3
import threading
import minimalmodbus
import time
from gpiozero import LED, PWMLED
import yaml


class Om310(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.electric = {'ok': False}
        with open('/etc/om310/config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.instrument = minimalmodbus.Instrument(config['device'].instrument_port, 1)
            self.instrument.serial.baudrate = config['device'].baudrate
            self.instrument.mode = minimalmodbus.MODE_RTU
            self.instrument.TIMEOUT = 0.1
            self.max_current_l1 = config['lines']['l1'].limit
            self.max_current_l2 = config['lines']['l2'].limit
            self.max_current_l3 = config['lines']['l3'].limit
            self.power_control = LED(config['overload_relay'].relay_gpio)
            self.disable_interval_sec = config['overload_relay'].disable_time_sec
            self.disable_start = None
            self.disable_end = None

    def run(self):
        self.polling()

    def update_values(self):
        self.electric = {
            'ok': True,
            'power_overload': False,
            'lines': {
                'freq': self.instrument.read_register(138, 1),
                'l1': {
                    'current': self.instrument.read_register(100, 1),
                    'limit': self.max_current_l1,
                    'overload': False,
                    'voltage': self.instrument.read_register(111, 0),
                    'power': self.instrument.read_register(126, 0) * 10
                },
                'l2': {
                    'current': self.instrument.read_register(101, 1),
                    'limit': self.max_current_l2,
                    'overload': False,
                    'voltage': self.instrument.read_register(112, 0),
                    'power': self.instrument.read_register(126, 0) * 10
                },
                'l3': {
                    'current': self.instrument.read_register(102, 1),
                    'limit': self.max_current_l3,
                    'overload': False,
                    'voltage': self.instrument.read_register(128, 0),
                    'power': self.instrument.read_register(130, 0) * 10
                },
            },
            'control': {
                'power_nominal_kW': self.instrument.read_register(153, 0),
                'power_calc_mode': self.instrument.read_register(154, 0),
                'main_level_percent': self.instrument.read_register(155, 0),
                'additional_level_percent': self.instrument.read_register(156, 0),
                'main_time_to_shutdown_seconds': self.instrument.read_register(157, 0),
                'main_time_to_power_on_minutes': self.instrument.read_register(158, 0)
            }
        }

    def poll_device(self):
        try:
            self.update_values()
            if self.electric["lines"]["l1"]["limit"] < self.electric["lines"]["l1"]["current"]:
                self.electric["lines"]["l1"]["overload"] = True
            else:
                self.electric["lines"]["l1"]["overload"] = False
            if self.electric["lines"]["l2"]["limit"] < self.electric["lines"]["l2"]["current"]:
                self.electric["lines"]["l1"]["overload"] = True
            else:
                self.electric["lines"]["l2"]["overload"] = False
            if self.self.electric["lines"]["l3"]["limit"] < self.electric["lines"]["l3"]["current"]:
                self.electric["lines"]["l1"]["overload"] = True
            else:
                self.electric["lines"]["l3"]["overload"] = False

            if self.electric["lines"]["l1"]["overload"] or self.electric["lines"]["l1"]["overload"] or \
                    self.electric["lines"]["l1"]["overload"]:
                self.disable_start = int(round(time.time(), 0))
                self.disable_end = int(round(time.time(), 0)) + self.disable_interval_sec

        except minimalmodbus.NoResponseError:
            pass

    def polling(self):
        print('Start polling')
        while True:
            time.sleep(1)
            self.poll_device()
            if self.electric["ok"]:
                if self.disable_end is not None:
                    if self.disable_end < int(round(time.time(), 0)):
                        print("Power: overload was ended at: ", self.disable_end)
                        self.disable_end = None
                        self.disable_start = None
                        self.power_control.off()
                    else:
                        self.power_control.on()
