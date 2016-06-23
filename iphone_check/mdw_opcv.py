#coding=utf-8
import FileDialog
import cv2
import numpy as np
import matplotlib
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt
import Image
import sys
import glob

from mdw_recog_world import *


#获取图片中时候存在文字信息
def getPicContentWord(png):
	content = calc_world(png)
	content = content.strip('\n')
	return content

# 图片色彩偏色处理
def picFix():
	pass
	# 读取
	#初步判定方式
	#特征定义 iphone   矩形 40×6 或 16×16
	#现在不计算 点与点 之间的间距

	# 色彩填充空间
	# for row in range(0, y):
	# 	for col in range(0, x):
	# 		print img.item(row,col)
	# 		if img.item(row,col) > 150:
	# 			img.[row,col] = 255

#图片相似度
def picSamRate():
	pass

# 图片颜色识别
def colorReg(png):
	h,w = png.shape[:2]
	#print h,w
	# 长分为10等分 宽分为8等分
	steph = int(h/10)
	stepw = int(w/8)
	count = 0

	regReg = [(steph, stepw), (9*steph, 7*stepw), (steph, 7*stepw), (9*steph, stepw)]
	for x,y in regReg:
		if (png.item(x,y) > 150):
			count += 1

	if count > 2:
		print "color:white"
	else:
		print 'color:black'

	# 图片
	# 获取图片的大小，用于图片切割色彩分类管理
	# 颜色简单判断，深入需要定义为分块颜色处理<如：色值直方图>
	# 需要谋取几个中心点的位置
	# x = img.item(50, 40)
	# y = img.item(133, 200)
	# if abs(x - y) > 150:
	# 	print "white"
	# else:
	# 	print "black"

def picGrayBit(img):
	# 滤波消除图片上的点
	# cv2.medianBlur
	#高斯滤波变换
	im1 = cv2.GaussianBlur(img, (3, 3), 0)
	canny = cv2.Canny(im1, 40, 60, 2)
	#填充数据不完整部分 如果为黑色开启这种校准模式
	des = cv2.bitwise_and(im1, canny)
	return des

# 检测霍夫圆
def checkHoughCircle(img):
	global circleIphone
	circles1 = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT, 3, 30)
	if np.equal(circles1.all(), True):
		circles = circles1[0,:,:]
		circles = np.uint16(np.around(circles))
		for i in circles[:]:
			if (i[2] > 30):
				continue
			#print "glod"
			#记录圆圈的坐标
			cir1 = (i[0], i[1])
			circleIphone.append((i[0], i[1], i[2]))
			cv2.circle(img1, (i[0], i[1]), i[2], (255,0,0), 1)
			cv2.circle(img1, (i[0], i[1]), 1, (255,0,255), 1)

# 检测细条的
# lines = cv2.HoughLinesP(des, 1, np.pi/180, 211)
# lines1 = lines[:,0,:]
# for x1,y1,x2,y2 in lines1[:]:
# 	cv2.line(img1, (x1,y1), (x2,y2), (0, 255, 255), 3)

def drawRect(img, cnt, thresholdx, point, rgb, size):
	x,y,w,h = cv2.boundingRect(cnt)
	# if (w > thresholdx or h > thresholdx):
	# 	return False
	point.append((x,y,w,h))
	#print x,y,w,h
	#cv2.rectangle(img, (x,y), (x+w, y+h), rgb, size)
	return True
#轮廓分割
def contourPic(img):
	cnts,_ = cv2.findContours(img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#print len(cnts)

	# 获取轮廓最小面积
	#c = max(cnts, key=cv2.contourArea)
	#print cv2.minAreaRect(c)

	#print cv2.isContourConvex(cnts[0])
	#cnts = cv2.sort(cnts, True)

	#特征值过滤
	for i in range(0, len(cnts)):
		area = cv2.contourArea(cnts[i])
		# 特征获取累死摄像头的矩形区域
		if (area > 30) and (area < 80):
			drawRect(img1, cnts[i], 20, pointCam, (255,0,0), 2)
		elif (area > 100) and (area < 400):
			drawRect(img1, cnts[i], 60, pointRect, (0, 200, 0), 2)
		elif (area > 400):
			drawRect(img1, cnts[i], 1400, pointShape, (0, 200, 255), 2)

		# 计算极值
		pentagram = cnts[i]
		leftmost = tuple(pentagram[:,0][(pentagram[:,:,0].argmin() + pentagram[:,:,0].argmax())/2.0])


# # #判断极致点中的间距
# # #for x1,y1 in point:
# # 	#x = np.sqrt((x1-cir1[0])*(x1-cir1[0]) + (y1 - cir1[1])*(y1 - cir1[1]))
#func 轮廓实际尺寸检查
def regRealSize():
	print "1234"

# 轮廓检查
# 现有的模糊轮廓特征
def regionPhone(img, focusPoint, width, hight):
	global circleIphone
	global iphone5sflag
	global iphoneflag
	global iphone4sflag
	global pointIphone
	rectPos = list(set(focusPoint))
	for x,y,w,h in rectPos:

		#if h/w > 4

		cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)
		if (h*1000.0 / w) > 1900 and (h*1000.0 / w) < 2000:
			#print "pix: h=%d w=%d, size scale:%f"%(h,w, h*1000.0/w)
			#print "like 4/4s model"
			iphoneflag = 4
			cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

		if (h*1000.0 / w) > 2000 and (h*1000.0 / w) < 2200:
			#print "pix: h=%d w=%d, size scale:%f"%(h,w, h*1000.0/w)
			#print "like 5+ model"
			print (h*1000.0 / w)
			iphoneflag = 5
			cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

		if (h*1000.0/w) > 850 and (h*1000.0/w) < 1200:
			#print ('square')
			#if (y < hight/4) and abs(w-h) < 4:
				#print 'like camera logo h=%d w=%d'%(h,w)
			#if (y > 3*hight/4) and abs(w-h) < 4:
				#print 'like button logo h=%d w=%d'%(h,w)

			for xs,ys, r in circleIphone:
				if (abs(x - xs + w/2) < 5 and abs(y-ys + h/2) < 5 and abs(w + h - 4*r) <10):
					iphone5sflag = 1
			#print x,y,w,h
			cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

		if (h*1000.0/w) > 120 and (h*1000.0/w) < 500:
			#print 'like listen h=%d w=%d'%(h, w)
			if not pointIphone:
				pointIphone.append((x,y,w,h))
				#print pointIphone
			else:
				for rx,ry, rw, rh in pointIphone:
					if (abs(x - rx) < 3 and abs(y - ry) < 3 and abs(rw-w) < 3 and abs(rh-h) < 3):
						iphone4sflag = iphone4sflag - 1
			#for rx,ry,rw,rh in
			iphone4sflag = iphone4sflag + 1
			cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
		# if (w > 12)and (w < 15) and (h > 12) and (h < 15):
		# 	if (y < hight/4):
		# 		print 'like camera logo'

		# if (w > 6)and (w < 11) and (h > 6) and (h < 11):
		# 	if (y < hight/4) and abs(w-h) < 4:
		# 		print 'like camera logo'

		# if (w > 16)and (w < 22) and (h > 16) and (h < 22):
		# 	if (y > 3*hight/4) and abs(w-h) < 4:
		# 		print 'like button logo'

		#print x,y,w,h
		# if (w > 39)and (w < 70) and (h > 3) and (h < 20):
		# 	if (y < hight/4) and abs(w - h) > 25:
		# 		print "like iphone logo"

		# if (w > 22)and (w < 38) and (h > 6) and (h < 12):
		# 	if (y  < hight/4):
		# 		print 'like 4s logo'

		# if (w>39)and (w < 42) and (h>35) and (h < 42):
		# 	print "5s"

