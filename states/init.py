from .state import AbstractState
from constants import NP_PIN, BTN_PIN, SHORT_PRESS_DURATION, LONG_PRESS_DURATION, Color
from helpers import get_settings
from machine import Pin
import time

try:
    from neopixel import NeoPixel
except ImportError:
    NeoPixel = None


class Init(AbstractState):
    def __init__(self, device):
        super().__init__(device)
        self.led = None
        self.btn_pin = None

    def enter(self):
        # Initialize LED if available
        try:
            if NeoPixel:
                self.led = NeoPixel(Pin(NP_PIN, Pin.OUT), 1)
                self.led[0] = Color.GREEN
                self.led.write()
                self.device.led = self.led
        except Exception:
            self.led = None

        # Initialize button
        try:
            self.btn_pin = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
            self.device.button = self.btn_pin
        except Exception:
            self.btn_pin = None

    def exec(self):
        # Try reading settings
        try:
            s = get_settings()
            self.device.settings = s
        except Exception:
            # If settings don't exist or are invalid, go to Configuration
            from .configuration import Configuration
            self.device.change_state(Configuration(self.device))
            return

        # Check button hold duration
        press_time = 0

        if self.btn_pin is None:
            # No button available -> go directly to diagnostics
            from .diagnostics import Diagnostics
            self.device.change_state(Diagnostics(self.device))
            return

        # Check if button is pressed at start
        if self.btn_pin.value() == 0:  # Active low (button pressed)
            t0 = time.ticks_ms()

            # Measure hold time
            while self.btn_pin.value() == 0:
                press_time = (time.ticks_ms() - t0) / 1000

                # Indicate thresholds with LED color changes
                if press_time >= LONG_PRESS_DURATION:
                    if self.led:
                        self.led[0] = Color.ORANGE
                        self.led.write()
                elif press_time >= SHORT_PRESS_DURATION:
                    if self.led:
                        self.led[0] = Color.CYAN
                        self.led.write()

        # Choose next state based on press duration
        if press_time >= LONG_PRESS_DURATION:
            from .factory_reset import FactoryReset
            self.device.change_state(FactoryReset(self.device))
        elif press_time >= SHORT_PRESS_DURATION:
            from .configuration import Configuration
            self.device.change_state(Configuration(self.device))
        else:
            # No press or very short press -> go to diagnostics
            from .diagnostics import Diagnostics
            self.device.change_state(Diagnostics(self.device))

    def exit(self):
        pass  # LED color will be changed by next state