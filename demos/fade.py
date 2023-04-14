# Blink LED's RGB Ring
from rgb_ring.rgb_ring_client import LEDClient

def demo():
    # Create instance of RGB LED Ring Client
    lc = LEDClient()

    # Loop thru and fade down to zero
    for x in range(-20, 1):
        lc.set_all(color=(0, int(x * -8), 0))
