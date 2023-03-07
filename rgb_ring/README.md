# RGB Ring
This repo includes code for interfacing with Ubo RGB LED Ring.

# Client/Manager Model
The RGB Ring is controlled and managed by `rgb_ring_manager.py`. The manager 
runs as a system service with root previlage. Since Ubo uses Neopixels and due to
the fact that Neopixel LEDs are driven through DRM, the script requires `sudo` previlage 
to run.

To eliminate the need to run all applications that want to communicate with
RGB LED ring run with root previlage, we run the manager with root and other
applications send messages to it via writing to a socket. The manager constantly
read the incoming messages at that socket and displays the communicated pattern.



```
sudo cp /rgb-ring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rgb-ring
sudo systemctl restart rgb-ring
```

The install script (`/setup/install.sh`) automically adds the rgb-ring service

# 

2) permission model

Only applications that belong to the user group that have write permission to that 
socket can send patterns to led ring manager.


3) setting up the service (add to install script)
4) document primitives

Pulse
Glow
Blink
Solid
Fill Up to
Fill Down to

5) add rgb_ring_example.py


