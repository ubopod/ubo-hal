#!/usr/bin/python3
__author__ = "Authon Name"
__copyright__ = "Copyright 2023, The UBO Project"
__credits__ = ["names oof the contributor"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Maintainer Name"
__email__ = 'email address'
__status__ = "Current Status Prototype or Production"
# ==================================================
# UBO SDK:
#          ubo_keypad.py
# Description:
# ==================================================

import RPi.GPIO as GPIO
from adafruit_bus_device import i2c_device
import adafruit_aw9523
import logging.config
import board
import math
import time
import os
import sys
import platform
import logging
import logging.config
import logging.handlers
from datetime import datetime
import argparse

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(up_dir)

from logger.ubo_logger import establish_logging, command_line_params

# above line is needed for following classes:
# from led_client import LEDClient  # noqa E402 need up_dir first
# from lcd import LCD as LCD  # noqa E402 need up_dir first
try:
    from self.configparser import configparser
except ImportError:
    import configparser
display = True


# CONFIG_FILE = './config/config.ini'
# LOG_CONFIG = "./log/logging.ini"
# logging.config.fileConfig(LOG_CONFIG,
#                           disable_existing_loggers=False)
INT_EXPANDER = 5



class KEYPAD(object):
    """
    KEYPAD class
    """

    def __init__(self):
        """
        KEYPAD Constructor.
        This assumes that the logging mechanism has been
        correctly iniRemovetialized and functional
        aw925 GPIO extender need to be available
        """
        logger = logging.getLogger(__name__)
        # self.config = configparser.ConfigParser()
        # self.config.read(CONFIG_FILE)
        # self.logger = logging.getLogger("keypad")
        self.display_active = False
        self.window_stack = []
        self.led_enabled = True
        logger.debug('Initialising keypad...')
        self.aw = None
        self.mic_switch_status = False
        self.last_inputs = None
        self.bus_address = False
        self.model = "aw9523"
        self.init_i2c()
        self.enabled = True
        # ===========================================================================
        # those buttons are the ones found on the top face of the UBO Platform
        # they are disposed around the screen
        # ===========================================================================

        self.BUTTONS = ["0", "1", "2", "up", "down", "back", "home", "mic"]
        self.index = 0
        self.buttonPressed = self.BUTTONS[self.index]

    def init_i2c(self):
        """
        Initializes the I2C via the GPIO Extender
        Detailed info about the GPIO header and pins
        can be found here https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
        """

        logger = logging.getLogger(__name__)
        # Use GPIO numbers not pin numbers
        GPIO.setmode(GPIO.BCM)
        i2c = board.I2C()

        # Set this to the GPIO of the interrupt:
        GPIO.setup(INT_EXPANDER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # this code was created to be able to access the two possible 
        # i2c address. We try both. If the 0x58 fails try the 0x5B
        # if this one fails bail out. 
        # if the hw is now stable we could get rid of this and access one only
        # those parameters could be in a configuration file 
        try:
            self.aw = adafruit_aw9523.AW9523(i2c, 0x58)
            new_i2c = i2c_device.I2CDevice(i2c, 0x58)
            self.bus_address = "0x58"
        except ValueError as e:
            logger.debug(e)
            logger.debug('Did not detect GPIO expander 0x58 address on I2C bus')
            self.bus_address = False
            return

        # Perform reset of the expander
        self.aw.reset()
        logger.debug("Inputs: {:016b}".format(self.aw.inputs))
        print("Inputs: {:016b}".format(self.aw.inputs))

        self.aw.directions = 0xff00
        # self.aw.outputs = 0x0000
        time.sleep(1)

        # The code below, accessing the GPIO extender directly via i2c registers
        # was created as a workaround of the reset the interrupt flag

        # first write to both registers to reset the interrupt flag
        buffer = bytearray(2)
        buffer[0] = 0x00
        buffer[1] = 0x00
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)
        time.sleep(0.1)

        buffer[0] = 0x01
        buffer[1] = 0x00
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)

        # disable interrupt for higher bits
        buffer[0] = 0x06
        buffer[1] = 0x00
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)

        buffer[0] = 0x07
        buffer[1] = 0xff
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)

        # read registers again to reset interrupt
        buffer[0] = 0x00
        buffer[1] = 0x00
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)

        time.sleep(0.1)
        buffer[0] = 0x01
        buffer[1] = 0x00
        new_i2c.write(buffer)
        new_i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        print(buffer)

        time.sleep(0.1)

        # _inputs = self.aw.inputs
        # print("Inputs: {:016b}".format(_inputs))
        for i in range(1):
            self.last_inputs = self.aw.inputs
            print("Inputs: {:016b}".format(self.last_inputs))
            # print(self.last_inputs & 0x80)
            self.mic_switch_status = ((self.last_inputs & 0x80) == 128)
            print("mic switch is " + str(self.mic_switch_status))
            time.sleep(0.5)
        time.sleep(0.5)
        GPIO.add_event_detect(INT_EXPANDER, GPIO.FALLING, callback=self.key_press_cb)
        # GPIO.add_event_detect(INT_EXPANDER, GPIO.BOTH, callback=self.key_press_cb, bouncetime=200)

    def key_press_cb(self, channel):
        """
        This function implements a FSM for the keypad inputs
        """
        # read inputs
        self.last_inputs = self.aw.inputs
        print("Inputs: {:016b}".format(self.last_inputs))
        inputs = 127 - self.last_inputs & 0x7F

        # if input is 0, then only look at microphone
        # switch state change
        if inputs == 0:
            # print("no keypad change")
            if ((self.last_inputs & 0x80) == 0) and \
                    (self.mic_switch_status is True):
                print("Mic Switch is now OFF")
                self.index = 7
                self.buttonPressed = self.BUTTONS[self.index]
                self.mic_switch_status = False
                self.button_event()

            if ((self.last_inputs & 0x80) == 128) and \
                    (self.mic_switch_status is False):
                print("Mic Switch is now ON")
                self.index = 7
                self.buttonPressed = self.BUTTONS[self.index]
                self.mic_switch_status = True
                self.button_event()
            return

        if inputs < 1:
            self.index = 500  # invalid index
            return

        self.index = int(math.log2(inputs))
        print("index is " + str(self.index))

        if inputs > -1:
            self.buttonPressed = self.BUTTONS[self.index]
            self.button_event()

            if self.BUTTONS[self.index] == "up":
                print("Key up on " + str(self.index))

            if self.BUTTONS[self.index] == "down":
                print("Key down on " + str(self.index))

            if self.BUTTONS[self.index] == "back":
                print("Key back on " + str(self.index))

            if self.BUTTONS[self.index] in ["1", "2", "0"]:
                print("Key side =" + str(self.index))

            if self.BUTTONS[self.index] == "home":
                print("Key home on " + str(self.index))

            return self.BUTTONS[self.index]

    def get_mic_switch_status(self):
        """
        This function retrieve the status of microphone switch
        """
        inputs = self.aw.inputs
        print("Inputs: {:016b}".format(inputs))

        # microphone switch is connected to bit 8th
        # of the GPIO expander
        return 128 == (inputs & 0x80)

    def button_event(self):
        """
        This function does nothing for now
        should it remains ??
        """
        pass



def main(argv: object):
    """
    Main function 
    - instantiate KEYPAD class
    """

    # ==================================
    # Establish the logging mechanism
    # local_log is true if we want 
    #  
    # ==================================
    local_log: bool = True
    establish_logging(local_log)

    # ==================================
    # Parse the command line arguments
    # ==================================
    command_line_params(argv)

    keypad = KEYPAD()
    if keypad.enabled is False:
        return
    s = "OFF"

    if keypad.led_enabled:
        s = "ON"

    # enter loop and wait for interrupt events from
    while True:
        time.sleep(100)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

