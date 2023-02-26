import os
import sys
import board
import adafruit_pct2075
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(1)
i2c = board.I2C()

def main():
    pct = adafruit_pct2075.PCT2075(i2c, address=0x48)

    temperature = pct.temperature

    print("Temperature is %.2f C" % temperature)

    lcd.display([(1,"Room",0,"white"), (2,"Temperature:",0,"white"), (3,str(temperature),0,"green"),], 22)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)