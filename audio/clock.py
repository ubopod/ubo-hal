# Audible Clock
#
# Pre-requisites:
#   sudo apt install espeak
#   pip3 install pyttsx3


import pyttsx3
from datetime import datetime

s = pyttsx3.init()
s.say("The time is")
s.runAndWait()

now = datetime.now().time()
print(now)

time = str(now).split(":")

s.say("%s, %s"%(str(int(time[0])), str(int(time[1]))))
s.runAndWait()
