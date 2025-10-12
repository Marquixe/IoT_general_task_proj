from models.udataclasses import Dataclass, validator
from constants import TempUnit


class Settings(Dataclass):
    units: str = TempUnit.STANDARD

    @validator('units')
    def check_units(self, value):
        if value not in (TempUnit.METRIC, TempUnit.STANDARD, TempUnit.IMPERIAL):
            raise ValueError(f'Unit "{value}" is invalid.')