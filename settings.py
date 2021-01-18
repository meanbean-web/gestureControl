import time
import cv2

# declare new variables

scale_factor = 2.0
size, center_x = 0,0

fps = 0
frame_counter = 0
start_time = time.time()

text = 'No hand detected'

# Define left, right, size_up_th, size_down_th:

size_up_th = 1000
size_down_th = 1
left = 160
right = 480

# Downsize the frame:

def resize (frame, copy):

    new_width = int(frame.shape[1] / scale_factor)
    new_height = int(frame.shape[0] / scale_factor)

    resized_frame = cv2.resize(copy, (new_width, new_height))

    return resized_frame

# Draw lines:

def guidelines (frame):
    cv2.line(frame, (left, 0), (left, frame.shape[0]), (25, 25, 255), 2)
    cv2.line(frame, (right, 0), (right, frame.shape[0]), (25, 25, 255), 2)

    cv2.putText(frame, 'Center: {}'.format(center_x), (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (233, 100, 25), 1)
    cv2.putText(frame, 'size: {}'.format(size), (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (233, 100, 25))



