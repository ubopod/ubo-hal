import time
import os
import sys

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from display.lcd import LCD as LCD
from ubo_keypad import * # Might have to revisit this form of import

#initialize LCD and Keypad
lcd = LCD()

class mykeypad(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(mykeypad, self).__init__(*args, **kwargs)
        self.buttons = {"0":False, "1":False, "2":False, "up":False, "down":False, "back":False, "home":False, "mic": True}

    def button_event(self):
        self.logger.debug(self.buttonPressed)
        self.buttons[self.buttonPressed] = True
        lcd.display([(1,"You pressed the",0,"green"), (2,self.buttonPressed,0,"blue"), (3,"button", 0,"green")], 19)
        time.sleep(1)
        lcd.indicate_buttons("Press all", "green", buttons=self.buttons)

def main():
    lcd.display([(1,"Starting",0,"white"), (2,"Keypad",0,"white"), (3,"Example 1", 0,"white")], 25)

    try:
        keypad = mykeypad()
    except:
        # did not detect keypad on i2c bus
        keypad.logger.error("failed to initialize keypad")
    if keypad.bus_address ==  False:
        return
    else:
        lcd.indicate_buttons("Press all", "green", buttons=keypad.buttons)
        # loop until all keypad buttons are pressed
        while (not all(keypad.buttons.values())): 
            time.sleep(1)
        lcd.indicate_buttons("Press all", "green", buttons=keypad.buttons)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(0)


