#coding=utf-8
from imutils import perspective
import cv2
import numpy as np
import math

img1 = cv2.imread("newpic.png")
image = cv2.imread("newpic.png", 0)

#h,w = image.shape[:2]

fourPoint = [(0,0), (400, 0), (0,600), (400,600)]
minPoint = []
minFlag = 0
corners = cv2.goodFeaturesToTrack(image, 90, 0.1, 150)
corners = np.int0(corners)

# 简答的寻找极点坐标
for rx,ry in fourPoint:
	minFlag = 0
	#print rx, ry
	for i in corners:
		x,y = i.ravel()
		length = math.sqrt((rx - x)* (rx - x) + (ry-y)*(ry-y))
		if (minFlag < length):
			minFlag = length
			qx = x
			qy = y

	#print qx, qy
	minPoint.append((qx,qy))
	cv2.circle(img1, (qx,qy), 5, (255, 0, 255), -1)

warped = perspective.four_point_transform(img1, np.array(minPoint))

cv2.imshow("winname", img1)
cv2.imshow("winna1me", warped)
cv2.waitKey(0)