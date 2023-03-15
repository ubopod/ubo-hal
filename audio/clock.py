# Audible Clock
#
# Pre-requisites:
#   sudo apt install espeak
#   pip3 install pyttsx3
#
# TODO: check output is set to internal speakers, and reasonable volume

try:
    import pyttsx3
except:
    print("ERROR: is pyttsx3 installed?\nUse 'pip3 install pyttsx3'")
    exit(1)

try:
    from pydub import AudioSegment
    from pydub.playback import play
except:
    print("ERROR: is pydub installed?]nUse 'pip3 install pydub'")
    exit(1)

import os
from datetime import datetime
from time import sleep

try:
    s = pyttsx3.init()
    #s.say("The time is")
    #s.runAndWait()
except:
    print("ERROR: is espeak installed?\n Use 'sudo apt install espeak'")
    exit(1)


now = datetime.now().time()
print(now)

time = str(now).split(":")

# Play the recorded audio file for hour
os.system("aplay -D plughw:CARD=seeed2micvoicec,DEV=0 -c 1 -f S16_LE " + str(int(time[0])) + ".wav")

if int(time[0]) > 12:
    time[0] = str(int(time[0]) - 12)


for x in range(int(time[0])):
    os.system("aplay -D plughw:CARD=seeed2micvoicec,DEV=0 -c 1 -f S16_LE beep.wav")



hour = AudioSegment.from_wav(str(int(time[0])) + ".wav")
play(hour)

# Use espeak to say the minutes of the hour
#s.say("%s, %s"%(str(int(time[0])),str(int(time[1]))))
s.say("%s"%(str(int(time[1]))))
s.runAndWait()
