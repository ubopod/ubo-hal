import time
import os
import sys
import json

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from display.lcd import LCD as LCD
from ubo_keypad import * # Might have to revisit this form of import

lcd = LCD()

class state_machine(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(state_machine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def button_event(self):
        if self.state_index == 0:
            if self.buttonPressed=="1": #YES  
                lcd.display([(1,"Yes",0,"green"), (2,"was",0,"white"), (3,"selected",0,"white")], 20)
                time.sleep(1)
                self.prompt()
            if self.buttonPressed=="2": #NO
                lcd.display([(1,"No",0,"red"), (2,"was",0,"white"), (3,"selected",0,"white")], 20)
                time.sleep(1)
                self.prompt()
            if self.buttonPressed=="home":
                lcd.display([(1,"Bye",0,"white"), (2,"Bye",0,"red"), (3,"Friend",0,"green")], 20)
                self.state_index = 1

    def prompt(self):
        lcd.show_prompt("Agree?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )

def main():
    S = state_machine()
    S.prompt()
    while (S.state_index != 1): # check state machine state 
        S.logger.debug("state_index = " + str(S.state_index))
        time.sleep(100)
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



