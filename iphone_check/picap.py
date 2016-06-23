#coding=utf-8
import cv2
import numpy as np
from PIL import Image

#降噪
#切割
#文本输出

BACKCOLOR = 0
TEXTCOLOR = 1
TEMPCOLOR = 2
BLOCK_MAX = 25
BLOCK_MEAN = 9

imgorg = cv2.imread('test.jpeg')
img = cv2.imread('test.jpeg', 0)

def binarized(img):
	h, w = img.shape
	print h, w
	threshold = 80
	for i in xrange(h):
		for j in xrange(w):
			if img.item(i, j) > threshold:
				img[i, j] = 255

	return img

def 
kernel = np.ones((3, 3), np.uint8)

# 膨胀
erosion = cv2.erode(img, kernel, iterations=1)

# 细化
dilation = cv2.dilate(img, kernel, iterations = 1)
cv2.imwrite("test.png", dilation)


# cv2.imshow('img', img1)
# cv2.waitKey(0)