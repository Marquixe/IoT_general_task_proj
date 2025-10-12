from states.state import AbstractState
from constants import DHT_PIN, Color
from machine import Pin
from dht import DHT22 as DHT
#import time

class Diagnostics(AbstractState):
    
    def enter(self):
        pass


    def exec(self):
        # try to create sensor
        try:
            pin = Pin(DHT_PIN, Pin.IN)
            sensor = DHT(pin)
            self.device.sensor = sensor
        except Exception as e:
            # failed -> error
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor init failed'))
            return


        # read measure
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
        except Exception:
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor read failed'))
            return


        # validate ranges
        if not (0 <= t <= 50) or not (20 <= h <= 90):
            from .error import Error
            self.device.change_state(Error(self.device, 'Sensor out of range'))
            return


        # OK -> go to Operation
        from .operation import Operation
        self.device.change_state(Operation(self.device))


    def exit(self):
        pass
