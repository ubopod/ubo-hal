import os
import subprocess
import sys
import board
up_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(up_dir)
from display.lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(1)

def main():

    measure_temp = subprocess.run("vcgencmd measure_temp", shell=True, capture_output=True).stdout.decode()
    temp_c = float(measure_temp.split("=")[1].split("'")[0])
    temp_f = temp_c * 1.8 + 32

    c = "green"
    if temp_c > 65 :
        c = "red"
    elif temp_c > 50 :
        c = "yellow"

    lcd.display([(1,"CPU Temp",0,"white"), \
(2,"%.2f'C"%temp_c,0,c), \
(3,"%.2f'F"%temp_f,0,c),], 30)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
