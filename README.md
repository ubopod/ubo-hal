# Ubo SDK
This repo includes code for communicating and interfacing with Ubo hardware peripherals

There are example code and readme for each peripheral inside each sub-directory.

This SDK has been tested on latest 64-bit Raspberry Pi OS release:

> uname -a

Linux ubo-106 6.1.21-v8+ #1642 SMP PREEMPT Mon Apr  3 17:24:16 BST 2023 aarch64 GNU/Linux

32-bit OS is still under testing.

## Setup

First, Update your system and clone this repository 

```
sudo apt update  
sudo apt upgrade  
cd ~
git clone https://github.com/ubopod/ubo-sdk.git 
```

Currently, we assume that the SDK is cloned in /home/pi/ubo-sdk diretory. We will offer more flexibility for changing installation path in the future.

It is recommended that you do a reboot after the updates are installed before continueing to the next step.

```
sudo reboot
```

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

Since all python packages are installed inside the virtual environment, it must be activated to run the python scripts. 

```
source ~/ubo-venv/bin/activate
```

Now you should be able to run sample codes 

