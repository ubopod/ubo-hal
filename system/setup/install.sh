set -x 
# TODO: ask user if they want to create a new user
export UBO_USER=$USER
# TODO: get install path from user
export SDK_INSTALL_PATH=$HOME
export UBO_SDK_PATH=$SDK_INSTALL_PATH/ubo-sdk/
export UBO_VENV_PATH=$SDK_INSTALL_PATH/ubo-venv/
export PATH=$PATH:$HOME/.local/bin

# Add enviroment variables to system 
echo "SDK_INSTALL_PATH=\"$SDK_INSTALL_PATH\"" | sudo tee -a /etc/environment
echo "UBO_SDK_PATH=\"$UBO_SDK_PATH\"" | sudo tee -a /etc/environment
echo "UBO_VENV_PATH=\"$UBO_VENV_PATH\"" | sudo tee -a /etc/environment

###### Install python & debian packages ######
sudo apt install -y python3-venv python3-dev python3-pyaudio python3-alsaaudio python3-picamera2
sudo apt install -y espeak libpcap-dev build-essential

######### Install python package ====
#change following line to include system packages
# --system-site-packages: Give the virtual environment 
# access to the system site-packages dir.
python3 -m venv --system-site-packages $UBO_VENV_PATH
. $UBO_VENV_PATH/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r $UBO_SDK_PATH/system/setup/requirements.txt

#######################################
# Install SeeedStudio for speakers
######################################
sudo /bin/bash $UBO_SDK_PATH/system/setup/install_seeedstudio.sh

#######################################
# Install EEPROM tools
######################################
sudo /bin/bash $UBO_SDK_PATH/system/setup/install_eeprom.sh

#######################################
# Install Infra Red tools
######################################
sudo apt install ir-keytable 

#######################################
# Update config files
######################################
sudo cp $UBO_SDK_PATH/system/boot/config.txt /boot/config.txt
sudo cp $UBO_SDK_PATH/system/etc/modprobe.d/snd-blacklist.conf /etc/modprobe.d/snd-blacklist.conf
#######################################
# Add systemd services
######################################
bash ./start_services.sh
