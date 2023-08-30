from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import re
import os
import sys

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from device.wifi_manager import wifiManager

picam2 = Picamera2()
wifi = wifiManager()
barcodes = []
picam2.start()
# Regular expression pattern
# WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;
pattern = r"WIFI:S:([^;]+);T:([^;]*);P:([^;]+);H:([^;]*);;"

while True:
    rgb = picam2.capture_array("main")
    barcodes = decode(rgb)
    if barcodes:
        code = barcodes[0].data.decode() 
        print(code)
        # Match the pattern in the input string
        match = re.match(pattern, code)

        if match:
            ssid = match.group(1)
            security_type = match.group(2)
            password = match.group(3)
            hidden = match.group(4)
            
            print("SSID:", ssid)
            print("Security Type:", security_type)
            print("Password:", password)
            print("Hidden:", hidden)
            id = wifi.add_wifi(ssid=ssid, 
                            password=password, 
                            type=security_type)
            R = wifi.connect_to_wifi(id)
            wifi.logger.info("wifi connected: ", R)
            break
        else:
            print("No match found.")
