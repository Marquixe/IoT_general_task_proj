from .state import AbstractState
from constants import Color, AP_SSID_PREFIX, AP_PASSWORD
from web_interface import run_server
import network
import machine
import time
import uasyncio


class Configuration(AbstractState):

    def enter(self):
        # Set RGB LED to CYAN when entering configuration mode
        if self.device.led:
            self.device.led[0] = Color.CYAN
            self.device.led.write()

        self.setup_ap()

    def setup_ap(self):
        try:
            # Get unique device ID for SSID
            import ubinascii
            device_id = ubinascii.hexlify(machine.unique_id()).decode()[-6:]

            ssid = f'{AP_SSID_PREFIX}-{device_id}'
            password = AP_PASSWORD

            # Use AP_IF for Access Point mode
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            ap.config(essid=ssid, password=password)

            # Wait for AP to be active
            while not ap.active():
                time.sleep(0.1)

            print(f'Access Point created: {ssid}')
            print(f'Password: {password}')
            print(f'IP: {ap.ifconfig()[0]}')
            print(f'Connect and navigate to: http://{ap.ifconfig()[0]}')
        except Exception as e:
            print(f'Failed to create AP: {e}')


    def exec(self):
        print('>> Configuration State')
        try:
            loop = uasyncio.get_event_loop()
        except RuntimeError:
            loop = uasyncio.new_event_loop()
            uasyncio.set_event_loop(loop)

        loop.create_task(run_server())
        print('Configuration mode active. Waiting for settings...')
        loop.run_until_complete(uasyncio.sleep(60))
        time.sleep(60)

        # After configuration or timeout, restart the device

        from .connection_check import ConnectionCheck
        self.device.change_state(ConnectionCheck(self.device))

    def exit(self):
        try:
            ap = network.WLAN(network.AP_IF)
            ap.active(False)
            print('Access Point disabled')
        except:
            pass