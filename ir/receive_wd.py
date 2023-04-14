#!/bin/python3
# WD Mini Remote (necx)

import subprocess
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')

from display.lcd import LCD as LCD

lcd = LCD()
lcd.set_lcd_present(1)

def main():
    lcd.display([(1, "Starting", 0, "blue"), (2, "Infrared (IR)", 0, "red"), (3, "TEST", 0, "green")], 25)
    p1 = subprocess.Popen('sudo ir-keytable -c -w keymap_wd.toml -t -s rc0', shell=True)
    #p1 = subprocess.Popen('sudo ir-keytable -t -s rc0', shell=True)
    #p1 = subprocess.Popen('sudo stdbuf -i0 -o0 -e0 ir-keytable -c -p all -t -s rc1', shell=True)

    while 1:
      #print("Wating for IR...")
      time.sleep(1)
      print(p1.poll())

    sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os_exit(0)
