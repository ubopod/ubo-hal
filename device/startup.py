from device import Device
import os
import sys
from time import sleep

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(SDK_HOME_PATH)

from display.lcd import LCD as LCD

def main():
    device = Device()
    lcd = LCD()
    # check hostname and update if first time booting up
    lcd.display([(1,"Checking",0,"white"),
                (1,"hostname...",0,"white")],
                24)
    sleep(1)
    device.update_hostname()
    while not device.check_internet_connection():
        device.logger.debug("Internet connection is not yet available.")
        # write message on screen
        lcd.display([(1,"Checking for",0,"white"),(2,"Internet...",0,"white")],24)    
        sleep(1)
    device.logger.debug("Internet connection is now available.")
    lcd.display([(1,"Internet",0,"white"),(2,"detected!",0,"white")],24)
    sleep(1)
    # write Internet connection detected pn LCD
    # start vscode tunnel and get access code
    # show IP address, hostname, device code on LCD
    local_ip_address = device.get_local_ip()
    device.logger.debug("Local IP address:" + str(local_ip_address))
    current_hostname = device.get_current_hostname()
    device.logger.debug(current_hostname)
    # run vscode tunnel
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
