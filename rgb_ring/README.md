# RGB Ring
This repo includes code for interfacing with Ubo RGB LED Ring.

# Client/Manager Model
The RGB Ring is controlled and managed by `rgb_ring_manager.py`. The manager 
runs as a system service with root previlage. Since the ring manager service uses Neopixel driver 
and due to the fact that Neopixel LEDs are driven through DRM, the script requires root `sudo` previlage 
to run.

To eliminate the need to run all applications that want to communicate with
RGB LED ring run with root previlage, we run the manager with root and other
applications send messages to it via writing to a socket. The manager constantly
read the incoming messages at that socket and displays the communicated pattern.


Please note that disable sound card
The install script (`system/setup/install.sh`) automically adds the rgb-ring service


```
sudo cp rgb-ring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart rgb-ring
sudo systemctl enable rgb-ring
```

2) permission model

Only applications that belong to the user group that have write permission to that 
socket can send patterns to led ring manager.

file socket `ledmanagersocket.sock`

3) setting up the service (add to install script)

`sudo bash system/setup/start_services.sh`

4) document primitives

```
lc = LEDClient()
lc.set_enabled(True)

# sets all LEDs to the specified color
lc.set_all(color=(255, 255, 255))


lc.blank()

lc.set_brightness(0.5)

lc.fill_upto(color = (255,255,255), 
            percentage = 0.5,
            wait = 100)

lc.fill_downfrom(color = (255,255,255), 
            percentage = 0.5,
            wait = 100)


Glows the LEDs in a rainbow pattern
percentage: is a float between 0 and 1
wait: is in milliseconds

lc.rainbow(rounds=10, wait=5)

# increments the position of bright strip by one step.
lc.progress_wheel_step(color=(0, 255, 0))


lc.pulse(color = (255,0,255), 
        wait = 50, #in miliseconds
        repetitions = 5)

# Spinning wheel 
# length = 10 leds
lc.spinning_wheel(color = (255,255,255), 
                wait = 20, #miliseconds
                length = 10, #leds
                repetitions = 3)
    


```

5) add rgb_ring_example.py

