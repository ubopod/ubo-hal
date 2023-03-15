# ==================================================
# UBO SDK:
#          keypad.py
# Description:
# This is an example of the way we can use the
#
# ==================================================
import time
import os
import sys
from display.lcd import LCD as LCD
from ubo_keypad import *

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)


# initialize LCD and Keypad
lcd = LCD()


class MyKeypad(KEYPAD):
    """
    MyKeypad a derived class from KEYPAD
    """
    def __init__(self, *args, **kwargs):
        """
        MyKeypad Constructor
        """
        super(MyKeypad, self).__init__(*args, **kwargs)
        self.test_result = False
        self.test_report = {"0": False, "1": False, "2": False, "up": False, "down": False, "back": False,
                            "home": False, "mic": True}

    def button_event(self):
        """
        Button event Handler
        """
        print(self.buttonPressed)
        self.test_report[self.buttonPressed] = True
        lcd.display([(1, "You pressed the", 0, "green"), (2, self.buttonPressed, 0, "blue"), (3, "button", 0, "green")],
                    19)
        time.sleep(2)
        lcd.indicate_buttons("Press all", "green", buttons=self.test_report)
        self.test_result = (self.test_report["0"] and self.test_report["1"] and
                            self.test_report["2"] and self.test_report["up"] and
                            self.test_report["down"] and self.test_report["home"] and
                            self.test_report["back"])


def main():
    lcd.display([(1, "Starting", 0, "white"), (2, "Keypad", 0, "white"), (3, "Test", 0, "white")], 25)

    try:
        keypad = MyKeypad()
    except ValueError as e:
        # did not detect keypad on i2c bus
        print("failed to initialize keypad")
    if not keypad.bus_address:
        keypad.test_result = False
        # abort test
    else:
        # continue with test
        lcd.indicate_buttons("Press all", "green", keypad.test_result)
        # loop until all keypad buttons are pressed
        while not keypad.test_result:
            time.sleep(1)

    print(keypad.test_result)
    if keypad.test_result:
        lcd.display([(1, "Keypad Test", 0, "white"), (2, "Result:", 0, "white"), (3, "Passed", 0, "green"),
                     (4, chr(56), 1, "green")], 25)
        time.sleep(1)
        sys.exit(0)
    else:
        lcd.display([(1, "Keypad Test", 0, "white"), (2, "Result:", 0, "white"), (3, "Failed", 0, "red"),
                     (4, chr(50), 1, "red")], 25)
        time.sleep(1)
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(0)
