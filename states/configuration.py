from .state import AbstractState
from constants import Color
import machine
import time


class Configuration(AbstractState):

    def enter(self):
        # Set RGB LED to CYAN when entering configuration mode
        if self.device.led:
            self.device.led[0] = Color.CYAN
            self.device.led.write()

    def exec(self):
        print('>> Configuration State')
        # TODO: Set up Access Point and web server here
        # For now, simulate configuration with timeout
        time.sleep(60)  # Wait 60 seconds for configuration

        # After configuration or timeout, restart the device
        machine.reset()

    def exit(self):
        pass