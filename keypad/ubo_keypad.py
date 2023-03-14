# ==================================================
# UBO SDK:
#          ubo_keypad.py
# Description:
# ==================================================

import RPi.GPIO as GPIO
from adafruit_bus_device import i2c_device
import adafruit_aw9523
from PIL import Image, ImageDraw, ImageFont
import logging.config
import board
import math
import time
import signal
import os
import sys
import platform
import logging
import logging.config
import logging.handlers
from logging.config import dictConfig
from datetime import datetime
import argparse

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)
# above line is needed for following classes:
# from led_client import LEDClient  # noqa E402 need up_dir first
# from lcd import LCD as LCD  # noqa E402 need up_dir first
try:
    from self.configparser import configparser
except ImportError:
    import configparser
display = True

DIR = './ui/'
CONFIG_FILE = './config/config.ini'
# LOG_CONFIG = "./log/logging.ini"
# logging.config.fileConfig(LOG_CONFIG,
#                           disable_existing_loggers=False)
INT_EXPANDER = 5


# BUTTONS = ["0", "1", "2", "up", "down", "back", "home", "mic"]


class KEYPAD(object):
    """
    KEYPAD Constructor

    """

    def __init__(self):
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
        Intialize the I2C via the GPIO Extender
        """
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
        except:
            try:
                self.aw = adafruit_aw9523.AW9523(i2c, 0x5b)
                new_i2c = i2c_device.I2CDevice(i2c, 0x5b)
                self.bus_address = "0x5b"
            except:
                # Test this scenario
                self.bus_address = False
                print("Failed to initialized I2C Bus")
                return

        # Perform reset of the Expender 
        self.aw.reset()
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
                    (self.mic_switch_status == True):
                print("Mic Switch is now OFF")
                self.index = 7
                self.buttonPressed = self.BUTTONS[self.index]
                self.mic_switch_status = False
                self.button_event()

            if ((self.last_inputs & 0x80) == 128) and \
                    (self.mic_switch_status == False):
                print("Mic Switch is now ON")
                self.index = 7
                self.buttonPressed = self.BUTTONS[self.index]
                self.mic_switch_status = True
                self.button_event()
            return

        if inputs < 1:
            self.index = 500  # invalid index
            return

        self.index = (int)(math.log2(inputs))
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
        return ((inputs & 0x80) == 128)

    def button_event(self):
        """
        This function does nothing for now
        should it remains ??
        """
        pass


def command_line_params(argv: object) -> object:
    """
    This function processes the arguments found on the command line
    We chose to use the argparse module in preference of getopt module
    :return:
    """
    # =======================================================
    # Establish the CLI commands parser
    # we use argparse module
    # ========================================================
    logger = None

    print(argv)
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(prog='UBO',
                                     description='UBO Keypad command line arguments',
                                     epilog='UBO Keypad')

    # Add the Verbose option
    parser.add_argument('--verbose', '-v',
                        dest='verbose_level', nargs='?', type=str,
                        help='Select a verbosity level to use')

    # Add the Config option
    parser.add_argument('--config', '-c',
                        dest='config_file', nargs='?', type=str,
                        help='Specify a Configuration file')

    # Parse and process the results
    args = parser.parse_args()

    # Process verbose flag
    if args.verbose_level:
        logger = logging.getLogger(__name__)
        logger.debug('Verbosity Level: ' + args.verbose_level)
        verbose_level = args.verbose_level

        valid_levels = [
            'NOTSET',
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ]

        logger_level = [
            logging.NOTSET,
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL
        ]

        if verbose_level in valid_levels:
            i = valid_levels.index(verbose_level)
            logger.setLevel(logger_level[i])
        else:
            logger.error('An invalid verbose level was specified %s:' % verbose_level)

    # Process config file flag
    if args.config_file:
        logger.debug('Config file: ' + args.config_file)
        config_file = args.config_file
        # check for existence of this file
        if os.path.exists(config_file) is False:
            logger.error('The specified config file %s does not exist' % config_file)
        else:
            logger.info('The UBO config file is %s: ' % config_file)
    return


def configure_logging(logfile_path):
    """
    Configure the logging mechanism
    This function is used to specify where the log files will reside.
    @param logfile_path: The file path where the logging files will be stored
    This function does:
    - Assign INFO and DEBUG level to logger file handler and console handler
    """

    # specify what we want to see on log lines
    # for debug and info
    debug_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] "
        "[%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d \
TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    info_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s]"
        " [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d \
TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers. \
        RotatingFileHandler(logfile_path, maxBytes=500 * 1024, backupCount=300,
                            encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler.setFormatter(debug_formatter)
    console_handler.setFormatter(info_formatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
    return


def establish_logging(local_log=True):
    """
    This function establishes the overall
    logging mechanism
    """
    if local_log is False:
        # Log on a specific filepath
        log_cfg_path = os.path.abspath(os.path.dirname(sys.argv[0])) \
                       + '/logging.cfg'
        print(log_cfg_path)

        # does the path exists ?
        if os.path.exists(log_cfg_path) is False:
            print('the specified logging configuration file %s does not exist' % log_cfg_path)
            sys.exit(1)

        logging.config.fileConfig(log_cfg_path, defaults=None,
                                  disable_existing_loggers=True)

        logger = logging.getLogger(__name__)
        logger.debug('UBO Keypad  log')
    else:
        now = datetime.now().isoformat()
        now = str(now).split('.')[0].replace(':', '-')

        # Create directory for logs
        h = platform.uname()[1]
        this_directory = os.path.realpath(os.path.dirname(__file__))
        logs_path = this_directory + '/Logs/' + h + '/'
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        # create a cycle number file
        # this file has a single number incremented each
        # time this program is run
        cycle_path = logs_path + 'cycle'
        if os.path.exists(cycle_path) is False:
            with open(cycle_path, 'w') as f:
                cycle = '1'
                f.write(cycle)
                f.close()
        else:
            with open(cycle_path, 'r') as f:
                cycle = f.read()
                f.close()
            cycle = int(cycle)
            cycle += 1
            cycle = str(cycle)

            with open(cycle_path, 'w') as f:
                f.write(cycle)
                f.close()
        logs_path += cycle
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        configure_logging(logs_path + '/' + now + '_UBO_Keypad.log')
        logger = logging.getLogger(__name__)
        logger.debug('UBO Keypad log')
    return


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
