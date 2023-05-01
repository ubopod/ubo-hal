#!/bin/bash

#set -x

UBO_USER=ubo
PI_USER=pi
UBO_PASSWD=password
RGBLED_GROUP=rgbled

# Create the rgbled group

if [ $(getent group $RGBLED_GROUP) ]; then
  echo "group $RGBLED_GROUP exists."
else
  echo "create group $RGBLED_GROUP"
  sudo groupadd $RGBLED_GROUP
fi


# Create the user uboo
egrep -i "^$UBO_USER:" /etc/passwd;
if [ $? -eq 0 ]; then
   echo "User $UBO_USER Exists"
else
   echo "User does not exist! let us create it"
   sudo useradd -m -p $(openssl passwd -1 $UBO_PASSWD) -G $RGBLED_GROUP $UBO_USER
fi

# Add pi user to rgbled group
sudo usermod -a -G $RGBLED_GROUP $PI_USER  

