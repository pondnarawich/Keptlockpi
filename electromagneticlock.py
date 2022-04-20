import RPi.GPIO as gpio
from camera import *
import _thread

class ElectromagneticLock:

    def PinUnlock(self, pin, realpin, slot, locked):
        slot = led # remove when change to electromagnetic lock code
        if locked == True:
            if pin == realpin:
                gpio.output(slot,HIGH) #change to electromagnetic lock code
            else:
                print("Incorrect pin code")
        else:
            print("The locker's status is unlocked")

    def GeneralUnlock(slot, locked):
        # slot = led # remove when change to electromagnetic lock code
        if locked == True:
            gpio.output(slot, gpio.HIGH) #change to electromagnetic lock code
            _thread.start_new_thread(Camera.start_record,())
            while locked == True:
                continue
            Camera.stop_record()
        else:
            print("The locker's status is unlocked")
        return


    def RFIDUnlock(self, rfid, slot, locked):
        slot = led # remove when change to electromagnetic lock code
        if locked == True:
            # insert rfid code
            if rfid == cid:
                gpio.output(slot,HIGH) #change to electromagnetic lock code
            else:
                print("Incorrect card id for RFID")
        else:
            print("The locker's status is unlocked")

