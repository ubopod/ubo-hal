This sample code will take the temperature and show it on the LCD

## How to run the examples

### Step 1 

It is assumed that the ubo-sdk has been cloned in a home directory (/home/pi). Before running the examples, make sure that you activate the python virtual environment by running:

```$ source ~/ubo-venv/bin/activate```

In the temperature directory we have the following files. 

├── screen.png <- An image to show the way of displaying temp

├── temp_cpu.py <- this python program shows the temperature of the CPU on the LCD

└── temperature.py <- this python program shows the ambient temperature on the LCD 


### Step 2 

1) Run `python3 temperature.py` 

You shoud see the ambient temperature displayed on the LCD display similar to image below: 

![temperature on LCD ](screen.png)

2) Run `python3 temp-cpu.py`

This shows the CPU temperature on the LCD display. It uses command `vcgencmd measure_temp` command to get the CPU temperature. 
To learn more about this command, look at the manual: `man vcgencmd`

### Temperature sensor info

Ubo uses PCT2075 Temperature sensor by NXP. Fore more information, you can checkout the [datasheet](https://www.nxp.com/docs/en/data-sheet/PCT2075.pdf). We use the [Adafruit PCT2075 Python Library](https://docs.circuitpython.org/projects/pct2075/en/latest/) to communicate with the sensor via I2C bus. The sensor uses `0x48` address on the I2C bus. 
