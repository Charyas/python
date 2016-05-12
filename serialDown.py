#coding=utf-8
#
import serial
import sys
import pygame

BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200)

if __name__ == '__main__':
	global flag
	#TODO: using optparse
	com = sys.argv[1]
	baudrate = sys.argv[2]

	data = sys.argv[3]

	ser = serial.Serial(com, baudrate)
	# if ser.isOpen() == True:
	# 	print "%s is open"%(com)
	# 	sys.exit(0)
	datasize = len(data)
	flag = True

	while flag:
		# TODO: split data
		ser.write(data)
		#flag = False

	ser.close()