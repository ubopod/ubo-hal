aplay -l | grep seeed &> /dev/null
if [ $? == 0 ]; then
   echo "SeeedStudio already installed"
else
   echo "installing seeedstudio, restarted needed after"
   # git clone https://github.com/respeaker/seeed-voicecard.git
   git clone https://github.com/HinTak/seeed-voicecard
   cd seeed-voicecard
   git pull
   # if uname -r (kernel version) is 6.1.19-v8+
   # for older kernel versions use v6.1, v6.0, or v5.9 
   git checkout v6.1
   sudo ./install.sh
   cd ..
fi
