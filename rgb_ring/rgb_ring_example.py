from rgb_ring_client import LEDClient
import time

# Instantiate an LED Ring client
lc = LEDClient()
# Enable ROG LED Ring
lc.set_enabled(True)
# Set all LEDs to white color
lc.set_all(color=(255, 255, 255))
time.sleep(1)
print("White ring must glow for 1 second")

# This line will disable the LED
# ring and sending any commands after that
# does not have an effect 
lc.set_enabled(False)
lc.set_all((255, 0, 0))
print("red ring must NOT glow for 1 second")
time.sleep(1)
# enabling RGB LED ring again
lc.set_enabled(True)

#set RGB ring to blank state
lc.blank()

# fill up the ring up to a given LED index
lc.fill_upto(color=(0,0,255), 
            percentage=1, #fill up to 100%
            wait=20) #miliseconds
time.sleep(1)

# fill down the rgb ring from a given LED index
lc.fill_downfrom(color=(0,0,255), 
                percentage=1, #fill down from full ring / 100%
                wait=20) #in miliseconds
time.sleep(1)

# Magenta
# Set all leds to magenta color 
lc.set_all(color=(255, 0, 255))
time.sleep(1)

# Yellow
# Set all leds to yellow color 
lc.set_all(color=(255, 255, 0))
time.sleep(1)

# Cyan
# Set all leds to Cyan color 
lc.set_all(color=(0, 255, 255))
time.sleep(1)

# White
# Set all leds to White color 
lc.set_all(color=(255, 255, 255))
time.sleep(1)

# Red
# Set all leds to Red color 
lc.set_all(color=(255, 0, 0))
time.sleep(1)

# Green
# Set all leds to Green color 
lc.set_all(color=(0, 255, 0))
time.sleep(1)     

# Blue
# Set all leds to Blue color 
lc.set_all(color=(0, 0, 255))
time.sleep(1)

# Turn off all leds
lc.blank()

# Activate rainbow
# wait: milisec
lc.rainbow(rounds=10, 
            wait=5) 
time.sleep(1)

# lower ring brightness
for i in range(0, 21, 1):
    lc.set_all(color=(255, 255, 255))
    lc.set_brightness(i/20)
    time.sleep(0.2)

# Show progress wheel step
for i in range(15):
    lc.progress_wheel_step(color=(0, 255, 0))
    time.sleep(0.1)

# Pulse
lc.pulse(color = (255,0,255), 
        wait = 50, #in miliseconds
        repetitions = 5)

time.sleep(2)

# Blink
lc.blink(color=(255, 0, 0), 
        wait=200, #turn off for miliseconds in between
        repetions=5) # blink 5 times
time.sleep(1)

# Spinning wheel 
# length = 10 leds
lc.spinning_wheel(color = (255,255,255), 
                wait = 20, #miliseconds
                length = 10, #number of leds, maxes to 27
                repetitions = 3) #spin 3 times
time.sleep(1)
lc.blank()

# length = 1 led
lc.spinning_wheel(color = (255,255,255), 
                wait = 20, #miliseconds
                length = 1, #leds
                repetitions = 3)
time.sleep(1)
lc.blank()

# Set progress wheel to 60%
for i in range(25):
    lc.progress_wheel(color = (255,255,255), 
                    percentage = i/25):
    time.sleep(0.1)
lc.blank()
