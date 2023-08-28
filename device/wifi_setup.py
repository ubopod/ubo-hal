from wifi_manager import wifiManager
import os
import sys

up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD
from rgb_ring.rgb_ring_client import LEDClient

LED_RING = LEDClient()
W = wifiManager()
ssid='earlplex-guest'
password='hammerearlplex'
psk = W.generate_passphrase(ssid, password)
# id = W.add_wifi(ssid, password, type='WPA')
LED_RING.spinning_wheel(color = (255,255,255), 
                        wait = 100,
                        length = 5,
                        repetitions = 30)


id = W.add_wifi(ssid='earlplex-guest', psk=psk, type='WPA')

if id:
    R = W.connect_to_wifi(id)
    W.logger.info("wifi connected: " + str(R))
    if R:
        LED_RING.blink(color = (0,255,0), 
                    wait = 1000, 
                    repetitions = 1)
    else:
        LED_RING.blink(color = (255,0,0), 
                        wait = 1000, 
                        repetitions = 1)
else:
    forgot = W.forget_wifi('earlplex-guest')
    if forgot:
        W.logger.info("network forgotten")
        LED_RING.blink(color = (0,0,255), 
                wait = 1000, 
                repetitions = 1)
    else:
        W.logger.info("network not removed")

