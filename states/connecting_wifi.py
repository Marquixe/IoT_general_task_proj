from .state import AbstractState
import network
import time


class ConnectingWiFi(AbstractState):

    def enter(self):
        pass

    def exec(self):
        ssid = self.device.settings.wifi_ssid
        password = self.device.settings.wifi_password

        if not ssid:
            from .error import Error
            self.device.change_state(Error(self.device, 'WiFi SSID not configured'))
            return

        # Use STA_IF (Station/Client mode) to connect to existing WiFi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        print(f'Connecting to WiFi: {ssid}', end='')

        # Wait for connection (with timeout)
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('.', end='')
            time.sleep(1)

        print()  # New line

        if wlan.status() != 3:
            wlan.active(False)
            from .error import Error
            self.device.change_state(Error(self.device, 'WiFi connection failed'))
            return

        print('Connected to WiFi')
        print('IP:', wlan.ifconfig()[0])

        # Sync time via NTP
        self.sync_time()

        # Go to Publishing state to send data via MQTT
        try:
            from .publishing import Publishing
            self.device.change_state(Publishing(self.device))
        except ImportError:
            # If Publishing state doesn't exist, just sleep
            from .sleep import Sleep
            self.device.change_state(Sleep(self.device))

    def sync_time(self):
        try:
            import ntptime
            ntptime.host = self.device.settings.ntp_host
            ntptime.timeout = 5
            ntptime.settime()
            print('Time synchronized via NTP')

            # Update external RTC if available
            if hasattr(self.device, 'rtc') and self.device.rtc:
                from machine import RTC
                rtc = RTC()
                self.device.rtc.datetime(rtc.datetime())
                print('External RTC updated')
        except Exception as e:
            print(f'NTP sync failed: {e}')

    def exit(self):
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
        except:
            pass