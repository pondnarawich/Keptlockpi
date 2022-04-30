
# # library from third-party
# # https://github.com/HubCityLabs/py532lib

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from multiprocessing import Process
import multiprocessing
import time
import threading


# def not_detected(detect):
#     if not detect:
#         print("Time out, No card detected")
#     return False
def check_id():
    pn532 = Pn532_i2c()
    pn532.SAMconfigure()
    card_id = pn532.read_mifare().get_data()
    if (card_id == bytearray(b'K\x01\x01\x00\x04\x08\x04G\x83\xf9\xd7'))\
        or (card_id == bytearray(b'K\x01\x01\x00\x04\x08\x04\x97\tq\xd7')):
        print('Unlock')
        return True
    else:
        print('Not match')
        return False
    return card_id


def read_id():
    print('Waiting for the card')
    x = threading.Thread(target=check_id)
    x.start()   
    x.join(timeout=40)     
        # return_dict['detect'] = True
        
    # print("RFID timeout")
    return False

# read_id()

# manager = multiprocessing.Manager()
# return_dict = manager.dict()
# return_dict['detect'] = False

# process = Process(target=read_id, args=(return_dict,))
# process.start()
# process.join(timeout=5)
# process.terminate()
# not_detected(return_dict['detect'])



