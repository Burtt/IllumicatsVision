import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_lim = np.array([40,100,100])
    upper_lim = np.array([80,255,255]) 
    mask = cv2.inRange(hsv, lower_lim, upper_lim)

    # Display the resulting frame
    cv2.imshow('frame',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
