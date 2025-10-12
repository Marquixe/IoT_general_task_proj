import json
from constants import SETTINGS_FILE, TempUnit
from models.settings import Settings

def get_settings() -> Settings:
    with open(SETTINGS_FILE, 'r') as file:
        settings = json.load(file)
        return Settings(**settings)

def convert_temp(value: float, units: str) -> float:
    if units == TempUnit.METRIC:
        return value
    if units == TempUnit.IMPERIAL:
        return value * 9/5 + 32
    if units == TempUnit.STANDARD:
        return value + 273.15
    raise ValueError(f'Unit "{units}" is invalid.')