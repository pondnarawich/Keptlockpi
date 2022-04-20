import RPi.GPIO as gpio
import time

lock1 = 6
lock2 = 13
lock3 = 19
lock4 = 26

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(lock1, gpio.OUT)
gpio.setup(lock2, gpio.OUT)
gpio.setup(lock3, gpio.OUT)
gpio.setup(lock4, gpio.OUT)
gpio.output(lock1, True)
gpio.output(lock2, True)
gpio.output(lock3, True)
gpio.output(lock4, True)
t = True

while True:
    # if t == True:
    gpio.output(lock1, False)
        # t = False
    # else:
    #     gpio.output(lock1, True)
    #     t = True
    # time.sleep(2)






# while True:
#     a = int(input(''))
#     if a == 1:
#         a = 0
#         gpio.output(lock1, False)
#     elif  a == 0:
#         a = 1
#         gpio.output(lock1, True)



# while True:
#     a = int(input(''))
#     if a == 1:
#         gpio.output(lock1,False)
#         gpio.output(lock2, True)
#         gpio.output(lock3, True)
#         gpio.output(lock4, True)
#     elif a == 2:
#         gpio.output(lock2,False)
#         gpio.output(lock1, True)
#         gpio.output(lock3, True)
#         gpio.output(lock4, True)
#     elif a == 3:
#         gpio.output(lock3,False)
#         gpio.output(lock1, True)
#         gpio.output(lock2, True)
#         gpio.output(lock4, True)
#     elif a == 4:
#         gpio.output(lock4, False)
#         gpio.output(lock1, True)
#         gpio.output(lock2, True)
#         gpio.output(lock3, True)
    
#     print(a)