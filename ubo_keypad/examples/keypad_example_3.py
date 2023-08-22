import time
import os
import sys
from threading import Thread

SDK_HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
sys.path.append(SDK_HOME_PATH)

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(up_dir)

from display.lcd import LCD as LCD
from ubo_keypad.ubo_keypad import Keypad # Might have to revisit this form of import

#initialize LCD and Keypad
lcd = LCD()

class mykeypad(Keypad):
    def __init__(self, *args, **kwargs):
        super(mykeypad, self).__init__(*args, **kwargs)

    def count(self):
        # T = time.time()
        while self.buttons.get_status(self.button_label) == "pressed":
            self.logger.debug("Button {} remain pressed".format(self.button_label))
            # lcd.display([ 
            #             (1,self.button_label, 0,"white"),
            #             (2,"Seconds:", 0,"white"),
            #             (3,str(round(time.time() - T, 3)), 0,"white")
            #              ], 25)

    def button_event(self):
        self.logger.debug(self.button_label)
        thread = Thread(target=self.count)
        thread.start()
        


def main():
    lcd.display([(1,"Starting",0,"white"), 
                 (2,"Keypad",0,"white"), 
                 (3,"Example 3", 0,"white")
                 ], 
                25)

    try:
        keypad = mykeypad()
    except Exception as e:
        keypad.logger.error("Error initializing keypad: {}".format(e))

    while True: 
        time.sleep(10)
        pass



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(0)


