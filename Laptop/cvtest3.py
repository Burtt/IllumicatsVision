import numpy as np
import cv2
import math
import time

capA = cv2.VideoCapture(1)
capB = cv2.VideoCapture(2)
#print capA.get(cv2.CAP_PROP_FRAME_WIDTH)   640
#print capA.get(cv2.CAP_PROP_FRAME_HEIGHT)  480
#capA.release()
#capB.release()
#time.sleep(100)

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
        elif(cv2.contourArea(contours[i]) > cv2.contourArea(contours[secondBiggest])):
            secondBiggest = i
        #//else
            #smaller than both current biggest and second biggest
    return biggestContourIndex, secondBiggest

def findBigContours(contours):
    bigContours = []
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        hull = cv2.convexHull(contours[i])
        hull_area = cv2.contourArea(hull)
        if(hull_area == 0):
            continue
        solidity = float(area)/hull_area
        if(solidity > .75):#450
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

def processCam(cap):
    bx = -1
    by = -1



    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#HSV
    #white led ring: 45,2,240 - 130,40,255
    lower_lim = np.array([37,10,180])#80,23,235
    upper_lim = np.array([106,63,255])#102,167,255
    mask = cv2.inRange(hsv, lower_lim, upper_lim)
    img, contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.inRange(hsv, lower_lim, upper_lim)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    contours = findBigContours(contours)
    # find big contours
    #biggestContourIndex = findBiggestContour(contours)
    biggestContourIndex, secondBiggestIndex = findSecondBiggestContour(contours)
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
    
    #img = cv2.drawContours(img, contours, biggestContourIndex, (255,255,0), 3)
    #img = cv2.drawContours(img, contours, secondBiggestIndex, (255,0,0), 3)
    for i in range(len(contours)):
        col = cv2.contourArea(contours[i]) / 20
        img = cv2.drawContours(img, contours, i, (0,255-col,col), 1)
    return img, bx, by
    #print(str(len(contours)) + " " + str(secondBiggestIndex) + " " + str(biggestContourIndex))

def getBinocularDistance(xa, xb):
    #xb should be the left camera
    #half of the ipd (inches)
    ipd = 2.1875
    #fov angle from perpendicular
    fov = 60.0 #54
    #assume max is 640
    xRes = 640.0
    normA = xa/xRes
    angleA = (normA * 2 * (90-fov)) + fov
    slopeA = math.tan((math.pi/180.0)*angleA)
    slopeA = math.tan( (math.pi/180.0) * (( normA*2*(90.0-fov)+fov )))
    #print "slopeA " + str(slopeA)
    normB = xb/xRes
    slopeB = math.tan( (math.pi/180.0) * (( normB*2*(90.0-fov)+fov )))
    #print "slopeB " + str(slopeB)
    distance = (2*ipd*slopeA*slopeB)/(slopeA-slopeB)
    return distance

while(True):    
    imgA, ax, ay = processCam(capA)
    imgB, bx, by = processCam(capB)
    #print str(ax) + " " + str(bx)
    if(ax > 0 and bx > 0 and ax != bx):
        #dist = 1
        print getBinocularDistance(ax,bx)/12
    
    # Display the resulting frames
    cv2.imshow('frameA',imgA)
    cv2.imshow('frameB',imgB)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
capA.release()
capB.release()
cv2.destroyAllWindows()
