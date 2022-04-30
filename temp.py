import RPi.GPIO as gpio
import time


global locked

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

gpio.setup(21, gpio.OUT)

while True:
    gpio.output(21,gpio.HIGH)
    time.sleep(1)
    gpio.output(21,gpio.LOW)
    time.sleep(1)
