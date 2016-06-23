import cv2
import numpy as np

imgorg = cv2.imread("newpic.png")
img = cv2.imread("newpic.png", 0)

dst = cv2.cornerHarris(img, 2, 3, 0.04)
dst = cv2.dilate(dst, None)

imgorg[dst>0.01*dst.max()] = [0,0,255]

#########
#corners = cv2.goodFeaturesToTrack(img, 25, 0.001, 10)


cv2.imshow("winname", imgorg)
cv2.waitKey(0)