# RGB Ring
This repo includes code for interfacing with Ubo RGB LED Ring.

## Client/Manager Model
The RGB Ring is controlled and managed by `rgb_ring_manager.py`. The manager 
runs as a system service with root privilege. Since the ring manager service uses 
[Neopixel](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage) 
driver and due to the fact that Neopixel LEDs are driven through DRM, the script 
requires root privilege (`sudo`) to run.

To eliminate the need to run all applications that want to communicate with
RGB LED ring run with root privilege (which has security implications), we only run 
the manager service with root privilege and other applications send messages to it 
by writing to a file socket. The manager constantly monitors and reads the incoming 
messages at that socket and displays the communicated pattern.

The SDK install script (`system/setup/install.sh`) automically sets up 
the following requirements for RGB LED Ring to function properly:

1. Sound must be disabled to use GPIO18. The install script updates `/boot/config.txt` 
by changing "dtparam=audio=on" to "dtparam=audio=off" and rebooting.

2. Sound card must be blacklisted by adding `blacklist snd_bcm2835` line 
in file `/etc/modprobe.d/snd-blacklist.conf`

3. Lastly `rgb-ring.service` must be added to system services and enabled 
to run at bootup. This is done in `system/setup/start_services.sh` script that runs 
during installation process.

```
sudo cp rgb-ring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart rgb-ring
sudo systemctl enable rgb-ring
```
You can run the above line by: 

`sudo bash system/setup/start_services.sh`

## Diagram 

![ubo rgb-ring](ubo_rgb_ring.jpg)

## Permission model

Only applications that belong to the user group that have write permission to the 
file socket can send patterns to led ring manager. Only user with root privilege
can add a user to that group. Currently, `pi` group has write permission to the file socket
(`ledmanagersocket.sock`)

We are improving permission managment currently. (TODO)


## Built-in RGB ring display patterns and primitives

### LED Client Class 

To show patterns on the RGB LED ring, you must first import LEDClient class:

`from rgb_ring_client import LEDClient`

### LED Client Object

then instantiate a new client object:

`lc = LEDClient()`

### LED Client enable/disable

To enable or disable the client, run:

`lc.set_enabled(True) #False`

### All LEDs to specified Color

To sets all LEDs to the specified color:

`lc.set_all(color=(0, 127, 0))`

### All LEDs off 

To turn off all LEDs:

`lc.blank()`

### Set LED Brightness

To set brightness to a specific level 
between 0 and 1 where 0 means darkness 
and 1 mmeans maxumum brightness:

`lc.set_brightness(0.5)`

### Fill up the Ring 

Fill up the ring from the first LED 
up to the specific LED index

```
lc.fill_upto(color = (255,255,255), 
            percentage = 0.5,
            wait = 100)
```

### Fill Down the ring

Fill down the ring from the first LED 
up to the specific LED index

```
lc.fill_downfrom(color = (255,255,255), 
            percentage = 0.5,
            wait = 100)
```

### Display Rainbow

Glows the LEDs in a rainbow pattern
percentage: is a float between 0 and 1
wait: is in milliseconds

`lc.rainbow(rounds=10, wait=5)`

### bright strip step
increments the position of bright strip by one step.

`lc.progress_wheel_step(color=(0, 255, 0))`

```
lc.pulse(color = (255,0,255), 
        wait = 50, #in miliseconds
        repetitions = 5)
```

# Spinning wheel 
# length = 10 leds
```
lc.spinning_wheel(color = (255,255,255), 
                wait = 20, #miliseconds
                length = 10, #leds
                repetitions = 3)
```    

