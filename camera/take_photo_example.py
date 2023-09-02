import time
import os
import sys
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD
from ubo_keypad.ubo_keypad import Keypad # Might have to revisit this form of import
from picamera2 import Picamera2
import logging

#initialize LCD and Keypad
lcd = LCD()

class mykeypad(Keypad):
    def __init__(self, *args, **kwargs):
        super(mykeypad, self).__init__(*args, **kwargs)
        self.picam2 = Picamera2()
        self.stop = False

    def button_event(self):
        pressed = self.buttons.buttonPressed
        logging.info("Button pressed: " + str(pressed))
        if pressed:
            lcd.display([(1,"You pressed the",0,"green"), (2,pressed ,0,"blue"), (3,"button", 0,"green")], 19)
            if pressed == "middle-left":
                self.picam2.start_and_capture_file("test.jpg")
            if pressed == "bottom-left":
                self.stop = True
            lcd.show_still_image("./test.jpg")
            time.sleep(2)
            lcd.show_prompt("Take Photo?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )


def main():
    lcd.display([(1,"Starting",0,"white"), (2,"Keypad",0,"white"), (3,"Test", 0,"white")], 25)

    try:
        keypad = mykeypad()
    except:
        # did not detect keypad on i2c bus
        logging.info("failed to initialize keypad")
    if keypad.bus_address ==  False:
        return
    else:
        lcd.show_prompt("Take Photo?", [{"text": "Yes", "color": "green"},{"text": "No", "color": "red"}] )
        # loop until user says no
        while (not keypad.stop): 
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(0)

