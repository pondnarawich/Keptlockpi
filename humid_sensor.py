import time
import board
import adafruit_dht
import psutil
import requests
# from main import lid
# We first check if a libgpiod process is running. If yes, we kill it!




def check_humid(lid):
    print("Checking Humidity")
    sent = False
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    sensor = adafruit_dht.DHT11(board.D23)
    while True:
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            if humidity >= 75 and sent == False:
                # try:
                data = {"lid": str(lid), "raining": str(True)}
                url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(lid)
                r = requests.post(url, data=data) 
                sent = True
                print(data)
                # except:
                #     print("cannot send the humidity")
            elif humidity < 75 and sent == True:
                try:
                    data = {"lid": str(lid), "raining": str(False)}
                    url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(lid)
                    r = requests.post(url, data=data)
                    sent = False
                    print(data)
                except:
                    print("cannot send the humidity")
    
            # print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        except RuntimeError as error:
            # print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            sensor.exit()
            raise error
        time.sleep(1)