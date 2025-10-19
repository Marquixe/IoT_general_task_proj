from models.udataclasses import Dataclass, validator
from constants import TempUnit


class Settings(Dataclass):
    units: str = TempUnit.STANDARD
    wifi_ssid: str = ''
    wifi_password: str = ''
    ntp_host: str = 'pool.ntp.org'
    mqtt_broker: str = ''
    mqtt_port: int = 1883
    mqtt_topic: str = ''

    @validator('units')
    def check_units(self, value):
        if value not in (TempUnit.METRIC, TempUnit.STANDARD, TempUnit.IMPERIAL):
            raise ValueError(f'Unit "{value}" is invalid.')