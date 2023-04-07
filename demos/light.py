import board
import adafruit_veml7700
from time import sleep
from display.lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(1)
i2c = board.I2C()

def demo():
    # bus_address = "0x10"
    try:
        light_sensor = adafruit_veml7700.VEML7700(i2c, address=0x10) 
    except ValueError as e:
        print("VEML7700 not found on I2C bus!")

    print("Light Intensity is %.2f Lux" % light_sensor.light)
    sleep(0.2)
    lcd.display([(1,"LUX",0,"cyan"), 
                    (2,"",0,"white"), 
                    (3,str(light_sensor.light),0,"white"),
                    ],
                    52)
