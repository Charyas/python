#coding=utf-8
import optparse
import socket
from socket import *
from threading import *

import nmap

screenLock = Semaphore(value=1)

def nmapScan(tgtHost, tgtPort):
	nmScan = nmap.PortScanner()
	nmScan.scan(tgtHost, tgtPort)
	state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
	print '[*] ' + tgtHost + "Tcp/" + tgtPort + " " + state

def connScan(tgtHost, tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		connSkt.send('hiPython\r\n')
		results = connSkt.recv(100)
		screenLock.acquire()
		print '[+]%d/tcp open' % tgtPort
		print '[+] ' + str(results)
		connSkt.close()
	except:
		screenLock.acquire()
		print '[-]%d/tcp closed' % tgtPort
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost, tgtPorts):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve '%s': Unknow host" % tgtHost
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print '\n[+] Scan Results for : ' + tgtName[0]
	except:
		print "\n[+] Scan Results for : " + tgtIP
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		print 'Scanning port ' + tgtPort
		t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
		#connScan(tgtHost, int(tgtPort))
		t.start()

def main():
	parser = optparse.OptionParser('usage%prog -H <target host> -p <target port>')
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')

	(options, args) = parser.parse_args()
	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(', ')

	if (tgtHost == None) | (tgtPorts[0] == None):
		print parser.usage
		exit(0)
	# print tgtPorts
	# portScan(tgtHost, tgtPorts)
	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
	main()
	# python scanport.py -H 192.168.2.35 -p "21, 22, 80"