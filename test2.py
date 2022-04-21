import RPi.GPIO as GPIO
import time
import spidev

# set BCM_GPIO 17 as relay pin
RelayPin = 5
stat_lock = 17
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def adc_convert(ch):
    raw = spi.xfer2([1, (ch<<4) | 0x80, 0])
    data = ((raw[1]&3) << 8) | raw[2]
    # print("ADC Output : "+str(data))
    return data

#print message at the begining ---custom function
def print_message():
    print ('|**********************************************|')
    print ('|                     Relay                    |')
    print ('|        -----------------------------------   |')
    print ('|        GPIO0 connect to relay control pin    |')
    print ('|        led connect to relay NormalOpen pin   |')
    print ('|        5V connect to relay COM pin           |')
    print ('|        Make relay to control a led           |')
    print ('|        -----------------------------------   |')
    print ('|                                              |')
    print ('|                                        OSOYOO|')
    print ('|**********************************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    print ('\n')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set RelayPin's mode to output,and initial level to LOW(0V)
    GPIO.setup(RelayPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(stat_lock, GPIO.IN)
    

#main function
def main():
    #print info
    print_message()
    
    while True:
        temp = GPIO.input(stat_lock)
        data = adc_convert(0)
        print(data)
        print(temp)
        print('*************')
        # print ('|******************|')
        # print ('|  ...Relay close  |', data)
        # print ('|******************|\n')
        
        # disconnect
        # if data == 0:
            # GPIO.output(RelayPin,GPIO.LOW)
            # time.sleep(3)

            # # print ('|*****************|')
            # # print ('|  Relay open...  |', data)
            # # print ('|*****************|\n')
            # # print ('')
            # # connect
            # GPIO.output(RelayPin,GPIO.HIGH)

        time.sleep(1)

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off relay
    GPIO.output(RelayPin,GPIO.LOW)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()