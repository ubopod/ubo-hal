from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import re
import os
import sys
import time
import logging

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from rgb_ring.rgb_ring_client import LEDClient

class Camera:
    """
    Class for managing basic camera functions
    """
    def __init__(self):
        self.picam2 = Picamera2()
        self.barcodes = []
        self.wifi_pattern = r"WIFI:S:([^;]+);T:([^;]*);P:([^;]+);H:([^;]*);;"
        self.scan_duration = 60
        self.LED_RING = LEDClient()
        self.scan_timeout = False

    def __del__(self):
        self.picam2.close()

    def scan_for_wifi_qr_code(self):
        barcodes = []
        self.picam2.start()
        # Regular expression pattern
        # WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;
        pattern = r"WIFI:S:([^;]+);T:([^;]*);P:([^;]+);H:([^;]*);;"

        scan_start = time.time()

        delta = 0
        self.scan_timeout = False
        while self.scan_timeout==False:
            self.LED_RING.progress_wheel_step(color = (0,0,255))
            delta = time.time() -  scan_start
            if delta > self.scan_duration:
                self.scan_timeout = True
            rgb = self.picam2.capture_array("main")
            barcodes = decode(rgb)
            if barcodes:
                code = barcodes[0].data.decode() 
                print(code)
                # Match the pattern in the input string
                match = re.match(pattern, code)
                if match:
                    logging.info("wifi qrcode match found.")
                    return match
                else:
                    logging.info("non wifi barcode match was found.")
                    # return None
                    # check time and abort if timeout
        return None


if __name__ == "__main__":
    camera = Camera()
