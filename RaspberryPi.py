import pyautogui as pyg
import dlib
import cv2
from settings import *
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

#DECLARE CAMERA MODULE
camera = PiCamera()
camera.resolution = (848, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(848, 480))
camera.vflip = True

time.sleep(0.2)

#from appcontrol import right, left, size_up_th, size_down_th
import sys

# print(pyg.size())
# print(pyg.position())

# load detector
detector = dlib.simple_object_detector('Hand_Detector.svm')


#GET REAL TIME VIDEO STREAM FOR RASPI

counter = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    counter += 1
    cap = frame.array
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        # Calculate the average FPS

        frame_counter += 1
        fps = (frame_counter / (time.time() - start_time))
        copy = frame.copy()
        resized_frame = resize(frame, copy)
        guidelines(frame)

        # print(resized_frame)

        detections = detector(resized_frame)

        if len(detections) > 0:

            detection = detections[0]

            # detection = detections[0]

            x1 = int(detection.left() * scale_factor)
            y1 = int(detection.top() * scale_factor)
            x2 = int(detection.right() * scale_factor)
            y2 = int(detection.bottom() * scale_factor)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'Is it a hand?', (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Calculate the size of the hand

            size = int(x2 - x1 * (y2 - y1))

            # Extract the center of the hand on x-axis
            center_x = int(x1 + (x2 - x1) / 2)

            # print(center_x)

            # Display center of hand, for our own sake

            # cv2.circle(frame, center_x, 1, (0, 255, 0))

            # DECIDE WHETHER IT'S LEFT OR RIGHT

            if center_x > right:
                pyg.press('right')
                text = 'pressed right'

            elif center_x < left:
                pyg.press('left')
                text = 'pressed left'

            elif size > size_up_th:
                pyg.press('up')
                text = 'pressed up'

            elif size < size_down_th:
                pyg.press('down')
                text = 'pressed down'

            # if size_down_th

            image = pyg.screenshot()

            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            # Display the text associated with left/ right detections
            cv2.putText(frame, text, (220, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (33, 100, 185), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




