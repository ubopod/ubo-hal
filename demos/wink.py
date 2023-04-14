# Blink LED's RGB Ring
from time import sleep

from rgb_ring.rgb_ring_client import LEDClient

def demo():
    # Create instance of RGB LED Ring Client
    lc = LEDClient()

    # Enabled by default
    # lc.set_enabled(True|False)

    # Set all to a specific color
    lc.set_all(color=(0, 127, 0))

    # Wait a moment, then clear
    sleep(0.1)
    lc.blank()
