import RPi.GPIO as gpio
import time
import spidev
import requests
from main import lid, elec_lock


global locked

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

lock_threshold = 20

def adc_convert(ch):
    global spi
    raw = spi.xfer2([1, (ch<<4) | 0x80, 0])
    data = ((raw[1]&3) << 8) | raw[2]
    # print("ADC Output : "+str(data))
    return data

def GeneralUnlock(slot, slot_status):
    global spi
    global lid
    print(lid)
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(elec_lock[slot-1], gpio.OUT,initial=gpio.HIGH)
    cnt = 0
    # slot = led # remove when change to electromagnetic lock code
    # print(locked_status)
    gpio.output(elec_lock[slot-1], False) #change to electromagnetic lock code\
    time.sleep(1)
    gpio.output(elec_lock[slot-1], True)
    data = {"lid": str(lid), "slot": str(slot), "opened": str(True)}
    url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(lid)
    
    r = requests.post(url, data=data)
    # print(locked_status)
    while True:
        locked_status = adc_convert(slot_status)
        if locked_status < lock_threshold:
            cnt += 1       

        else:
            cnt = 0    
            # print(locked_status)
        if cnt >= 20:
            cnt = 0
            break
        print(locked_status)
        time.sleep(0.2)
    print('unlock', slot)
    return False


def is_lock(slot_status):
    global spi
    cnt = 0
    for i in range(10):
        locked_status = adc_convert(slot_status)
        if locked_status < lock_threshold:
            cnt += 1
        print(locked_status)
        time.sleep(0.2)
    if cnt >= 10:
        return True
    else:
        return False

# def is_lock(slot_status):
#     gpio.setwarnings(False)
#     gpio.setmode(gpio.BCM)
#     print(slot_status)
#     gpio.setup(slot_status, gpio.IN)
#     time.sleep(1)
#     locked_status = gpio.input(slot_status)
#     print('is_lock',locked_status)
#     if locked_status == 0:
#         return True
#     else:
#         return False
#     return 


