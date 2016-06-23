#coding=utf-8
# 图片相似度比较

import cv2

#图片分割
def picSplit(img, xs, se, ys, ye):
	#newImg = img.crop(region)
	#cv2.imwrite("aaa.png", newImg)
	im = img[xs:ys, se:ye]


#策略三
# 图片直方率(比较两幅图的相似度)
def histoGramRate(img1, img2, formatH):
	hist1 = cv2.calcHist(img1, [0], None, [256], [0.0, 255.0])
	hist2 = cv2.calcHist(img2, [0], None, [256], [0.0, 255.0])

	#cv2.cv.CV_COMP_BHATTACHARYYA
	result = cv2.compareHist(hist1, hist2, formatH)
	print (result)

# 手机上的图标识别
def logoReg():
	pass

def check

# 物体纹理辨别
img2 = cv2.imread('phone_pic/matchIphone.png')
img = cv2.imread("phone_pic/iphone5bai.png")

fast = cv2.FastFeatureDetector()
kp = fast.detect(img, None)
# cv2.drawKeypoints(img, kp, color=(255, 0, 0))



# x = cv2.Sobel(img,cv2.CV_16SC1,1,0)
# y = cv2.Sobel(img,cv2.CV_16S,0,1)

# absX = cv2.convertScaleAbs(x)
# absY = cv2.convertScaleAbs(y)
# cv2.imshow("absX", absX)
# cv2.imshow("absY", absY)
# dst = cv2.addWeighted(absX,0.2,absY,0.2,0)
# print img.shape
#regRect = []
#im = img[0:100, 100:200]

cv2.imshow("histImgB", img2)
cv2.waitKey(0)