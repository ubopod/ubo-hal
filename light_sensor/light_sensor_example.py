import os
import sys
import board
import adafruit_veml7700
import time
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(1)
i2c = board.I2C()

def main():
    # bus_address = "0x10"
    while True:
        try:
            light_sensor = adafruit_veml7700.VEML7700(i2c, address=0x10) 
        except ValueError as e:
            print("VEML7700 not found on I2C bus!")

        print("Light Intensity is %.2f Lux" % light_sensor.light)
        time.sleep(0.2)
        lcd.display([(1,"Light Intensity",0,"white"), 
                    (2,"Lux:",0,"white"), 
                    (3,str(light_sensor.light),0,"green"),
                    ], 
                    22)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)