This sample code will display the Light Intensity in Lux and show it on LCD

## How to run examples

### Step 1 
It is assumed that the ubo-sdk has been cloned in a home directory (/home/pi). Before running the examples, ma
ke sure that you activate the python virtual environment by running:

```$ source ~/ubo-venv/bin/activate```
In the light-sensor directory we have the following files.

.
├── light_sensor_example.py <- this program shows on the LCD the Light Intensity in Lux




### Step 2 

Run `python3 light_sensor_example.py`

You shoud see on the LCD display something resembling this


==================================
Light Intensity is 2629.00 Lux
Light Intensity is 2637.00 Lux
Light Intensity is 2626.00 Lux
Light Intensity is 2624.00 Lux
Light Intensity is 2653.00 Lux
Light Intensity is 2654.00 Lux
Light Intensity is 2640.00 Lux
Light Intensity is 2642.00 Lux
Light Intensity is 2654.00 Lux
Light Intensity is 2655.00 Lux
...Keep going until CTRL+C........

==================================

        The example program will run  until stopped by CTRL+C 

### Light sensor info 

[Datasheet](https://www.vishay.com/docs/84286/veml7700.pdf) for light sensor
[Adafruit Documentation](https://learn.adafruit.com/adafruit-veml7700/overview) 
