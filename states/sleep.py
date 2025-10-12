from .state import AbstractState  # ✅ Relative import
from constants import Color
import sys


class Sleep(AbstractState):

    def enter(self):
        # Turn off LED before sleeping
        if self.device.led:
            self.device.led[0] = Color.OFF
            self.device.led.write()

    def exec(self):
        print('>> Sleep State - shutting down')
        # For now, exit the program
        # Later this will be replaced with actual deep sleep
        sys.exit(0)

    def exit(self):
        pass