import RPi.GPIO as GPIO
from adafruit_bus_device import i2c_device
import adafruit_aw9523
import logging.config
import board
import math
import time
import os
import sys
from typing import Literal

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(SDK_HOME_PATH)

LOG_CONFIG = SDK_HOME_PATH + "system/log/logging-debug.ini"
logging.config.fileConfig(LOG_CONFIG,
                          disable_existing_loggers=False)

INT_EXPANDER = 5 # GPIO PIN index that receives interrupt from AW9523

class ButtonStatus:
    """ Class to keep track of button status.
        0: "top_left": Top left button
        1: "middle_left": Middle left button 
        2: "bottom_left": Bottom left button
        3: "back": Button with back arrow label (under LCD)
        4: "home": Button with home label (Under LCD)
        5: "up": Right top button with upward arrow label
        6: "down": Right bottom button with downward arrow label
        7: "mic": Microphone mute switch
    """
    BUTTON_NAMES = [
        "top-left", "middle-left", "bottom-left",
        "up", "down", "back", "home", "mic"
    ]

    BUTTON_NAMES_TYPE = Literal[
        "top-left", "middle-left", "bottom-left",
        "up", "down", "back", "home", "mic"
    ]

    def __init__(self):
        self.buttons = {
            button_name: {"status": "released", "timeStamp": time.time()}
            for button_name in self.BUTTON_NAMES
        }

    def update_status(self, 
                      button_name: BUTTON_NAMES_TYPE,
                      new_status: Literal["pressed", "released"]):
        if new_status not in ["pressed", "released"]:
            raise Exception("Invalid status")
        if button_name in self.buttons:
            self.buttons[button_name]["status"] = new_status
            self.buttons[button_name]["timeStamp"] = time.time()

    def get_status(self, button_name: BUTTON_NAMES_TYPE) -> Literal["pressed", 
                                                                    "released"]:
        if button_name in self.buttons:
            return self.buttons[button_name]["status"]
        else:
            raise Exception("Invalid button name")

    def get_timestamp(self, button_name: BUTTON_NAMES_TYPE) -> float:
        if button_name in self.buttons:
            return self.buttons[button_name]["timeStamp"]
        else:
            raise Exception("Invalid button name")
        
    def get_label(self, index) -> BUTTON_NAMES_TYPE:
        if index > len(self.BUTTON_NAMES):
            raise Exception("Invalid index")
        else:
            return self.BUTTON_NAMES[index]

