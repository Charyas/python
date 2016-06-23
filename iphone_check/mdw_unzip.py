#coding=utf-8
import os
import sys
from zipfile import *

def unzip(source):
	pos = source.find(".ipsw")
	if pos < 0:
		return False

	dir = source[0:pos]
	os.mkdir(dir)
	#print dir
	zip = ZipFile(source, allowZip64=True)
	zip.extractall(dir)
	zip.close()
	print "DONE"
	return True

if __name__ == '__main__':
	print len(sys.argv)
	ipsw = sys.argv[1]

	#ipsw = 'iPhone6,1_9.2_13C75_Restore.ipsw'
	unzip(ipsw)