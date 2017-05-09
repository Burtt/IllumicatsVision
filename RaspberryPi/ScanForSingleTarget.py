#! /usr/bin/env python

import numpy as np
import cv2
import visiontable

display = False
cap = cv2.VideoCapture(0)
table = visiontable.VisionTable()
lower_lim = np.array([60,60,60])
upper_lim = np.array([100,255,255])
minContourArea = 400

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find contours
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

    # draw contours
    if(display):
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
            bx = int((rect[0][0] + rect[1][0])/2)
            by = int((rect[0][1] + rect[1][1])/2)
            
            # draw center
            if(display):
                box = np.int0(box)
                img = cv2.drawContours(img,[box],0,(0,0,255),1)
                img = cv2.circle(img,(bx,by),4,(0,255,255),-1)
            
            # publish results to dashboard
            table.update(True, bx, by)
            print str(bx) + " " + str(by)
            
        # Otherwise, assume it is noise
        else:
            table.update(False)
    else:
        table.update(False)
    
    

    # Display the resulting frame
    if(display):
        cv2.imshow('frame',img)

# When everything's done, release the capture
cap.release()
cv2.destroyAllWindows()
