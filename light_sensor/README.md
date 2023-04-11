# How do I run it?

Step 1: It is assumed that the ubo-sdk has been cloned in a local directory.
        It is further assumed that you are running in the context of the
        ubo-venv python virtual environment.
        To activate this virtual environment you can enter the cli command
        $ ubo-venv/bin/activate

Step 2: Run `python3 light_sensor_example.py`
        The output of the program will look as follows:

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
.................................

==================================

        The example program will run  until stopped by CTRL+C 

### What Sensor are we using for to measure the ambient light intensity?

We use VEML7700 sensor from Vishay for light sensing. For more information on the sensor, check out the datasheet below:

Datasheet](https://www.vishay.com/docs/84286/veml7700.pdf) for light sensor


