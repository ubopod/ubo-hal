# RGB Ring
This repo includes code for communicating and interfacing with Ubo hardware peripherals


1) explain the mamnager client model and the reason behind it
2) permission model
3) setting up the service (add to install script)
4) document primitives
5) add rgb_ring_example.py


```
sudo cp /rgb-ring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rgb-ring
sudo systemctl restart rgb-ring
```