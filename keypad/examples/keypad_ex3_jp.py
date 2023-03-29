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
    """
    State Machine class
    """

    def __init__(self, *args, **kwargs):
        """
        State Machine constructor
        @param self:
        @param args:
        @param kwargs:
        @return:
        """
        super(StateMachine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def button_event(self):
        """

        @param self:
        @return:
        """
        print('Button Event')
        print(self.buttonPressed)
        return

    def prompt(self):
        """
        this function displays 3 lines on the LCD

        The prompt itself <Agree>
        The choice of responses
        <Yes> with green background
        <No> with red background

        @rtype: object
        @return:
        """
        lcd.show_prompt("Agree?", [{"text": "Yes", "color": "green"}, {"text": "No", "color": "red"}])

        return


def main():
    # instantiate state machine 
    sm = StateMachine()

    # show the prompt on the LCD
    sm.prompt()

    # loop thru the state until state  is 1 
    while sm.state_index != 1:  # check state machine state
        # print("state_index = {0}self.buttonPressed ", sm.state_index)
        time.sleep(1)

    # we are done and out of here 
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
