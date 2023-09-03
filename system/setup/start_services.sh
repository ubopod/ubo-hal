UBO_HOME=/home/pi/ubo-sdk
export PATH=$PATH:/home/pi/.local/bin
sudo cp $UBO_HOME/rgb_ring/rgb-ring.service /etc/systemd/system/
sudo cp $UBO_HOME/device/startup-screen.service /etc/systemd/system/
sudo cp $UBO_HOME/device/safe-reboot-shutdown.service /etc/systemd/system/
sudo cp $UBO_HOME/device/clear-ui.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rgb-ring
sudo systemctl enable startup-screen
sudo systemctl enable safe-reboot-shutdown
sudo systemctl enable clear-ui
sudo systemctl restart rgb-ring
sudo systemctl restart startup-screen
sudo systemctl restart safe-reboot-shutdown
sudo systemctl restart clear-ui
# the following lines are required for PiIR library to work
# sudo systemctl enable pigpiod
# sudo systemctl start pigpiod
