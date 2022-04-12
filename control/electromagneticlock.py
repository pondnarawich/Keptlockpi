import RPi.GPIO as gpio

class ElectromagneticLock:

    # cid
    
    led = 2

    gpio.setwarnings(False)
    gpio.cleanup()
    gpio.setmode(gpio.BCM)
    gpio.setup(led, gpio.OUT)
    gpio.output(led, False)

    def PinUnlock(pin, realpin, slot, locked):
        slot = led # remove when change to electromagnetic lock code
        if locked == True:
            if pin == realpin
                gpio.output(slot,HIGH) #change to electromagnetic lock code
            else:
                print("Incorrect pin code")
        else:
            print("The locker's status is unlocked")

    def GeneralUnlock(slot, locked):
        slot = led # remove when change to electromagnetic lock code
        if locked == True:
            gpio.output(slot,HIGH) #change to electromagnetic lock code
        else:
            print("The locker's status is unlocked")


    def RFIDUnlock(rfid, slot, locked):
        slot = led # remove when change to electromagnetic lock code
        if locked == True:
            # insert rfid code
            if rfid == cid
                gpio.output(slot,HIGH) #change to electromagnetic lock code
            else:
                print("Incorrect card id for RFID")
        else:
            print("The locker's status is unlocked")

