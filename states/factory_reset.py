from .state import AbstractState
from constants import SETTINGS_FILE
import os
from machine import reset


class FactoryReset(AbstractState):

    def enter(self):
        pass

    def exec(self):
        # Delete settings file to force reconfiguration on next boot
        try:
            os.remove(SETTINGS_FILE)
            print('Settings file deleted')
        except Exception:
            pass  # File might not exist, that's OK

        # Restart device
        print('Restarting device...')
        reset()

    def exit(self):
        pass








# from states.state import AbstractState
# import ujson
# from machine import reset
#
# class FactoryReset(AbstractState):
#     def __init__(self, device):
#         super().__init__(device)
#         self.name = "FactoryReset"
#
#     def exec(self):
#         default_config = {
#             "wifi_ssid": "",
#             "wifi_password": "",
#             "measurements_file": "measurements.json"
#         }
#         with open("config.json", "w") as f:
#             ujson.dump(default_config, f)
#
#         # Reštart zariadenia
#         reset()
