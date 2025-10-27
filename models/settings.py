from models.udataclasses import Dataclass, validator
from constants import TempUnit


class Settings(Dataclass):
    # Temperature settings
    units: str = TempUnit.STANDARD

    # WiFi settings
    wifi_ssid: str = ''
    wifi_password: str = ''

    # Time sync
    ntp_host: str = 'pool.ntp.org'

    # MQTT settings
    mqtt_broker: str = ''
    mqtt_port: int = 1883

    # MQTT topic structure (Smart Department format)
    department: str = 'kpi'
    room: str = 'kronos'
    device_name: str = 'thsensor'
    device_id: str = 'mm272ar'

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

    def get_mqtt_topic(self, suffix):
        return f"{self.department}/{self.room}/{self.device_name}/{self.device_id}/{suffix}"