from .state import AbstractState
from constants import MEASUREMENTS_FILE
from helpers import convert_temp
import ujson
import time


class Operation(AbstractState):

    def enter(self):
        pass

    def exec(self):
        try:
            # Use the sensor already initialized in Diagnostics
            sensor = self.device.sensor
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()

            # Convert temperature based on user settings
            temp_converted = convert_temp(temp, self.device.settings.units)  # ✅ FIXED: use .units not ["units"]

            # Create measurement record
            measurement = {
                "time": time.time(),
                "temperature": temp_converted,
                "humidity": hum,
                "units": self.device.settings.units
            }

            # Load existing measurements
            measurements = []
            try:
                with open(MEASUREMENTS_FILE, "r") as f:  # ✅ FIXED: use constant
                    measurements = ujson.load(f)
            except:
                pass  # File doesn't exist yet

            # Append new measurement
            measurements.append(measurement)

            # Save back to file
            with open(MEASUREMENTS_FILE, "w") as f:
                ujson.dump(measurements, f)

            print(f'Measurement saved: {temp_converted}°, {hum}%')

            # After successful measurement, go to sleep
            from .sleep import Sleep  # ✅ ADDED: transition to sleep
            self.device.change_state(Sleep(self.device))

        except Exception as e:
            # On any error during measurement, go to error state
            from .error import Error
            self.device.change_state(Error(self.device, 'Measurement failed'))

    def exit(self):
        pass