#

# 屏幕完整性检测
# 利用腐蚀 膨胀 检查区域内是否存在特定直线
def checkScreenIntact():
	print "screen intact"

# cam = list(set(pointCam))
# rect = list(set(pointRect))
# for x,y,w,h in rect:
# 	#print x,y,w,h
# 	if (w > 39)and (w < 42) and (h > 5) and (h < 8):
# 		print "iphone"
# 	if (w>39)and (w < 42) and (h>35) and (h < 42):
# 		print "5s"
# 	if (w > 24) and (w < 28) and (h > 5) and (h < 9):
# 		print "4s"
# shape = list(set(pointShape))

def getMaxRage(path):
	maxpoint = []
	img = cv2.imread(path, 0)
	# h, w = img.shape[:2]
	# print w, h

	im1 = cv2.GaussianBlur(img, (3, 3), 0)
	canny = cv2.Canny(im1, 40, 60, 2)
	#填充数据不完整部分 如果为黑色开启这种校准模式
	des = cv2.bitwise_and(im1, canny)

	contours,_ = cv2.findContours(des, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for i in xrange(len(contours)):
		x,y,w,h = cv2.boundingRect(contours[i])
		if not maxpoint:
			maxpoint.append((x, y, w, h))
		else:
			for rx,ry,rw,rh in maxpoint:
				if w - rw >= 0 and h - rh >= 0:
					del maxpoint[0]
					maxpoint.append((x,y,w,h))
					#print maxpoint

	print maxpoint
	return maxpoint


pointCam=[]
pointRect=[]
pointShape=[]

pointIphone = []
circleIphone = []

contours = []
count = 0

iphoneflag = 0
iphone4sflag = 0
iphone5sflag = 0

if __name__ == '__main__':

	imgPath = sys.argv[1]

	flag = int(sys.argv[2])
	print flag
	#print imgPath
	img1 = cv2.imread(imgPath)
	img = cv2.imread(imgPath, 0)

	region = getMaxRage(imgPath)
	#for x,y,w,h in region:
	# 	cv2.rectangle(img1, (abs(x - 5), abs(y - 5)), (x + w + 5, y + h + 5), (0, 255, 0), 3)

	x,y,w,h = region[0]
	imgcut = img[abs(y - 5): (y + h + 5), abs(x - 5):(x + w + 5)]
	#cv2.imshow("winname111", imgcut)
	h,w=imgcut.shape[:2]
	print h,w
	colorReg(imgcut)

	des = picGrayBit(imgcut)
	# 检查是否含有字体
	print getPicContentWord(imgPath)

	# 简单识别iphone
	# 检查
	print checkHoughCircle(des)

	#
	contourPic(des)
	regionPhone(imgcut, pointCam, w, h)
	regionPhone(imgcut, pointRect, w, h)
	regionPhone(imgcut, pointShape, w, h)

	if iphoneflag == 4:
		if iphone4sflag == 2:
			print "model:iPhone 4S"
		else:
			print "model:iPhone 4"
	elif iphoneflag == 5:
		if iphone5sflag == 1:
			print "model:iPhone 5S"
		else:
			print "model:iPhone 5"
	else:
		print "model:unknow"

	# print list(set(pointCam))
	# print list(set(pointRect))
	# print list(set(pointShape))

	#cv2.drawContours(img1, cnts, -1, (255,0,255), 1)
	if (flag == 1):
		cv2.namedWindow("winname", cv2.WINDOW_NORMAL)
		cv2.imshow("winname", imgcut)
		cv2.waitKey(0)