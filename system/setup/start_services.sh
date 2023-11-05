envsubst < $UBO_SDK_PATH/rgb_ring/rgb-ring.service | sudo tee /etc/systemd/system/rgb-ring.service
envsubst < $UBO_SDK_PATH/device/startup-screen.service | sudo tee /etc/systemd/system/startup-screen.service
envsubst < $UBO_SDK_PATH/device/safe-reboot-shutdown.service | sudo tee /etc/systemd/system/safe-reboot-shutdown.service
envsubst < $UBO_SDK_PATH/device/clear-ui.service | sudo tee /etc/systemd/system/clear-ui.service
sudo systemctl daemon-reload
sudo systemctl enable rgb-ring
sudo systemctl enable startup-screen
sudo systemctl enable safe-reboot-shutdown
sudo systemctl enable clear-ui
sudo systemctl restart rgb-ring
sudo systemctl restart startup-screen
sudo systemctl restart safe-reboot-shutdown
sudo systemctl start clear-ui
# the following lines are required for PiIR library to work
# sudo systemctl enable pigpiod
# sudo systemctl start pigpiod
