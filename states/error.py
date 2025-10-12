from states.state import AbstractState
from states.sleep import Sleep
from machine import Pin
import time

class Error(AbstractState):
    def __init__(self, device):
        super().__init__(device)

    def enter(self):
        self.led = Pin(15, Pin.OUT)

    def exec(self):
        error_blinks = 3 if self.device.error_code == "SENSOR_FAILURE" else 5
        for _ in range(error_blinks):
            self.led.on()
            time.sleep(0.3)
            self.led.off()
            time.sleep(0.3)

        self.device.change_state(Sleep(self.device))

    def exit(self):
        self.led.off()