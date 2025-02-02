# import the opencv library
import cv2 as cv
import numpy as np
import _thread
import datetime
import time
# import main

camera_recorded = True
global cap
global videoWriter
global vi_path
global cap_main
global videoWriter_main
global vi_path

vi_path=''
# cap = cv.VideoCapture(0)
# vid_cod = cv.VideoWriter_fourcc(*'XVID')
# videoWriter = cv.VideoWriter('/home/pi/Desktop/video.avi',vid_cod, 30.0, (640,480))


def Start_record(vi_path,camera_slot):
    # cap = main.cap
    # videoWriter = main.videoWriter

    global cap
    global videoWriter
    global camera_recorded
    
    cap = cv.VideoCapture(camera_slot)
    vid_cod = cv.VideoWriter_fourcc(*'XVID')
    # fourcc = cv.VideoWriter_fourcc(*'X264')
    videoWriter = cv.VideoWriter(vi_path,vid_cod, 30.0, (640,480))
   

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...", vi_path)
            cap.release()
            videoWriter.release()
            cv.destroyAllWindows()
            break
        else:
            cv.imshow('video', frame)
            videoWriter.write(frame)
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', gray)
        # print(camera_recorded)
        if camera_recorded == False:
            print('finished recorded')
            cap.release()
            videoWriter.release()
            cv.destroyAllWindows()
            
            break
    # When everything done, release the capture

def Stop_record():
    global cap
    global videoWriter
    global camera_recorded
    cap.release()
    videoWriter.release()
    cv.destroyAllWindows()
    print('stop')

def Start_record_main(vi_path,camera_slot):
    # cap = main.cap
    # videoWriter = main.videoWriter

    global cap_main
    global videoWriter_main
    global camera_recorded_main
    
    cap_main = cv.VideoCapture(camera_slot)
    vid_cod_main = cv.VideoWriter_fourcc(*'XVID')
    # fourcc = cv.VideoWriter_fourcc(*'X264')
    videoWriter_main = cv.VideoWriter(vi_path,vid_cod_main, 30.0, (640,480))
   

    if not cap_main.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap_main.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...", vi_path)
            cap_main.release()
            videoWriter_main.release()
            cv.destroyAllWindows()
            break
        else:
            cv.imshow('video', frame)
            videoWriter_main.write(frame)
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', gray)
        # print(camera_recorded)
        if camera_recorded == False:
            print('finished recorded')
            cap_main.release()
            videoWriter_main.release()
            cv.destroyAllWindows()
            
            break
    # When everything done, release the capture

def Stop_record_main():
    global cap_main
    global videoWriter_main
    global camera_recorded_main
    cap_main.release()
    videoWriter_main.release()
    cv.destroyAllWindows()
    print('stop')

# val = ''
# camera_status = ''

# val = input('Start record or Stop record (input as start or stop): ')

# c = 0

# while True:
#     if val == 'start':
#         c_name = str(c)
#         _thread.start_new_thread(start_record,(c_name,))
#         c += 1
#         val = ''
#         val = input('Start record or Stop record (input as start or stop): ')
#     elif val == 'stop':
#         camera_status = 'stop'
#         stop_record()
#         val = ''
#         val = input('Start record or Stop record (input as start or stop): ')
#     elif val != 'start' or val != 'stop':
#         print('The input does not match with the command.')
#     elif val == '':
#         val = input('Start record or Stop record (input as start or stop): ')
#     else:
#         continue