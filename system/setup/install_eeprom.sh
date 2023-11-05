# Check if hats/eepromutils/ directory exists
DIR_PATH=./hats/eepromutils/
if [ -d "$DIR_PATH" ]; then
    echo "The directory $DIR_PATH exists."
else
    echo "The directory $DIR_PATH does not exist."
    git clone https://github.com/raspberrypi/hats.git
    wget -c https://raw.githubusercontent.com/RobertCNelson/tools/master/pkgs/dtc.sh
    chmod +x dtc.sh
    ./dtc.sh
    # then install these
    cd hats/eepromutils/
    make && sudo make install
fi