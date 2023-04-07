import board
import subprocess
import adafruit_pct2075
from display.lcd import LCD as LCD
from time import sleep

lcd = LCD()
lcd.set_lcd_present(1)
i2c = board.I2C()

def displayTempText(temp_c, temp_f, c):
    lcd.display([(1,"CPU Temp",0,"purple"),
                 (2,"%.2f'C"%temp_c,0,c),
                 (3,"%.2f'F"%temp_f,0,c)
                ],
                30
               )

def displayTempWheel(temp_c):
    lcd.progress_wheel(title="Temperature %.2f'C"%temp_c,
                       degree=temp_c * 4,
                       color=(0,255,0)
                      )

def cpu_temp():

    measure_temp = subprocess.run("vcgencmd measure_temp", shell=True, capture_output=True).stdout.decode()
    temp_c = float(measure_temp.split("=")[1].split("'")[0])
    temp_f = temp_c * 1.8 + 32

    c = "green"
    if temp_c > 65 :
        c = "red"
    elif temp_c > 50 :
        c = "yellow"

    return (temp_f, c)
    #displayTempWheel(temp_c)
    #sleep(2)
    #displayTempText(temp_c, temp_f, c)

def demo():
    pct = adafruit_pct2075.PCT2075(i2c, address=0x48)

    sensor_temp = pct.temperature * 1.8 + 32
    cpu_info = cpu_temp()

    print("Temperature is %f C" % sensor_temp)

    lcd.display([(1,"Internal",0,"white"), (1,"%.1f'F"%sensor_temp,0,"cyan"), (2, "CPU",0,"white"), (3, "%0.1f'F"%cpu_info[0],0,cpu_info[1])], 40)
