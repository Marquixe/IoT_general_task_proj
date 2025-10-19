from .state import AbstractState
import network
import time
from machine import reset


class ConnectionCheck(AbstractState):

    def enter(self):
        pass

    def exec(self):
        ssid = self.device.settings.wifi_ssid
        password = self.device.settings.wifi_password

        if not ssid:
            print('No WiFi SSID configured')
            from .configuration import Configuration
            self.device.change_state(Configuration(self.device))
            return

        # Use STA_IF (Station/Client mode) to test connection
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        print(f'Testing connection to: {ssid}', end='')

        # Try to connect
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('.', end='')
            time.sleep(1)

        #print()  # New line

        if wlan.status() != 3:
            # Connection failed - back to configuration
            print('Connection test failed')
            wlan.active(False)
            from .configuration import Configuration
            self.device.change_state(Configuration(self.device))
            return

        # Success! Sync time and restart
        print('Connection test successful')

        # Sync time with NTP
        try:
            import ntptime
            ntptime.host = self.device.settings.ntp_host
            ntptime.settime()
            print('Time synced')

            # Update external RTC if available
            if hasattr(self.device, 'rtc') and self.device.rtc:
                from machine import RTC
                rtc = RTC()
                self.device.rtc.datetime(rtc.datetime())
                print('External RTC updated')
        except Exception as e:
            print(f'Time sync failed: {e}')

        wlan.active(False)

        # Restart device to begin normal operation
        print('Restarting...')
        time.sleep(1)
        reset()

    def exit(self):
        pass