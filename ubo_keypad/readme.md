If you want to only test the keypad on a fresh Raspberry Pi OS, clone/copy this directory, then run:

`pip install keypad_requirements.txt`

Make sure you have already installed `gpiozero` by running:

`sudo apt install python3-gpiozero`

Also make sure yu have I2C and SPI buses enabled in you `/boot/firmware/config.txt`

Finally run the following example:

`python3 examples/keypad_example.py`
