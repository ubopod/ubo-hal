UBO_HOME=/home/pi/ubo-sdk
export PATH=$PATH:/home/pi/.local/bin
sudo cp $UBO_HOME/rgb_ring/rgb-ring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart rgb-ring
sudo systemctl enable rgb-ring