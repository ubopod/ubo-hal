# Ubo SDK
This repo includes code for communicating and interfacing with Ubo hardware peripherals

There are example code and readme for each peripheral inside each sub-directory.

This SDK has been tested on latest 64-bit Raspberry Pi OS (uname -r: 6.1.19)

## Setup

First, Update your system and clone this repository 

```
sudo apt update  
sudo apt upgrade  
cd ~
git clone https://github.com/ubopod/ubo-sdk.git 
```

Currently, we assume that the SDK is cloned in /home/pi/ubo-sdk diretory. We will offer more flexibility for changing installation path in the future.

## Install

Run install script to setup everything. Make sure you do NOT install the SDK with sudo.

```
cd /home/pi/ubo-sdk/system/setup/  
bash install.sh
```

## Reboot
Next reboot the ssystem This is necessary to load drivers and new config.txt

`sudo reboot`

## Activate Virtual Environment

Since all python packages are installed inside ~/ubo-venv/bin/activate

Then you should be able to run sample codes 

