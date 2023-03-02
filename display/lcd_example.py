import os
import sys
import board
from lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(0)
i2c = board.I2C()

def main():

    # lcd lisplay three lines with different colors
    lcd.display([(1,"Line 1, Red",0,"red"), 
        (2,"Line 2, Green",0,"green"),
        (3,"Line 3, Blue ",0,"blue"),
        (4,"Line 4, White",0,"white"),
        (5,"Line 5, Yellow",0,(255,255,0)),
        (6,"All Size 22",0,(0,255,255))],
        22)
    # This will prompt the user to choose between two
    # options. The text and color can be customized 
    lcd.show_prompt(title="Agree?", 
                    options = [{"text": "Yes", 
                                "color": "green"},
                                {"text": "No", 
                                "color": "red"}
                                ]
                                )
    # wheel is filled up to provided circular degree (0-360)
    lcd.progress_wheel(title="Downloading...", 
                        degree=120, 
                        color=(255,255,0)
                    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
