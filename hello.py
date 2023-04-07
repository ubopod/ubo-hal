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

# Load all demo's
import demos.wink
import demos.fade
import demos.rainbeau
import demos.tone
import demos.wav
import demos.mp3
import demos.light
import demos.temperature
import demos.clock

lcd = LCD()


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
  0) Demo "Blinks"
  1) Demo "Beeps"
  2) Demo "Sensors"
  Back ==> Continue "Intro Prompt"
  Home ==> Exiting

2:Demo "RGB Ring"
  0) Color Wink {wink.py}
  1) Color Fade  {fade.py}
  2) Color Rainbow {rainbeau.py}
  Back ==> Demo Menu
  Home ==> Exiting

3:Demo "Sounds"
  0) Play Tone {tone.py}
  1) Play Sound {wav.py}
  2) Play mp3   {mp3.py}
  Back ==> Demo Menu
  Home ==> Exiting

4:Demo "Sensors"
  0) Light Level  {light.py}
  1) Temperature  {temperature.py}
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
                    self.demo_blinks()
                elif button == "1":
                    self.state_index = 3
                    self.demo_beeps()
                elif button == "2":
                    self.state_index = 4
                    self.demo_sensors()
                elif button == "up":
                    pass
                elif button == "down":
                    # Set to "Clock" mode
                    self.state_index = 66
            elif self.state_index == 2:
                # Blink Demos
                print("Blink Demos")
                if button == "0":
                    self.launch_demo("wink")
                elif button == "1":
                    self.launch_demo("fade")
                elif button == "2":
                    self.launch_demo("rainbeau")
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
                # Sensor Demos
                print("Sensor Demos")
                if button == "0":
                    self.launch_demo("light")
                elif button == "1":
                    self.launch_demo("temperature")
                elif button == "2":
                    self.launch_demo("mic")

            if button == "back":
                print("<- BACK")
                self.state_index = 1
                sleep(0.1)
                self.demo_menu()

            if button == "home" and self.state_index == 99:
                print("> QUIT")
                print("'ubo-sdk/hello.py' to restart")
                self.quiting()
                self.state_index = 100
            elif button == "home":
                print("> Exiting!")
                self.state_index = 99
                self.exiting()


    def launch_demo(self, demo):
        print(demo)
        eval("demos." + demo + ".demo")()

    def prompt(self):
        lcd.clear()
        lcd.show_prompt("Continue?", [{"text": "Yes", "color": "cyan"},{"text": "No", "color": "blue"}] )

    def demo_menu(self):
        lcd.clear()
        lcd.show_menu("Demo's", ["Blinks", "Beeps", "Sensors"])

    def demo_blinks(self):
        lcd.clear()
        lcd.show_menu("RGB Ring", ["Wink", "Fade", "Rainbow"])

    def demo_beeps(self):
        lcd.clear()
        lcd.show_menu("Sounds", ["Tone", "WAV", "mp3"])

    def demo_sensors(self):
        lcd.clear()
        lcd.show_menu("Sensors", ["Light", "Temperature", "Microphone"])

    def exiting(self):
        lcd.clear()
        lcd.display([
            (1,"Press HOME",0,"white"),
            (2,"to quit, or",0,"red"),
            (3,"Press BACK",0,"orange"),
            (4," - - - - - - - -",0,"grey"),
            (5,"run ./hello.py",0,"cyan"),
            (6,"to re-launch",0,"cyan")
                    ], 20)

    def quiting(self):
        lcd.clear()
        lcd.display([
            (1,"PROGRAM QUIT",0,"white"),
            (2,"goodbye hacker",0,"blue"),
            (3,"",0,"orange"),
            (4," - - - - - - - -",0,"grey"),
            (5,"run ./hello.py",0,"cyan"),
            (6,"to re-launch",0,"cyan")
                    ], 20)


def loop(S):
    if S.state_index == 66:
        # tick "Clock"
        demos.clock.tick(lcd)
    sleep(0.1)

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
    while (S.state_index < 100): # check state machine state
        #print("state_index = {0}",S.state_index)
        loop(S)
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

