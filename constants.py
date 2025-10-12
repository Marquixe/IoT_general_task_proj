DHT_PIN = 27
BTN_PIN = 20
NP_PIN = 18

SETTINGS_FILE = '/settings.json'
MEASUREMENTS_FILE = '/measurements.json'


SHORT_PRESS_DURATION = 3
LONG_PRESS_DURATION = 6

class TempUnit:
    IMPERIAL: str = 'imperial'
    STANDARD: str = 'standard'
    METRIC: str = 'metric'

    
class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    OFF = (0, 0, 0)


# DEFAULT_SETTINGS = {"units": "standart"}
# 
# TEMP_METRIC = 'metric'
# TEMP_IMPERIAL = 'imperial'
# TEMP_STANDART = 'standart'