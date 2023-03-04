from rgb_ring_client import LEDClient
import time

# Instantiate an LED Ring client
lc = LEDClient()
lc.set_enabled(True)
lc.set_all((255, 255, 255))
time.sleep(1)
print("White ring must glow for 1 second")

# This line will disable the LED
# ring and everything after that
# does not take effect
lc.set_enabled(False)
lc.set_all((255, 0, 0))
print("red ring must NOT glow for 1 second")
time.sleep(1)

# enabling RGB LED ring again
lc.set_enabled(True)

#set RGB ring to blank state
lc.blank()

# fill up the ring up to a given LED index
lc.fill_upto((0,0,255), 1, 20)
time.sleep(1)

# fill down the rgb ring from a given LED index
lc.fill_downfrom((0,0,255), 1, 20)
time.sleep(1)

# Magenta
# Set all leds to magenta color 
lc.set_all((255, 0, 255))
time.sleep(1)

# Yellow
# Set all leds to yellow color 
lc.set_all((255, 255, 0))
time.sleep(1)

# Cyan
# Set all leds to Cyan color 
lc.set_all((0, 255, 255))
time.sleep(1)

# White
# Set all leds to White color 
lc.set_all((255, 255, 255))
time.sleep(1)

# Red
# Set all leds to Red color 
lc.set_all((255, 0, 0))
time.sleep(1)

# Green
# Set all leds to Green color 
lc.set_all((0, 255, 0))
time.sleep(1)     

# Blue
# Set all leds to Blue color 
lc.set_all((0, 0, 255))
time.sleep(1)

# Turn off all leds
lc.blank()

# Activate rainbow
lc.rainbow(10, 5)
time.sleep(1)
for i in range(0, 11, 1):
    lc.set_brightness(i/10)
    time.sleep(0.2)

# Show progress wheel step
for i in range(15):
    lc.progress_wheel_step((0, 255, 0))
    time.sleep(0.1)

# Pulse
lc.pulse((255, 0, 255), 50, 5)
time.sleep(2)

# Blink
lc.blink((255, 0, 0), 200, 5)
time.sleep(1)

# Spinning wheel
lc.spinning_wheel((255, 255, 255), 20, 10, 3)
time.sleep(2)
lc.blank()

# Set progress wheel to 60%
for i in range(25):
    lc.progress_wheel((0, 0, 255), i/25)
    time.sleep(0.1)
lc.blank()
time.sleep(1)
lc.rainbow(3, 5)
time.sleep(2)
lc.blank()
