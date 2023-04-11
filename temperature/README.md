This sample code will take the temperature and show it on the LCD

### How do I run it?

Step 1: It is assumed that the ubo-sdk has been cloned in a local directory
        the directory should look as follows:

.
├── audio
├── camera
├── datasheets
├── demos
├── display
├── error.log
├── hackathon
├── hello.py
├── ir
├── ledmanagersocket.sock
├── LICENSE
├── light_sensor
├── README.md
├── rgb_ring
├── stemmaqt
├── system
├── **temperature**
└── ubo_keypad
        
In the temperature directory we have the following files. 


.
├── __pycache__
│   └── lcd.cpython-39.pyc
├── README.md
├── screen.png
├── temp_cpu.py <- this python program shows on the LCD the temperature of the CPU
└── temperature.py <- this python program shows on the LCD the ambient temperature


Step 2: Run `python3 temperature.py`

### What Sensor are we using for to measure the temperature
	- [Datasheet](https://www.nxp.com/docs/en/data-sheet/PCT2075.pdf) for temprature sensor:



