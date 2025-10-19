from device import Device

if __name__ == '__main__':
    print("Initializing device...")
    device = Device()
    print("Starting device...")
    device.run()







# # main.py
# #from dht import DHT11
# from machine import Pin
# from constants import DHT_PIN
# from helpers import read_settings, convert_temp
# import time
# import dht
# 
# pin = Pin(DHT_PIN, Pin.IN)
# sensor = dht.DHT22(Pin(27))
# 
# sensor.measure()
# temp = sensor.temperature()
# hum = sensor.humidity()
# settings = read_settings()
# 
# print(convert_temp(temp, settings['units']), hum)