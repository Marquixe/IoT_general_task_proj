from .state import AbstractState
from constants import MEASUREMENTS_FILE
import ujson
import time


class Measurement(AbstractState):

    def enter(self):
        pass

    def exec(self):
        try:
            sensor = self.device.sensor
            time.sleep(2)
            sensor.measure()
            time.sleep(0.1)
            temp = sensor.temperature()
            hum = sensor.humidity()

            measurement = {
                "time": time.time(),
                "temperature": temp,
                "humidity": hum
            }

            # Load existing measurements
            measurements = []
            try:
                with open(MEASUREMENTS_FILE, "r") as f:
                    measurements = ujson.load(f)
            except:
                pass  # File doesn't exist yet

            # Append new measurement
            measurements.append(measurement)

            # Save back to file
            with open(MEASUREMENTS_FILE, "w") as f:
                ujson.dump(measurements, f)

            print(f'Sensor: {sensor is not None}, Measured: {temp}°C, {hum}%')

            # Try to connect to WiFi to publish data
            from .connecting_wifi import ConnectingWiFi
            self.device.change_state(ConnectingWiFi(self.device))

        except Exception as e:
            from .error import Error
            self.device.change_state(Error(self.device, f'Measurement failed: {e}'))

    def exit(self):
        pass