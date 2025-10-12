from .state import AbstractState
import machine  # For restart
# Assuming constants.py has Color, or define here if needed
from constants import Color


class Configuration(AbstractState):
    def enter(self):
        # Set RGB LED to CYAN when entering the state
        self.device.led.set_color(Color.CYAN)  # Assuming Device has 'led' attribute for RGB LED control

    def exec(self):
        print('>> Configuration State')
        # Stub for AP mode: In a real implementation, set up Access Point and web server here
        # For now, simulate configuration (e.g., wait for user input or timeout)
        # Example: Wait 60 seconds for configuration (placeholder)
        import time
        time.sleep(60)  # Simulate timeout or configuration period

        # After configuration or timeout, restart the device
        machine.reset()

    def exit(self):
        # Optional: Clean up if needed, e.g., turn off LED
        pass