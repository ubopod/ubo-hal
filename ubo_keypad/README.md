# KEYPAD Module Documentation
This module provides a class called KEYPAD that allows users to interact with a 8-key membrane keypad connected to a Raspberry Pi via an I2C GPIO expander.

## Requirements
    
    - Python 3

    - RPi.GPIO
https://www.adafruit.com/product/4886
    - adafruit_bus_device

    - adafruit_aw9523

    - Pillow (PIL)

Here is a bit more information about the modules imported

    - import RPi.GPIO as GPIO: 
    This imports the Raspberry Pi GPIO library, which is used to interact with the GPIO pins on a Raspberry Pi. 
    You can find more information on this library in the official Raspberry Pi documentation: 
    https://www.raspberrypi.org/documentation/usage/gpio/

    - from adafruit_bus_device import i2c_device: 
    This imports the I2C device class from the Adafruit CircuitPython Bus Device library, which is used to communicate with I2C devices connected to the Raspberry Pi. 
    You can find more information on this library in the Adafruit CircuitPython documentation: 
    https://circuitpython.readthedocs.io/en/latest/shared-bindings/bus_device/index.html

    - import adafruit_aw9523: 
    This imports the Adafruit AW9523 library, which is used to control the AW9523 GPIO Expander. 
    You can find more information on this library in the Adafruit CircuitPython documentation: 
    https://circuitpython.readthedocs.io/projects/aw9523/en/latest/

    - from PIL import Image, ImageDraw, ImageFont: 
    This imports the Python Imaging Library (PIL), which is used to manipulate images in Python. 
    Specifically, it imports the Image, ImageDraw, and ImageFont modules. You can find more information on PIL in the official documentation: https://pillow.readthedocs.io/en/stable/

    - import logging.config: This imports the Python logging module, which is used for logging messages in Python applications. 
    Specifically, it imports the config submodule. 
    You can find more information on the logging module in the official Python documentation: 
    https://docs.python.org/3/library/logging.html

    - import board: 
    This imports the CircuitPython board module, which provides access to pins and features on a specific board. 
    You can find more information on the board module in the Adafruit CircuitPython documentation: 
    https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/index.html

    - import math: 
    This imports the Python math module, which provides mathematical functions and constants. 
    You can find more information on the math module in the official Python documentation: 
    https://docs.python.org/3/library/math.html

    - import time: 
    This imports the Python time module, which provides time-related functions. 
    You can find more information on the time module in the official Python documentation:    

    - import signal: 
    This imports the Python signal module, which provides mechanisms to use signals in Python programs. 
    You can find more information on the signal module in the official Python documentation: 
    https://docs.python.org/3/library/signal.html

    - import os: 
    This imports the Python os module, which provides a way of interacting with the operating system. 
    You can find more information on the os module in the official Python documentation: 
    https://docs.python.org/3/library/os.html

    - import sys: 
    This imports the Python sys module, which provides access to some variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter. 
    You can find more information on the sys module in the official Python documentation: 
    https://docs.python.org/3/library/sys.html



## Installation
Install the required dependencies using pip:

pip install RPi.GPIO adafruit_bus_device adafruit_aw9523 Pillow

## Usage
Instantiate a KEYPAD object to use the keypad functions. Here is an example:

from keypad import KEYPAD

keypad = KEYPAD()

def callback(key):
    print("Button pressed:", key)

keypad.add_handler(callback)

while True:
    keypad.update()


The KEYPAD class provides the following methods:

## KEYPAD.init_i2c()
Initializes the I2C connection to the GPIO expander.

## KEYPAD.add_handler(callback)
Adds a callback function to the KEYPAD object that is called every time a button is pressed. 
The callback function should take one argument, the key identifier, which is a string (e.g. "0", "1", "2", "up", "down", "back", "home", "mic").

## KEYPAD.update()
Updates the KEYPAD object. 
This method should be called frequently to read the keypad input and trigger the callback function if a button is pressed.

## KEYPAD.set_led(index, state)
Turns on/off the LED associated with the specified index. 
The index should be an integer from 0 to 7, where 0 corresponds to the top left button and 7 corresponds to the mic button. 
The state should be a boolean value, where True turns on the LED and False turns it off.

## KEYPAD.set_display(image)
Displays an image on the LCD screen. 
The image parameter should be a PIL Image object.

## KEYPAD.clear_display()
Clears the LCD screen.

## KEYPAD.enable()
Enables the KEYPAD object. 
When the KEYPAD object is enabled, it will check for keypad input and trigger the callback function if a button is pressed.

## KEYPAD.disable()
Disables the KEYPAD object. 
When the KEYPAD object is disabled, it will not check for keypad input and will not trigger the callback function if a button is pressed.

## KEYPAD.shutdown()
Cleans up the KEYPAD object and releases the resources. 
This method should be called before the program exits.

# License
This module is licensed under the MIT License.: