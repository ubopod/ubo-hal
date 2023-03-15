# Audible Clock
#
# Pre-requisites:
#   sudo apt install espeak
#   pip3 install pyttsx3


try:
    import pyttsx3
except:
    print("ERROR: is pyttsx3 installed?\nUse 'pip3 install pyttsx3'")
    exit(1)

from datetime import datetime

s = pyttsx3.init()
s.say("The time is")
s.runAndWait()

now = datetime.now().time()
print(now)

time = str(now).split(":")

s.say("%s, %s"%(str(int(time[0])), str(int(time[1]))))
s.runAndWait()
