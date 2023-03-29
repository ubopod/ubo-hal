# Blink LED's RGB Ring
from rgb_ring.rgb_ring_client import LEDClient

def demo():
    # Create instance of RGB LED Ring Client
    lc = LEDClient()

    # Show the Rainbow effect
    lc.rainbow(rounds=5, wait=2)
