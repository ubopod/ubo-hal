from device import Device
from wifi_manager import wifiManager
import os
import sys
from time import sleep
import logging
import time

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(SDK_HOME_PATH)

from display.lcd import LCD
from ubo_keypad.ubo_keypad import Keypad 
from rgb_ring.rgb_ring_client import LEDClient
from camera.camera_manager import Camera

lcd = LCD()
led_ring = LEDClient()
camera = Camera()
wifi = wifiManager()
device = Device()

class my_keypad(Keypad):
    def __init__(self, *args, **kwargs):
        super(my_keypad, self).__init__(*args, **kwargs)
        self.stop = False
        self.ON_PROMPT = False

    def button_event(self):
        pressed = self.buttons.buttonPressed
        logging.info("Button pressed: " + str(pressed))
        # only process buttons if prompt is being shown
        if self.ON_PROMPT:
            if pressed:
                if pressed == "middle-left":
                    lcd.display([(1,"Scan WiFi QRCode",0,"white"), (2, "using the front" ,0,"white"), (3,"camera", 0,"white")], 19)
                    # show led pattern for scanning
                    led_ring.progress_wheel_step(color = (0,0,255))
                    # scan wifi qr code
                    match = camera.scan_for_wifi_qr_code()
                    if match:
                        ssid = match.group(1)
                        security_type = match.group(2)
                        password = match.group(3)
                        hidden = match.group(4)
                        # match found led blink green once
                        lcd.display([(1,"Valid QRCode",0,"white"), (2, "Detect!" ,0,"white")], 19)
                        led_ring.blink(color = (255,255,255),
                                        wait = 1000,
                                        repetitions = 1)
                        # show ssid, security type, password, hidden on LCD
                        logging.info("SSID:", ssid)
                        logging.info("Security Type:", security_type)
                        logging.info("Password:", password)
                        logging.info("Hidden:", hidden)
                        id = wifi.add_wifi(ssid=ssid, 
                                        password=password, 
                                        type=security_type)
                        if id:
                            logging.info("wifi added successfully ")
                            led_ring.spinning_wheel(color = (255,255,255), 
                                        wait = 100,
                                        length = 5,
                                        repetitions = 30)
                            R = wifi.connect_to_wifi(id)
                            wifi.logger.info("wifi connected: " + str(R))
                            if R:
                                led_ring.blink(color = (0,255,0), 
                                            wait = 1000, 
                                            repetitions = 1)
                            else:
                                lcd.display([(1,"Connecting to WiFi",0,"white"), (2, "Failed!" ,0,"white")], 19)
                                led_ring.blink(color = (255,0,0), 
                                                wait = 1000, 
                                                repetitions = 1)
        else:
            logging.info("Internet connection is available.")

            if pressed == "bottom-left":
                lcd.display([(1,"Retyring to connect",0,"white"), (2, "to the Internet" ,0,"white"), (3,"....", 0,"white")], 19)
                # check internet connection


def main():
    kp = my_keypad()
    # check hostname and update if first time booting up
    lcd.display([(1,"Checking",0,"white"),
                (1,"hostname...",0,"white")],
                24)
    sleep(1)
    device.update_hostname()
    if not device.check_internet_connection():
        kp.ON_PROMPT = True
        lcd.show_prompt(title = "WiFi Setup", 
                        options =[{"text":"add","color":"green"},
                                    {"text":"remove","color":"red"}
                                    ])
    while not device.check_internet_connection():
        device.logger.debug("Internet connection is not yet available.")
        sleep(2)

    kp.ON_PROMPT = False
    device.logger.debug("Internet connection is now available.")
    lcd.display([(1,"Internet",0,"white"),(2,"detected!",0,"white")],24)
    sleep(2)
    # write Internet connection detected pn LCD
    # start vscode tunnel and get access code
    # show IP address, hostname, device code on LCD
    local_ip_address = device.get_local_ip()
    device.logger.debug("Local IP address:" + str(local_ip_address))
    current_hostname = device.get_current_hostname()
    device.logger.debug(current_hostname)
    # run vscode tunnel
    lcd.display([(1,"Establishing",0,"white"),(2,"Tunnel...",0,"white")],24)
    code = device.run_vscode_tunnel(current_hostname + '-remote')
    device.logger.debug(code)
    lcd.display([(1,"Code:" ,0,"white"), (2, str(code) ,0,"white"), 
                (3,"IP address:",0,"green"), (4,local_ip_address,0,"green"),
                (5,"Hostname:",0,"blue"),(6, current_hostname ,0,"blue")
                ],22)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
