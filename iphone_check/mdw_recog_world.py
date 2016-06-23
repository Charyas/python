#coding=utf-8
import os
import subprocess
import time

# 图片中内容识别; 策略二
def calc_world(png):
	if (os.path.isfile('xyq.txt')):
		os.remove('xyq.txt')

	cmd = "tesseract.exe " + png + " xyq"
	#os.system("tesseract.exe htc.png xyq.txt")
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	# 延时 3s
	time.sleep(3)

	if (os.path.isfile('xyq.txt')):
		fd = open('xyq.txt', 'r')
		content = fd.read()
		fd.close()

	return content

# test
# if __name__ == '__main__':
# 	content = calc_world("htc.png")
# 	print content