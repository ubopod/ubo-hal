# Records audio sample files for clock playback
# Speak each hour following the beep, one thru twelve

import os

if (os.system("i2cdetect -y 1 | grep 'UU'") == 0):
    print("audio IC detected!")
    #bus_address = "0xa1"
else:
    print("No audio IC detected!")


# TODO: Add check if mic switch is enabled

for x in range(1,13):
    os.system("aplay -D plughw:CARD=seeed2micvoicec,DEV=0 -c 1 -f S16_LE beep.wav")
    os.system("arecord -D plughw:CARD=seeed2micvoicec,DEV=0 --duration=1 --file-type=wav \
               --format=S16_LE  --rate=16000 --channels=2 " + str(x) + ".wav" \
             )

