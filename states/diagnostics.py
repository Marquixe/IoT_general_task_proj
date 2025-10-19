from .state import AbstractState
from constants import DHT_PIN
from machine import Pin
from dht import DHT22 as DHT  #?


class Diagnostics(AbstractState):

    def enter(self):
        pass

    def exec(self):
        # Using old sensor instance
        sensor = self.device.sensor
        if sensor is None:
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor not initialized'))
            return

        # Read measurement
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
        except Exception:
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor read failed'))
            return

        # Validate ranges: 0 <= temp <= 50, 20 <= humidity <= 90
        if not (0 <= t <= 50) or not (20 <= h <= 90):
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor out of range'))
            return

        # All checks passed -> go to Operation
        from .measurement import Measurement
        self.device.change_state(Measurement(self.device))

    def exit(self):
        pass