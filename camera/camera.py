from pyzbar.pyzbar import decode
from picamera2 import Picamera2

picam2 = Picamera2()
barcodes = []
picam2.start()
while True:
    rgb = picam2.capture_array("main")
    barcodes = decode(rgb)
    print(barcodes)