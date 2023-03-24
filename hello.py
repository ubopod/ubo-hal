#!/usr/bin/python

# Hello Ubo for Hackathon Getting Started

# Requirements:
#   pip3 install adafruit-circuitpython-rgb-display
#   pip3 install adafruit-circuitpython-aw9523
#   pip3 install adafruit-circuitpython-busdevice
#   pip3 install board

import os
import sys
import board
import math
from time import sleep

# RENAMED directory keypad to ubo_keypad (conflicted with Python library "keypad")
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
0:Continue "Intro Prompt"
   Yes / No ==> EXITING
    ||
    \/
1:Demo Menu
  0) Demo "Blink"
  1) Demo "Beep"
  2) Demo "Ambient"
  Back ==> Continue "Intro Prompt"
  Home ==> Exiting

2:Demo "Blink"
  0) Color Blink {blink.py}
  1) Color Fade  {fade.py}
  2) Color Chase {chase.py}
  Back ==> Demo Menu
  Home ==> Exiting

3:Demo "Beep"
  0) Play Tone {tone.py}
  1) Play Sound {wav.py}
  2) Play mp3   {mp3.py}
  Back ==> Demo Menu
  Home ==> Exiting

4:Demo "Ambient"
  0) Light Level  {sense.py}
  1) Temperature  {temp.py}
  2) Mic Volume   {mic.py}
  Back --> Demo Menu
  Home --> Exiting

99:Exiting
  Home / Back ==> Demo Menu
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
        #print("Inputs: {:016b}".format(inputs))
        inputs = 127 - inputs & 0x7F
        if inputs < 1:
            return
        index = (int)(math.log2(inputs))

        if inputs > -1:
            button = self.BUTTONS[index]
            if self.state_index == 0:
                if button == "1":  # 'YES'
                    print("Pressed: Yes ==> Main Menu")
                    #self.prompt()
                    self.state_index = 1
                    self.demo_menu()
                if button == "2":  # 'NO'
                    print("> NO")
                    self.state_index = 99
                    self.exiting()
            elif self.state_index == 1:
                # Demo Menu
                if button == "0":
                    self.state_index = 2
                    self.demo_blink()
                elif button == "1":
                    self.state_index = 3
                    self.demo_beep()
                elif button == "2":
                    self.state_index = 4
                    self.demo_ambient()
            elif self.state_index == 2:
                # Blink Demos
                print("Blink Demos")
                if button == "0":
                    self.launch_demo("blink")
                elif button == "1":
                    self.launch_demo("fade")
                elif button == "2":
                    self.launch_demo("chase")
            elif self.state_index == 3:
                # Beep Demos
                print("Beep Demos")
                if button == "0":
                    self.launch_demo("tone")
                elif button == "1":
                    self.launch_demo("wav")
                elif button == "2":
                    self.launch_demo("mp3")
            elif self.state_index == 4:
                # Ambient Demos
                print("Ambient Demos")
                if button == "0":
                    self.launch_demo("sense")
                elif button == "1":
                    self.launch_demo("temp")
                elif button == "2":
                    self.launch_demo("mic")

            if button == "back":
                self.state_index = 1
                self.demo_menu()

            if button == "home" and self.state_index == 99:
                print("> QUIT")
                print("'ubo-sdk/hello.py' to restart")
                self.state_index = 100
            elif button == "home":
                print("> Exiting!")
                self.state_index = 99
                self.exiting()


    def launch_demo(self, demo):
        print(demo)

    def prompt(self):
        lcd.clear()
        lcd.show_prompt("Continue?", [{"text": "Yes", "color": "cyan"},{"text": "No", "color": "blue"}] )

    def demo_menu(self):
        lcd.clear()
        lcd.show_menu("Demo's", ["Blink", "Beep", "Ambient"])

    def demo_blink(self):
        lcd.clear()
        lcd.show_menu("RGB Ring", ["Blink", "Fade", "Chase"])

    def demo_beep(self):
        lcd.clear()
        lcd.show_menu("Beep", ["Tone", "WAV", "mp3"])

    def demo_ambient(self):
        lcd.clear()
        lcd.show_menu("Ambient", ["Sense", "Mic", "Temperature"])

    def exiting(self):
        print("EXITING...")
        lcd.clear()
        lcd.display([
            (1," Going home",0,"white"),
            (2,"   Good Bye",0,"red"),
            (3,"     Hacker",0,"orange"),
            (4," - - - - - - - -",0,"grey"),
            (5,"run ./hello.py",0,"cyan"),
            (6,"to re-launch",0,"cyan")
                    ], 20)
        print("EXIT TEXT")

def main():

    # lcd lisplay initializing text while loading
    lcd.display([
        (1,"  Hello Ubo!",0,"orange"),
        (2,"Welcome to",0,"green"),
        (3,"HACKATHON",0,"cyan"),
        (4,"Circuit Launch",0,"blue"),
        (5,"Saturday BBQ",0,(255,0,255)),
        (6,"  initializing...",0,(123,123,123))
                ], 22)

    sleep(0.2)

    S = state_machine()
    S.prompt()
    while (S.state_index != 99): # check state machine state
        #print("state_index = {0}",S.state_index)
        sleep(0.1)
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

