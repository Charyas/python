#coding=utf-8
#用于图片转换 jpeg  png 填充色彩
#颜色检测
import cv2

#img = cv2.imread("huawei.png")
img = cv2.imread("phone_pic/1122.png", 0)

# img = cv2.GaussianBlur(img, (3, 3), 0)
# canny = cv2.Canny(img, 40, 60, 2)

x,y= img.shape[:2]
print x, y

for i in xrange(x):
	for j in xrange(y):
		if img.item(i,j) < 66:
			img[i, j] = 0
		elif img.item(i,j) < 110:
			img[i, j] = 50
		elif img.item(i, j) > 140:
			img[i, j] = 250


cv2.imshow("winname", img)
cv2.waitKey()