class Keypad:
    """ Class to handle keypad events.
    """
    def __init__(self, *args, **kwargs):
        """
        KEYPAD Constructor
        This initializes various parameters including
        loggers and button names.
        """
        self.logger = logging.getLogger("keypad")
        self.logger.debug("Initialising keypad...")
        self.event_queue = []
        self.aw = None
        self.inputs = None
        self.bus_address = 0x58
        self.model = "aw9523"
        self.enabled = True
        self.buttons = ButtonStatus()
        self.index = 0
        self.buttonPressed = None
        self.init_i2c()

    def clear_interrupt_flags(self, i2c):
        # Write to both registers to reset the interrupt flag
        buffer = bytearray(2)
        buffer[0] = 0x00
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        #print(buffer)
        time.sleep(0.1)
        buffer[0] = 0x01
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        time.sleep(0.1)

    def disable_interrupt_for_higher_bits(self, i2c):
        # disable interrupt for higher bits
        buffer = bytearray(2)
        buffer[0] = 0x06
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        #print(buffer)
        buffer[0] = 0x07
        buffer[1] = 0xff
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)

    def init_i2c(self):
        # connect to the I2C bus
        GPIO.setmode(GPIO.BCM)
        i2c = board.I2C()
        # Set this to the GPIO of the interrupt:
        GPIO.setup(INT_EXPANDER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        try:
            # Search for the GPIO expander address on the I2C bus
            self.aw = adafruit_aw9523.AW9523(i2c, self.bus_address)
            new_i2c = i2c_device.I2CDevice(i2c, self.bus_address)
        except Exception as e: 
            self.bus_address = False
            self.logger.error("Failed to initialized I2C Bus on address 0x58")
            self.logger.error(e)
            return
        
        # Perform soft reset of the expander
        self.aw.reset()
        # Set first 8 low significant bits (register 1) to input
        self.aw.directions = 0xff00
        time.sleep(1)

        # The code below, accessing the GPIO expander registers directly via i2c 
        # was created as a workaround of the reset the interrupt flag.
        self.clear_interrupt_flags(new_i2c)
        self.disable_interrupt_for_higher_bits(new_i2c)
        # reset interrupts again
        self.clear_interrupt_flags(new_i2c)
        
        # read register values
        self.inputs = self.aw.inputs
        self.logger.debug("Inputs: {:016b}".format(self.inputs))
        self.event_queue = [{"inputs": self.inputs, "timeStamp": time.time()}]
        time.sleep(0.5)

        # Enable interrupt on the GPIO expander
        GPIO.add_event_detect(INT_EXPANDER, 
                              GPIO.FALLING, 
                              callback=self.key_press_cb, 
                              bouncetime=1)

    def key_press_cb(self,_channel):
        """ Callback function dispatched by GPIO interrupt
            This is callback funtion that gets triggers
         if any change is detected on keypad buttons 
         states. 
         
         In this callback, we look at the state
         change to see which button was pressed or leased.

         Parameters:
        -----------
        _channel: int
            GPIO channel that triggered the callback
            NOT USED currently
        """
        # read register values
        self.inputs = self.aw.inputs
        event = {"inputs": self.inputs, "timeStamp": time.time()}
        # append the event to the queue. The queue has a depth of 2 and
        # keeps the current and last event.
        self.event_queue.append(event)
        self.logger.info(self.event_queue)
        self.logger.debug("Current Inputs: {:016b}".format(self.inputs))
        previos_event = self.event_queue.pop(0)
        self.logger.debug("Previous Inputs: {:016b}".format(
                                previos_event.get("inputs"))
                            )
        # XOR the last recorded input values with the current input values
        # to see which bits have changed. Technically there can only be one 
        # bit change in every callback 
        change_mask = previos_event.get("inputs") ^ self.inputs
        self.logger.info("Change: {:016b}".format(change_mask))
        # use the change mask to see if the button was the change was 
        # falling (1->0) indicating a pressed action
        # or risign (0->1) indicating a release action
        self.index = (int)(math.log2(change_mask))
        self.logger.info("button index is " + str(self.index))
        # Check for rising edge or falling edge action (press or release)
        self.button_label = self.buttons.get_label(self.index)
        if ((previos_event.get("inputs") & change_mask) == 0):
            self.logger.info("Released -> button {} with label {}.".format(
                                                                str(self.index),
                                                                self.button_label
                                                                ))
            

            # calculate how long the button was held down
            # and print the time
            last_time_stamp = self.buttons.get_timestamp(self.button_label)
            held_down_time = time.time() - last_time_stamp
            self.logger.info("Button was pressed down for {} seconds".format(
                                                                held_down_time))
            
            self.buttons.update_status(self.button_label, "released")

        else:
            self.logger.info("Pressed: button {} with label {}.".format(
                                                    str(self.index),
                                                    self.button_label
                                                    ))
            self.buttonPressed = self.button_label
            self.buttons.update_status(self.button_label, "pressed")        
            

        self.logger.info(self.buttons.buttons)
        self.button_event()

    def button_event(self):
        pass
    
    #     # mask the first 7 bits: 000000000 01111111
    #     inputs = 127 - self.inputs & 0x7F
    #     # if input is 0, then only look at microphone
    #     # switch state change.
    #     if inputs == 0:
    #         # Reaching here means some changes in GPIO expander 
    #         # triggered an interrupt but it was not due to a press on 
    #         # any of the keypad buttons. 
    #         # 
    #         # The code below checks if the interrupt was due to 
    #         # a change in microphone mute switch status. 
    #         # 
    #         # Other non-keypad button events must also be handled here.
    #         self.logger.debug("No keypad change.")
    #         # Look at value of register bit connnected to microphone switch
    #         # to see if it has changed. 
    #         # 
    #         # Toggle the mic switch status accordingly.
    #         # Mask the 8th bit: 10000000
    #         if ((self.inputs & 0x80) == 0) and \
    #             (self.mic_switch_status is True):
    #             self.logger.debug("Mic Switch is now OFF")
    #             self.index = 7
    #             self.buttonPressed = self.BUTTONS[self.index]
    #             self.mic_switch_status = False
    #             self.button_event()
    #         if ((self.inputs & 0x80) == 128) and \
    #             (self.mic_switch_status is False):
    #             self.logger.debug("Mic Switch is now ON")
    #             self.index = 7
    #             self.buttonPressed = self.BUTTONS[self.index]
    #             self.mic_switch_status = True
    #             self.button_event()
    #         return
    #     if inputs < 1:
    #         self.index = 500 #invalid index
    #         return
    #     self.index = (int)(math.log2(inputs))
    #     self.logger.info("index is " + str(self.index))
    #     if inputs > -1:
    #         self.buttonPressed = self.BUTTONS[self.index]
    #         self.button_event()
    #         if self.BUTTONS[self.index] == "up":
    #             self.logger.debug("Key up on " + str(self.index))
    #         if self.BUTTONS[self.index] == "down":
    #             self.logger.debug("Key down on " + str(self.index))
    #         if self.BUTTONS[self.index] == "back":
    #             self.logger.debug("Key back on " + str(self.index))
    #         if self.BUTTONS[self.index] in ["top_left", "middle_left", "bottom_left"]:
    #             self.logger.debug("Key side =" + str(self.index))
    #         if self.BUTTONS[self.index] == "home":
    #             self.logger.debug("Key home on " + str(self.index))
    #         return self.BUTTONS[self.index]

    # def get_mic_switch_status(self):
    #     inputs = self.aw.inputs
    #     self.logger.debug("Inputs: {:016b}".format(inputs))
    #     # microphone switch is connected to bit 8th
    #     # of the GPIO expander
    #     return ((inputs & 0x80) == 128)
    
    # def get_buttons_current_state(self):
    #     inputs = self.aw.inputs
    #     self.logger.debug("Inputs: {:016b}".format(inputs))
    #     return (127 - inputs & 0x7F)
    




def main():
    keypad = Keypad()
    if keypad.enabled is False:
        return
    while True:
        time.sleep(100)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
