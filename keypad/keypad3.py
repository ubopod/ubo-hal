import time
import os
import sys
import json
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD
from ubo_keypad import * # Might have to revisit this form of import

lcd = LCD()

class state_machine(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(state_machine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def key_press_cb(self, channel):
        #read inputs
        inputs = self.aw.inputs
        print("Inputs: {:016b}".format(inputs))
        inputs = 127 - inputs & 0x7F
        if inputs < 1:
            return
        index = (int)(math.log2(inputs))
        
        if inputs > -1:
            if self.state_index == 0:
                if BUTTONS[index]=="1": #YES  
                    lcd.display([(1,"Staying",0,"white"), (2,"in the",0,"red"), (3,"Loop",0,"green")], 20)
                    time.sleep(2)
                    lcd.show_prompt("Do you want to continue?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )
                if BUTTONS[index]=="2": #NO
                    lcd.display([(1,"Exiting",0,"white"), (2,"the",0,"red"), (3,"Loop",0,"green")], 20)
                    time.sleep(2)
                    self.state_index = 1

def main():
    S = state_machine()
    lcd.show_prompt("Do you want to continue?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )
    print("state_index = {0}",S.state_index)
    while (S.state_index != 1): # check state machine state 
        print("state_index = {0}",S.state_index)
        time.sleep(1)
    lcd.display([(1,"Bye",0,"white"), (2,"Bye",0,"red"), (3,"Friend",0,"green")], 20)
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



