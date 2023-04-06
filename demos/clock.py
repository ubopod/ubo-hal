# Hello Ubo Hackathon Clock Demo

# Requirements:
#   pip3 install adafruit-circuitpython-rgb-display
#   pip3 install adafruit-circuitpython-aw9523
#   pip3 install adafruit-circuitpython-busdevice
#   pip3 install board

import time

def tick(lcd):
    # Get current time and format
    now = time.localtime()
    n = "%02d:%02d"%(now[3], now[4])
    s = "     %02d"%(now[5])

    lcd.display([
        (1,n,0,"white"),
        (2,s,0,"cyan"),
        (3,"time",0,"grey"),
                ], 52)
