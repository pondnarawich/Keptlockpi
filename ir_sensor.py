import RPi.GPIO as gpio
import time

sensor = 24

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.cleanup()
# gpio.setmode(gpio.BCM)

gpio.setup(sensor, gpio.IN)

while True:
    x = gpio.input(sensor)
    # print(x)
    if x == False:
        print("object detected")
        time.sleep(0.3)
    else:
        print("-----------")
        time.sleep(0.3)