UBO_HOME=/home/pi/ubo
export PATH=$PATH:/home/pi/.local/bin

python3 -m pip install --upgrade pip
pip3 install --upgrade pip
pip3 install -r $UBO_HOME/system/setup/requirements.txt

#######################################
# Install SeeedStudio for speakers
######################################
/bin/bash $UBO_HOME/system/setup/install_seeedstudio.sh

#######################################
# Install EEPROM tools
######################################
/bin/bash $UBO_HOME/system/setup/install_eeprom.sh

#######################################
# Install Infra Red tools
######################################
sudo apt install ir-keytable 

#######################################
# Update config files
######################################
sudo cp $UBO_HOME/system/boot/config.txt /boot/config.txt
sudo cp $UBO_HOME/system/etc/modprobe.d/snd-blacklist.conf /etc/modprobe.d/snd-blacklist.conf
#######################################
# Add systemd services
######################################
/bin/bash ./start_services.sh
