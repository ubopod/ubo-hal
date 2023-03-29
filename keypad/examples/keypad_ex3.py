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


class StateMachine(KEYPAD):Key
    """
    State Machine class derived for KEYPAD class

    """
    def __init__(self, *args, **kwargs):
        """
        StateMachine constructor.
        invoke the parent class init

        """
        super(StateMachine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def key_press_cb(self, channel):
        """
        This function is a callback from 
        interrupt
        """

        # read inputs
        inputs = self.aw.inputs
        print("Inputs: {:016b}".format(inputs))
        inputs = 127 - inputs & 0x7F
        print('ZORGLUB')
        print(inputs)
        if inputs < 1:
            return
        
        # explain effect of this code
        index = int(math.log2(inputs))

        if inputs > -1:
            print('zzz')
            if self.state_index == 0:
                # button 1 pressed ?
                if self.buttonPressed == "1":  # YES
                    print('button yes pressed')
                    lcd.display([(1, "Yes", 0, "white"), (2, "was", 0, "red"), (3, "hit", 0, "green")], 20)
                    time.sleep(2)
                    self.prompt()

                # button 2 pressed ?
                if self.buttonPressed == "2":  # NO
                    lcd.display([(1, "No", 0, "white"), (2, "was", 0, "red"), (3, "hit", 0, "green")], 20)
                    time.sleep(2)
                    self.prompt()
                    # self.state_index = 1

                # button home pressed ? 
                if self.buttonPressed == "home":  # NO
                    lcd.display([(1, "Bye", 0, "white"), (2, "Bye", 0, "red"), (3, "Friend", 0, "green")], 20)
                    self.state_index = 1

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
        print("state_index = {0}self.buttonPressed ", sm.state_index)
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
