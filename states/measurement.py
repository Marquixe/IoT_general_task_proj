from states import AbstractState
from states.error import Error
from states.wifi_connect import ConnectingToWiFi
import dht
from machine import Pin
import ujson
import time

class Measurement(AbstractState):
    def __init__(self, device):
        super().__init__(device)
        self.name = "Measurement"

    def exec(self):
        # Meranie zo senzora DHT
        try:
            sensor = dht.DHT11(Pin(14))
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()

            # Uloženie dát do súboru
            measurement = {"time": time.time(), "temperature": temp, "humidity": hum}
            measurements = []
            try:
                with open(self.device.settings["measurements_file"], "r") as f:
                    measurements = ujson.load(f)
            except:
                pass
            measurements.append(measurement)
            with open(self.device.settings["measurements_file"], "w") as f:
                ujson.dump(measurements, f)

            self.device.change_state(ConnectingToWiFi(self.device))
        except:
            self.device.error_code = "MEASUREMENT_ERROR"
            self.device.change_state(Error(self.device))