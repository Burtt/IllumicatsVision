import numpy as np
import cv2
import datetime

# This script can be used to save an image from the webcam in order to determine
# the exact color of the target as seen from the webcam.
# Images are saved in as "cap Month-Day Hour_Minute_Second.png"
# Use SCP to copy images off of the pi

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite("cap {:%m-%d %H_%M_%S}.png".format(datetime.datetime.now()), frame)

cap.release()
