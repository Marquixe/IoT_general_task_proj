# states/init.py
from states import AbstractState, factory_reset
#from states.configuration import Configuration
#from states.diagnostics import Diagnostics
from machine import Pin
import time
import ujson

try:
    from neopixel import NeoPixel
except Exception:
    NeoPixel = None

class Init(AbstractState):

    def __init__(self, device):
        super().__init__(device)
        self.led = None
        self.btn_pin = None

    def enter(self):
        # init LED if available
        try:
            if NeoPixel:
                self.led = NeoPixel(Pin(NP_PIN, Pin.OUT), 1)
                self.led[0] = Color.GREEN
                self.led.write()
                self.device.led = self.led
        except Exception:
            self.led = None
        # init button
        try:
            self.btn_pin = Pin(20, Pin.IN, Pin.PULL_UP)
            self.device.button = self.btn_pin
        except Exception:
            self.btn_pin = None

    def exec(self):
        # Try reading settings
        s = get_settings()
        self.device.settings = s

        # check button hold duration
        press_time = 0
        if self.btn_pin is None:
            # no button -> go to diagnostics
            from .diagnostics import Diagnostics
            self.device.change_state(Diagnostics(self.device))
            return

        # wait a short window to see if button is pressed
        t0 = time.ticks_ms()
        # if button pressed at start, measure duration
        if self.btn_pin.value() == 0:  # active low
            # measure hold time
            while self.btn_pin.value() == 0:
                press_time = (time.ticks_ms() - t0) / 1000
                # indicate thresholds
                if press_time >= LONG_PRESS_DURATION:
                    if self.led:
                        self.led[0] = Color.ORANGE
                        self.led.write()
                elif press_time >= SHORT_PRESS_DURATION:
                    if self.led:
                        self.led[0] = Color.CYAN
                        self.led.write()
        # choose next state
        if press_time >= LONG_PRESS_DURATION:
            from .factory_reset import FactoryReset
            self.device.change_state(FactoryReset(self.device))
            return
        if press_time >= SHORT_PRESS_DURATION:
            from .configuration import Configuration
            self.device.change_state(Configuration(self.device))
            return

        # otherwise go to diagnostics
        from .diagnostics import Diagnostics
        self.device.change_state(Diagnostics(self.device))

    def exit(self):
        # turn off LED for short blink
        try:
            if self.led:
                self.led[0] = Color.OFF
                self.led.write()
        except Exception:
            pass







# class Init(AbstractState):
#     def __init__(self, device):
#         super().__init__(device)
# 
#     def enter(self):
#         self.button = Pin(14, Pin.IN, Pin.PULL_UP)
#         self.np = neopixel.NeoPixel(Pin(15), 1)
#         self.np[0] = (0, 255, 0)
#         self.np.write()
# 
#     def exec(self):
#         start_time = time.ticks_ms()
#         while not self.button.value():
#             elapsed = time.ticks_diff(time.ticks_ms(), start_time) / 1000
#             if elapsed >= 6:
#                 self.np[0] = (255, 165, 0)
#                 self.np.write()
#                 while not self.button.value():
#                     pass
#                 self.device.change_state(FactoryReset(self.device))
#                 return
#             elif elapsed >= 3:
#                 self.np[0] = (0, 255, 255)
#                 self.np.write()
# 
#         # Načítanie konfigurácie
#         try:
#             with open("config.json", "r") as f:
#                 self.device.settings = ujson.load(f)
#             self.device.change_state(Diagnostics(self.device))
#         except:
#             self.device.change_state(Configuration(self.device))
# 
#     def exit(self):
#         self.np[0] = (0, 0, 0)  # Vypnutie LED
#         self.np.write()