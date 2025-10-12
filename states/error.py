from .state import AbstractState
from constants import Color
import time


class Error(AbstractState):

    def __init__(self, device, error_msg=None):
        super().__init__(device)
        self.error_msg = error_msg
        if error_msg:
            self.device.error_code = error_msg

    def enter(self):
        # Turn LED red to indicate error
        if self.device.led:
            self.device.led[0] = Color.RED
            self.device.led.write()

    def exec(self):
        # Blink LED to indicate error
        # Number of blinks could vary based on error type
        error_blinks = 5

        for _ in range(error_blinks):
            if self.device.led:
                self.device.led[0] = Color.RED
                self.device.led.write()
                time.sleep(0.3)
                self.device.led[0] = Color.OFF
                self.device.led.write()
                time.sleep(0.3)

        print(f'Error: {self.error_msg}')

        # After showing error, go to sleep
        from .sleep import Sleep
        self.device.change_state(Sleep(self.device))

    def exit(self):
        # Turn off LED
        if self.device.led:
            self.device.led[0] = Color.OFF
            self.device.led.write()