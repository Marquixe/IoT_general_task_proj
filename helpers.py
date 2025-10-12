import json
from constants import SETTINGS_FILE, TempUnit
from models.settings import Settings




def get_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            return Settings(**data)
    except Exception as e:
        s = Settings()
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({'units': s.units}, f)
        except Exception:
            pass
        
    
        return s




def convert_temp(value: float, units: str) -> float:
    if units == TempUnit.METRIC:
        return float(value)
    if units == TempUnit.IMPERIAL:
        return float(value) * 9.0/5.0 + 32.0
    if units == TempUnit.STANDARD:
        return float(value) + 273.15
    
    raise ValueError('Unit "%s" is invalid.' % units)




def append_measurement(rec, path):
# rec: dict -> {'ts': ..., 'temp_c': ..., 'hum': ...}
    try:
        import ujson as json
    except Exception:
        json = __import__('json')
        
        
    try:
        try:
            with open(path, 'r') as f:
                arr = json.load(f)
        except Exception:
            arr = []
            arr.append(rec)
            with open(path, 'w') as f:
                json.dump(arr, f)
    except Exception:
        pass
