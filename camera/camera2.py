import time
import os
import sys
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD
from ubo_keypad import * # Might have to revisit this form of import
from picamera2 import Picamera2

#initialize LCD and Keypad
lcd = LCD()

class mykeypad(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(mykeypad, self).__init__(*args, **kwargs)
        self.test_result  = False
        self.test_report = {"0":False, "1":False, "2":False, "up":False, "down":False, "back":False, "home":False, "mic": True}
        self.picam2 = Picamera2()

    def button_event(self):
        print(self.buttonPressed)
        self.test_report[self.buttonPressed] = True
        lcd.display([(1,"You pressed the",0,"green"), (2,self.buttonPressed,0,"blue"), (3,"button", 0,"green")], 19)
        if self.buttonPressed == "1":
            self.picam2.start_and_capture_file("test.jpg")
            #time.sleep(5)
        lcd.show_still_image("./test.jpg")
        time.sleep(2)
        lcd.show_prompt("Take Photo?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )


def main():
    lcd.display([(1,"Starting",0,"white"), (2,"Keypad",0,"white"), (3,"Test", 0,"white")], 25)

    try:
        keypad = mykeypad()
    except:
        # did not detect keypad on i2c bus
        print("failed to initialize keypad")
    if keypad.bus_address ==  False:
        keypad.test_result = False
        #abort test
    else:
        # continue with test
        lcd.show_prompt("Take Photo?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )
        # loop until all keypad buttons are pressed
        while (not keypad.test_result): 
            time.sleep(1)


    print(keypad.test_result)
    if keypad.test_result:
        lcd.display([(1,"Keypad Test",0,"white"), (2, "Result:", 0, "white"), (3,"Passed",0,"green"), (4,chr(56),1,"green")], 25)
        time.sleep(1)
        sys.exit(0)
    else:
        lcd.display([(1,"Keypad Test",0,"white"), (2, "Result:", 0, "white"), (3,"Failed",0,"red"), (4,chr(50),1,"red")], 25)
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

