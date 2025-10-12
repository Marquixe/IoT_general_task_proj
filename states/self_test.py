from states import AbstractState
from states.error import Error
from states.measurement import Measurement
import time
import dht
from machine import Pin

class SelfTests(AbstractState):
    def __init__(self, device):
        super().__init__(device)

    def enter(self):
        self.led = Pin(15, Pin.OUT)
        self.led.on()

    def exec(self):
        self.led.on()
        time.sleep(0.5)
        self.led.off()

        try:
            sensor = dht.DHT11(Pin(14))
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()

            if not (0 <= temp <= 50) or not (20 <= hum <= 90):
                self.device.error_code = "INVALID_SENSOR_DATA"
                self.device.change_state(Error(self.device))
                return
        except Exception as e:
            self.device.error_code = "SENSOR_FAILURE"
            self.device.change_state(Error(self.device))
            return

        self.device.change_state(Measurement(self.device))

    def exit(self):
        self.led.off()