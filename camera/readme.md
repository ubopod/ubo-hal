To test the camera you can run this:
`libcamera-hello`


This is the example for the camera module

before running

`sudo apt install -y python3-picamera2`

##references:

https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

##Examples:
This will take a photo and save it in test.jpg
`python3 camera.py`

##Known issues:

If you see this issue

`libcblas.so.3: cannot open shared object file: No such file or directory`

then run

`sudo apt-get install libatlas-base-dev`


