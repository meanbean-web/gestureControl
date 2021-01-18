import dlib
import cv2
import pyautogui as pyg
import time
import numpy as np
from appcontrol import right, left, size_up_th, size_down_th
import sys
import webbrowser

# Load our trained detector
detector = dlib.simple_object_detector('Hand_Detector.svm')

# Initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Setting the downscaling size, for faster detection
# If you're not getting any detections then you can set this to 1
scale_factor = 2.0

# Initially the size of the hand and its center x point will be 0
size, center_x = 0, 0

# Initialize these variables for calculating FPS
fps = 0
frame_counter = 0
start_time = time.time()

# Set Player = True in order to use this script for the VLC video player
player = False

# This variable is True when we press a key and False when there is no detection.
# It's only used in the video Player
status = False

# We're recording the whole screen to view it later
screen_width, screen_height = tuple(pyg.size())
out = cv2.VideoWriter(r'videorecord.mp4', cv2.VideoWriter_fourcc(*'XVID'), 15.0, (screen_width, screen_height))


# Set the while loop
while (True):

    try:

        # Read frame by frame
        ret, frame = cap.read()

        if not ret:
            break

        # Laterally flip the frame
        frame = cv2.flip(frame, 1)

        # Calculate the Average FPS
        frame_counter += 1
        fps = (frame_counter / (time.time() - start_time))

        # Create a clean copy of the frame
        copy = frame.copy()

        # Downsize the frame.
        new_width = int(frame.shape[1] / scale_factor)
        new_height = int(frame.shape[0] / scale_factor)
        resized_frame = cv2.resize(copy, (new_width, new_height))

        # Detect with detector
        detections = detector(resized_frame)

        # Key will initially be None
        key = None

        if len(detections) > 0:

            # Grab the first detection
            detection = detections[0]

            # Since we downscaled the image we will need to resacle the coordinates according to the original image.
            x1 = int(detection.left() * scale_factor)
            y1 = int(detection.top() * scale_factor)
            x2 = int(detection.right() * scale_factor)
            y2 = int(detection.bottom() * scale_factor)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'Hand Detected', (x1, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)

            # Calculate size of the hand.
            size = int((x2 - x1) * (y2 - y1))

            # Extract the center of the hand on x-axis.
            center_x = int(x1 + (x2 - x1) / 2)

            # Press the required button based on center_x location and size
            # The behavior of keys will be different depending upon if we're controlling a game or a video player.
            # The status variable makes sure we do not double press the key in case of a video player.

            if center_x > right:

                key = 'right'
                if player and not status:
                    pyg.hotkey('ctrl', 'right')
                    status = True

            elif center_x < left:

                key = 'left'
                if player and not status:
                    pyg.hotkey('ctrl', 'left')
                    status = True

            elif size > size_up_th:

                key = 'up'
                if player and not status:
                    pyg.press('space')
                    status = True

            elif size < size_down_th:
                key = 'down'

            # Check if we're playing a game then press the required key
            if key is not None and player == False:
                pyg.press(key)

                # If there wasn't a detection then the status is made False
        else:
            status = False

        # Capture the screen
        image = pyg.screenshot()

        # Convert to BGR, numpy array (Opencv format of image)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Resize the camera frame and attach it to screen.
        resized_frame = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
        h = resized_frame.shape[0]
        w = resized_frame.shape[1]
        img[0:h, 0:w] = resized_frame

        # Save the video frame
        out.write(img)

        # time.sleep(0.2)
    except KeyboardInterrupt:
        print('Releasing the Camera and exiting since the program was stopped')
        cap.release()
        out.release()
        sys.exit()
