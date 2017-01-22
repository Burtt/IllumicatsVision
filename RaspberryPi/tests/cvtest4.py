#! /usr/bin/env python

import numpy as np
import cv2

img = cv2.imread("frclogo.jpg")
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_lim = np.array([0,155,155])
upper_lim = np.array([179,255,255])
mask = cv2.inRange(hsv, lower_lim, upper_lim)

cv2.imshow("logo",img)
cv2.imshow("masked",mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
