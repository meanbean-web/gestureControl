import dlib
import cv2
import time
from appcontrol import right, left, size_up_th, size_down_th
import webbrowser
import pyautogui as pyg
import sys

# # open web browser to control
# url = 'https://templerun3.co/'
# openBrowser = webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
# webbrowser.get('chrome').open(url)
#
# # check if web browser was open
# if openBrowser = True :
#
#

# load detector
detector = dlib.simple_object_detector('Hand_Detector.svm')

# initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

scale_factor = 2.0

# Initially the size of the hand and its center x point will be 0
size, center_x = 0, 0

# Initialize these variables for calculating FPS
fps = 0
frame_counter = 0
start_time = time.time()

# PYG SETUP
screen_width, screen_height = tuple(pyg.size())
fourcc= cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('videorecord.mp4', fourcc, 15.0, (screen_width, screen_height))


#WHILE LOOP (processing the video stream)

while True:
    print('hoho helo' + frame_counter)

    try:

        # Read frame by frame
        ret, frame = cap.read()

        if not ret:
            break

        # Laterally flip the frame
        frame = cv2.flip(frame, 1)

        # Calculate the average FPS
        frame_counter += 1
        fps = (frame_counter / (time.time() - start_time))

        # Create a clean copy of the frame
        copy = frame.copy()

        # Downsize the frame:
        new_width= int(frame.shape[1] / scale_factor)
        new_height= int(frame.shape[0] / scale_factor)
        resized_frame= cv2.resize(copy, (new_width, new_height))

        # Detect with detector

        detections = detector(resized_frame)

        # Key = none initially
        key = None

        if len(detections) > 0:

            detection = detections[0]

            x1 = int(detection.left() * scale_factor)
            y1 = int(detection.top() * scale_factor)
            x2 = int(detection.right() * scale_factor)
            y2 = int(detection.bottom() * scale_factor)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'It is a hand?', (x1, y2 +20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255),2)

            # Calculate the size of the hand
            size = int((x2-x1) * (y2-y1))

            #Extract the center of the hand on the x-axis
            center_x = int(x1 + (x2 - x1) / 2)
            if center_x > right:
                pyg.write('Hello world!', interval=0.25)

            elif center_x < left:
                pyg.press = 'u'

            elif size > size_up_th:
                pyg.press = 'k'

            elif size > size_down_th:
                pyg.press = 'r'

        # Capture the screen
        image = pyg.screenshot()

        # Convert to BGR, numpy array
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Resize the camera frame and attach it to the screen
        resized_frame = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
        h = resized_frame.shape[0]
        h = resized_frame.shape[1]
        img[0:h, 0:w] = resized_frame

        # Save the video frame
        out.write(img)

        time.sleep(0.2)

    except KeyboardInterrupt:
        print('Releasing camera and exit program')
        cap.release()
        out.release()
        sys.exit()


