import os
import subprocess
import sys
import board
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD
from time import sleep

lcd = LCD()
lcd.set_lcd_present(1)

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

def main():

    measure_temp = subprocess.run("vcgencmd measure_temp", shell=True, capture_output=True).stdout.decode()
    temp_c = float(measure_temp.split("=")[1].split("'")[0])
    temp_f = temp_c * 1.8 + 32

    c = "green"
    if temp_c > 65 :
        c = "red"
    elif temp_c > 50 :
        c = "yellow"

    displayTempWheel(temp_c)
    sleep(2)
    displayTempText(temp_c, temp_f, c)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
