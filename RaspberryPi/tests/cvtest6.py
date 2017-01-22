import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_lim = np.array([25,60,60])
    upper_lim = np.array([100,255,255]) 
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    img = np.zeros((1000,1000,3), np.uint8)
    img = cv2.drawContours(img, contours, -1, (255,255,0), 3)


    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
