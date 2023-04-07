import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
soft_pwm = GPIO.PWM(26, 1000)

def demo():
    soft_pwm.start(5)
    sleep(2)
    soft_pwm.stop()
    sleep(0.02)
    GPIO.output(26, 1)
