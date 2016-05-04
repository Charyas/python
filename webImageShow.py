#coding=utf-8
#
#
from PIL import Image
import requests

def downLoadImage():
	url = 'http://www.baidu.com/img/baidu_jgylogo3.gif'

	r = requests.get(url)
	print r.content
	with open("aaa.gif", "wb") as f:
		f.write(r.content)
		f.close()

def showImage(filename):
	img = Image.open(filename)
	img.show()


downLoadImage()
showImage("bbbb")