from states.state import AbstractState
import ujson
from machine import reset

class FactoryReset(AbstractState):
    def __init__(self, device):
        super().__init__(device)
        self.name = "FactoryReset"

    def exec(self):
        default_config = {
            "wifi_ssid": "",
            "wifi_password": "",
            "measurements_file": "measurements.json"
        }
        with open("config.json", "w") as f:
            ujson.dump(default_config, f)

        # Reštart zariadenia
        reset()