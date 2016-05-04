#coding=utf-8


def readiproxy(filename):
	iproxy = []
	f = open(filename, 'r')
	buf = f.readlines(10000000)
	f.close
	for line in buf:
		line = line.strip('\n')
		iproxy.append(line)

	return iproxy

def checkip(proxy):
	handle = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(handle,urllib2.HTTPHandler)
	try:
		r = opener.open("http://www.baidu.com/img/baidu_jgylogo3.gif", timeout=5)
		l = len(r.read())
		if (l == 705):
			return True
		return False
	except Exception,e:
		return False

if __name__ == '__main__':
	file = open("iproxy.txt")
	buf = file.readlines(1000000000)
	file.close()

	buf = set(buf)

	file = open("reiproxy.txt","w+")
	file.writelines(buf)
	file.close()