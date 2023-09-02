from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import re
import os
import sys
import time
import logging
:
SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from device.wifi_manager import wifiManager
from display.lcd import LCD 
from rgb_ring.rgb_ring_client import LEDClient


wifi = wifiManager()
LED_RING = LEDClient()

picam2 = Picamera2()
barcodes = []
picam2.start()
# Regular expression pattern
# WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;
pattern = r"WIFI:S:([^;]+);T:([^;]*);P:([^;]+);H:([^;]*);;"

scan_start = time.time()
duration = 60 # seconds
delta = 0
timeout = False
match_found = False
while timeout==False:
    LED_RING.progress_wheel_step(color = (0,0,255))
    delta = time.time() -  scan_start
    if delta > duration:
        timeout = True
    rgb = picam2.capture_array("main")
    barcodes = decode(rgb)
    if barcodes:
        code = barcodes[0].data.decode() 
        print(code)
        # Match the pattern in the input string
        match = re.match(pattern, code)
        if match:
            logging.info("wifi qrcode match found.")
            match_found = True
            break
        else:
            logging.info("non wifi barcode match was found.")
            timeout = True # abort if non wifi barcode found
            # check time and abort if timeout

# add led, lcd, and audio bits here

if timeout ==  False & match_found:
    ssid = match.group(1)
    security_type = match.group(2)
    password = match.group(3)
    hidden = match.group(4)

    LED_RING.blink(color = (255,255,255),
                    wait = 1000,
                    repetitions = 1)

    print("SSID:", ssid)
    print("Security Type:", security_type)
    print("Password:", password)
    print("Hidden:", hidden)
    id = wifi.add_wifi(ssid=ssid, 
                    password=password, 
                    type=security_type)
    if id:
        wifi.logger.info("wifi added successfully ")
        LED_RING.spinning_wheel(color = (255,255,255), 
                    wait = 100,
                    length = 5,
                    repetitions = 30)
        R = wifi.connect_to_wifi(id)
        wifi.logger.info("wifi connected: " + str(R))
        if R:
            LED_RING.blink(color = (0,255,0), 
                        wait = 1000, 
                        repetitions = 1)
        else:
            LED_RING.blink(color = (255,0,0), 
                            wait = 1000, 
                            repetitions = 1)
    else:
        wifi.logger.info("wifi already exists...let's remove it")
        forgot = wifi.forget_wifi('earlplex-guest')
        if forgot:
            wifi.logger.info("network forgotten")
            LED_RING.blink(color = (0,0,255), 
                    wait = 1000, 
                    repetitions = 2)
        else:
            wifi.logger.info("network not removed!")
