#! /usr/bin/env python

import numpy as np
import cv2
import visiontable

cap = cv2.VideoCapture(0)
table = visiontable.VisionTable()
lower_lim = np.array([80,23,235])
upper_lim = np.array([102,167,255])
minContourArea = 30

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find contours
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE) 

    if(len(contours) > 0):
        # find biggest contour
        biggestContourIndex = 0
        secondContourBiggestIndex = 0
        for i in range(len(contours)):
            if(cv2.contourArea(contours[i]) >
               cv2.contourArea(contours[biggestContourIndex])):
                secondContourBiggestIndex = biggestContourIndex
                biggestContourIndex = i
            elif(cv2.contourArea(contours[i]) >
                 cv2.contourArea(contours[secondContourBiggestIndex])):
                secondContourBiggestIndex = i

        # Check if second biggest contour is big enough
        if(cv2.contourArea(contours[biggestContourIndex]) > minContourArea):
            # find center
            recta = cv2.minAreaRect(contours[biggestContourIndex])
            rectb = cv2.minAreaRect(contours[secondBiggestIndex])
            boxa = np.int0(cv2.cv.boxPoints(recta))
            boxb = np.int0(cv2.cv.boxPoints(rectb))
            rect = cv2.minAreaRect(np.concatenate([boxa,boxb]))
            box = np.int0(cv2.cv.boxPoints(rect))
            bx = int((box[0][0] + box[2][0])/2)
            by = int((box[0][1] + box[2][1])/2)
            
            # publish results to dashboard
            table.update(True, bx, by)
            
        # Otherwise, assume it is noise
        else:
            table.update(False)
    else:
        table.update(False)

# When everything's done, release the capture
cap.release()
