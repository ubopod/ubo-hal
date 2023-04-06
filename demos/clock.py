# Hello Ubo Hackathon Clock Demo

# Requirements:
#   pip3 install adafruit-circuitpython-rgb-display
#   pip3 install adafruit-circuitpython-aw9523
#   pip3 install adafruit-circuitpython-busdevice
#   pip3 install board

import os
import sys
import board
import math
from time import sleep

# RENAMED directory keypad to ubo_keypad (conflicted with Python library "keypad")
from ubo_keypad.ubo_keypad import KEYPAD as KEYPAD
from display.lcd import LCD as LCD

import time

try :
 i2c = board.I2C()
except :
 print("I2C failed")
 exit

lcd = LCD()

count = 99

def loop():
    global count

    if (count >= 60):
        count = 0

    # Get current time and format
    now = time.localtime()
    n = "%02d:%02d"%(now[3], now[4])
    s = "     %02d"%(now[5])

    lcd.display([
        (1,n,0,"white"),
        (2,s,0,"cyan"),
        (3,"time",0,"grey"),
                ], 52)

    count = count + 1

def main():

    # lcd lisplay initializing text while loading
    lcd.display([
        (1,"12345",0,"orange"),
        (2,"12345",0,"white"),
        (3,"12345",0,"cyan"),
                ], 52)

    sleep(.1)

    while (True):
        loop()
        sleep(1)

    sys.exit(0)

main()

