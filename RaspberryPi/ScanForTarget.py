#! /usr/bin/env python

import numpy as np
import cv2
import visiontable

cap = cv2.VideoCapture(0)
table = visiontable.VisionTable()
lower_lim = np.array([60,60,60])
upper_lim = np.array([100,255,255])
minContourArea = 400

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find contours
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    img, contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

    # draw contours
    imW = np.size(frame, 0)
    imH = np.size(frame, 1)
    img = np.zeros((imW,imH,3), np.uint8)
    img = cv2.drawContours(img, contours, -1, (255,255,0), 3)

    if(len(contours) > 0):
        # find biggest contour
        biggestContourIndex = 0
        for i in range(len(contours)):
            if(cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggestContourIndex])):
                biggestContourIndex = i

        # Check if biggest contour is big enough
        if(cv2.contourArea(contours[biggestContourIndex]) > minContourArea):
            # find center
            rect = cv2.minAreaRect(contours[biggestContourIndex])
            box = cv2.boxPoints(rect)
            bx = int((box[0][0] + box[2][0])/2)
            by = int((box[0][1] + box[2][1])/2)
            
            # draw center
            box = np.int0(box)
            img = cv2.drawContours(img,[box],0,(0,0,255),1)
            img = cv2.circle(img,(bx,by),4,(0,255,255),-1)
            
            # publish results to dashboard
            table.update(True, bx, by)
            
        # Otherwise, assume it is noise
        else:
            table.update(False)
    else:
        table.update(False)
    
    

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything's done, release the capture
cap.release()
cv2.destroyAllWindows()
