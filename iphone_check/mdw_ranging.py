#coding=utf-8

# 图片距离计算 全面计算 外形的大小与实际尺寸
# 1 厘米 ＝0.3937 英寸   1 英寸=2.54 厘米   1点 = 1/72英寸

import cv2
import sys
img = cv2.imread("phone_pic/1122.png")

im1 = cv2.GaussianBlur(img, (3, 3), 0)
canny = cv2.Canny(im1, 40, 60, 2)

cnts,_ = cv2.findContours(canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print len(cnts)

for i in range(0, len(cnts)):
	area = cv2.contourArea(cnts[i])
	x,y,w,h = cv2.boundingRect(cnts[i])
	print x,y,w,h,area
cv2.drawContours(img, cnts, -1, (255,0,0))

cv2.imshow("winname", img)
cv2.waitKey(0)