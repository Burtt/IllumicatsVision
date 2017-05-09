import numpy as np
import cv2

img = cv2.imread("frclogo.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_lim = np.array([0,155,155])
upper_lim = np.array([179,255,255])

# Threshold the HSV image to get highly saturated image
mask = cv2.inRange(hsv, lower_lim, upper_lim)

# find contours
image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# find biggist contour
biggestContourIndex = 0
for i in range(len(contours)):
    if(cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggestContourIndex])):
        biggestContourIndex = i


# find contours above 1000 area
#bigContours = filter(lambda a: cv2.contourArea(a) > 1000, contours)

# find centroid from moments
M = cv2.moments(contours[biggestContourIndex])
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print("centroid: " + str(cx) + ', ' + str(cy))

# find box around contour and it's center
rect = cv2.minAreaRect(contours[biggestContourIndex])
box = cv2.boxPoints(rect)
bx = int((box[0][0] + box[2][0])/2)
by = int((box[0][1] + box[2][1])/2)
print("center: " + str(bx) + ', ' + str(by))
box = np.int0(box)

# clear image
lower_lim = np.array([178,254,254])
mask = cv2.inRange(hsv, lower_lim, upper_lim)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# draw everything
mask = cv2.drawContours(mask,[box],0,(0,0,255),1)
mask = cv2.drawContours(mask, contours, biggestContourIndex, (0,255,0), 1)
mask = cv2.circle(mask,(cx,cy),4,(255,255,0),-1)
mask = cv2.circle(mask,(bx,by),4,(0,255,255),-1)

cv2.imshow("a",img)
cv2.imshow("b",mask)
cv2.moveWindow("b",600,50)
cv2.waitKey(0)
cv2.destroyAllWindows()

quit()
