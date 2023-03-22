#!/usr/bin/python

# Hello Ubo for Hackathon Getting Started

# Requirements:
#   pip3 install adafruit-circuitpython-rgb-display
#   pip3 install adafruit-circuitpython-aw9523

import os
import sys
import board
import math
from time import sleep

# RENAMED directory keypad to ubo_keypad (confilicted with Python library "keypad")
from ubo_keypad.ubo_keypad import KEYPAD as KEYPAD
from display.lcd import LCD as LCD

lcd = LCD()
#lcd.set_lcd_present(1)


"""
Keypad Mapping:

       ___________
      |           |
0  <= |  240x240  | /\   up  [3]
1  <= |  Display  |
2  <= |           | \/  down [4]
      |___________|

       ( < ] [ # )
    [5] back home [6]

         X |-+| O
          mic [7]


Menu Flow Chart:


Welcome screen while initializing...
    || (pauses while keypad loads)
    \/
Continue "Intro Prompt"
   Yes / No --> EXITING
    ||
    \/
Demo Menu
  0) Demo "Blink"
  1) Demo "Beep"
  2) Demo "Ambient"
  Back --> Continue "Intro Prompt"
  Home --> Exiting

Demo "Blink"
  0) Color Blink {blink.py}
  1) Color Fade  {fade.py}
  2) Color Chase {chase.py}
  Back --> Demo Menu
  Home --> Exiting

Demo "Beep"
  0) Play Tone {tone.py}
  1) Play Sound {wav.py}
  2) Play mp3   {mp3.py}
  Back --> Demo Menu
  Home --> Exiting

Demo "Ambient"
  0) Light Level  {sense.py}
  1) Temperature  {temp.py}
  2) Mic Volume   {mic.py}
  Back --> Demo Menu
  Home --> Exiting

Exiting
  Home / Back --> Demo Menu
   ||
   \/
  Quit

"""


class state_machine(KEYPAD):
    def __init__(self, *args, **kwargs):
        super(state_machine, self).__init__(*args, **kwargs)
        self.state_index = 0

    def key_press_cb(self, channel):
        #read inputs
        inputs = self.aw.inputs
        print("Inputs: {:016b}".format(inputs))
        inputs = 127 - inputs & 0x7F
        if inputs < 1:
            return
        index = (int)(math.log2(inputs))

        if inputs > -1:
            if self.state_index == 0:
                if self.BUTTONS[index]=="1":  # 'YES'
                    print("> YES")
                    lcd.display([(1,"Yes",0,"white"), (2,"was",0,"cyan"), (3,"hit",0,"green")], 20)
                    sleep(2)
                    self.prompt()
                if self.BUTTONS[index]=="2":  # 'NO'
                    print("> NO")
                    lcd.display([(1,"Exiting...",0,"grey"),
                                 (2,"come back",0,"cyan"),
                                 (3,"soon",0,"cyan"),
                                 (4,"press home",0,"white"),
                                 (3,"to quit",0,"red")],
                                   20)
                if self.BUTTONS[index]=="home":
                    print("> HOME")
                    lcd.display([(1," Going home",0,"white"),
                                 (2,"   Good Bye",0,"red"),
                                 (3,"     Hacker",0,"orange"),
                                 (4," - - - - - - - -",0,"grey"),
                                 (5,"run ./hello.py",0,"cyan"),
                                 (6,"to re-launch",0,"cyan")],
                                   20)
                    self.state_index = 1

    def prompt(self):
        lcd.show_prompt("Continue?", [{"text": "Yes", "color": "cyan"},{"text": "No", "color": "blue"}] )


def main():

    # lcd lisplay three lines with different colors
    lcd.display([(1,"  Hello Ubo!",0,"orange"), 
        (2,"Welcome to",0,"green"),
        (3,"HACKATHON",0,"cyan"),
        (4,"Circuit Launch",0,"blue"),
        (5,"Saturday BBQ",0,(255,0,255)),
        (6,"  initializing...",0,(123,123,123))],
        22)
    sleep(0.2)

    S = state_machine()
    S.prompt()
    while (S.state_index != 1): # check state machine state
        print("state_index = {0}",S.state_index)
        sleep(1)
    sys.exit(0)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

