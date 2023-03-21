import piir
from time import sleep

SLEEP_TIME = 0.3

"""
  Available IR Commands

    POWER

    RED
    GREEN
    BLUE
    WHITE

    1-20 (Available solid colors)

    BRIGHTER (7 steps)
    DIMMER   (7 steps)
    QUICK
    SLOW
    PAUSE

    AUTO
    FLASH
    JUMP_RGB
    JUMP_ALL
    FADE_RGB
    FADE_ALL
"""

# Setup remote for controlling RGB strip
remote = piir.Remote("rgb.json", 23)

#remote.send("POWER")

remote.send("RED")
sleep(SLEEP_TIME)

remote.send("GREEN")
sleep(SLEEP_TIME)

remote.send("BLUE")
sleep(SLEEP_TIME)

remote.send("WHITE")
sleep(SLEEP_TIME)


