
# # library from third-party
# # https://github.com/HubCityLabs/py532lib

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from multiprocessing import Process
import multiprocessing
import time
import threading

card_status = False

# def not_detected(detect):
#     if not detect:
#         print("Time out, No card detected")
#     return False
def check_id():
    global card_status
    pn532 = Pn532_i2c()
    pn532.SAMconfigure()
    card_id = pn532.read_mifare().get_data()
    if (card_id == bytearray(b'K\x01\x01\x00\x04\x08\x04G\x83\xf9\xd7'))\
        or (card_id == bytearray(b'K\x01\x01\x00\x04\x08\x04\x97\tq\xd7')):
        print('Unlock')
        card_status = True
    else:
        print('Not match')
        card_status = False
    return card_id


def read_id():
    global card_status
    card_status = False
    print('Waiting for the card')
    x = threading.Thread(target=check_id)
    x.start()   
    x.join(timeout=40)     
        # return_dict['detect'] = True
    # print("RFID timeout")
    return card_status

# read_id()

# manager = multiprocessing.Manager()
# return_dict = manager.dict()
# return_dict['detect'] = False

# process = Process(target=read_id, args=(return_dict,))
# process.start()
# process.join(timeout=5)
# process.terminate()
# not_detected(return_dict['detect'])



