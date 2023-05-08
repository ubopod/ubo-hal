# KEYPAD Module Documentation
This module provides a class called KEYPAD that allows users to interact with a 8-key membrane keypad connected to a Raspberry Pi via an I2C GPIO expander.

## Requirements
    
    - Python 3

    - RPi.GPIO

    - adafruit_bus_device

    - adafruit_aw9523

    - Pillow (PIL)

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