# import the opencv library
import cv2 as cv
import numpy as np
import _thread
import datetime
import time

class Camera:

    global cap
    global videoWriter
    global camera_status

    def start_record():
        global cap
        global videoWriter

        global camera_status

        tm = time.time()

        t = str(tm)

        camera_status = ''

        cap = cv.VideoCapture(0)
        vid_cod = cv.VideoWriter_fourcc(*'XVID')
        videoWriter = cv.VideoWriter('/home/pi/Desktop/video'+t+'.avi',vid_cod, 30.0, (640,480))

        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            else:
                cv.imshow('video', frame)
                videoWriter.write(frame)
            # Our operations on the frame come here
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv.imshow('frame', gray)
            if camera_status == 'stop':
                break
        # When everything done, release the capture

    def stop_record():
        cap.release()
        videoWriter.release()
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