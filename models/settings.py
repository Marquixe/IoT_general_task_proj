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

    @validator('wifi_ssid')
    def check_wifi_ssid(self, value):
        # WiFi SSID can be empty (will use AP mode)
        if value and len(value) > 32:
            raise ValueError('WiFi SSID too long (max 32 chars)')

    @validator('wifi_password')
    def check_wifi_password(self, value):
        # Password can be empty for open networks
        if value and (len(value) < 8 or len(value) > 63):
            raise ValueError('WiFi password must be 8-63 characters')