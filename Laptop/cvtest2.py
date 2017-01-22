import numpy as np
import cv2

cap = cv2.VideoCapture(1)

def findBiggestContour(contours):
    biggestContourIndex = 0
    for i in range(len(contours)):
        if(cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggestContourIndex])):
            biggestContourIndex = i
    return biggestContourIndex

def findSecondBiggestContour(contours):
    biggestContourIndex = 0
    secondBiggest = 0
    for i in range(len(contours)):
        if(cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggestContourIndex])):
            secondBiggest = biggestContourIndex
            biggestContourIndex = i
    return secondBiggest

def findBigContours(contours):
    bigContours = []
    for i in range(len(contours)):
        if(cv2.contourArea(contours[i]) > 450):
            bigContours.append(contours[i])
    return bigContours

def findBestAR(contours):
    bestMatchIndex = 0
    bestMatch = 100
    idealAR = 0.4
    for i in range(len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        if(abs((w/float(h)) - idealAR) < bestMatch):
            bestMatchIndex = i
            bestMatch = abs((w/float(h)) - idealAR)
    return bestMatchIndex

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#HSV
    lower_lim = np.array([45,2,240])#45,2,248
    upper_lim = np.array([130,40,255])#100,14,255
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    img, contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.inRange(hsv, lower_lim, upper_lim)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    
    # find big contours
    biggestContourIndex = findBiggestContour(contours)
    secondBiggestIndex = findSecondBiggestContour(contours)
    #bigContours = findBigContours(contours)
    #biggestContourIndex = findBestAR(bigContours)
    if(len(contours) != 0):
        # find box around contour and it's center
        recta = cv2.minAreaRect(contours[biggestContourIndex])
        rectb = cv2.minAreaRect(contours[secondBiggestIndex])
        boxa = cv2.boxPoints(recta)
        boxb = cv2.boxPoints(rectb)
        rect = cv2.minAreaRect(np.concatenate([boxa,boxb]))
        box = cv2.boxPoints(rect)
        bx = int((box[0][0] + box[2][0])/2)
        by = int((box[0][1] + box[2][1])/2)
        #x,y,w,h = cv2.boundingRect(contours[biggestContourIndex])
        #if(h != 0):
        #    print("aspect ratio: " + str(h/float(w)))
        #print("center: " + str(bx) + ', ' + str(by))
        box = np.int0(box)
        img = cv2.drawContours(img,[box],0,(0,0,255),1)
        img = cv2.circle(img,(bx,by),4,(0,255,255),-1)

        # find centroid from moments
        #M = cv2.moments(contours[biggestContourIndex])
        #if(M['m00'] != 0):
        #    cx = int(M['m10']/M['m00'])
        #    cy = int(M['m01']/M['m00'])
        #    img = cv2.circle(img,(cx,cy),4,(255,255,0),-1)
    
    img = cv2.drawContours(img, contours, biggestContourIndex, (255,255,0), 3)
    
    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
