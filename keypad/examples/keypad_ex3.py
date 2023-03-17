import math
import time
import os
import sys

# to reach display
up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(up_dir)

# to reach the ubo_keypad
up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from display.lcd import LCD as LCD
from ubo_keypad import *

lcd = LCD()


class StateMachine(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(StateMachine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def key_press_cb(self, channel):
        # read inputs
        inputs = self.aw.inputs
        print("Inputs: {:016b}".format(inputs))
        inputs = 127 - inputs & 0x7F
        if inputs < 1:
            return
        index = int(math.log2(inputs))

        if inputs > -1:
            if self.state_index == 0:
                if self.buttonPressed == "1":  # YES
                    lcd.display([(1, "Yes", 0, "white"), (2, "was", 0, "red"), (3, "hit", 0, "green")], 20)
                    time.sleep(2)
                    self.prompt()
                if self.buttonPressed == "2":  # NO
                    lcd.display([(1, "No", 0, "white"), (2, "was", 0, "red"), (3, "hit", 0, "green")], 20)
                    time.sleep(2)
                    self.prompt()
                    # self.state_index = 1
                if self.buttonPressed == "home":  # NO
                    lcd.display([(1, "Bye", 0, "white"), (2, "Bye", 0, "red"), (3, "Friend", 0, "green")], 20)
                    self.state_index = 1

    def prompt(self):
        lcd.show_prompt("Agree?", [{"text": "Yes", "color": "green"}, {"text": "No", "color": "red"}])


def main():
    sm = StateMachine()
    sm.prompt()
    while sm.state_index != 1:  # check state machine state
        print("state_index = {0}self.buttonPressed ", sm.state_index)
        time.sleep(1)
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
