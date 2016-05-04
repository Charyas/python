#coding=utf-8

import sys
from scapy.all import *

interface = 'mon0'
hiddenNets = []
unhiddenNets = []

def sniffDotll(p):
	if p.haslayer(DotllProbeResp):
		addr2 = p.getlayer(Dotll).addr2
		if (addr2 in hiddenNets) & (addr2 not in unhiddenNets):
			netName = p.getlayer(DotllProbeResp).info
			print '[+] Decloaked Hidden SSID: ' + netName + " for MAC: " + addr2
			unhiddenNets.append(addr2)

		if p.haslayer(DotllBeacon):
			if p.getlayer(DotllBeacon).info == "":
				addr2 = p.getlayer(Dotll).addr2
				if addr2 not in hiddenNets:
					print "[-] Detected Hidden SSID: " + 'with MAC:'+addr2
					hiddenNets.append(addr2)

sniff(iface=interface, prn=sniffDotll)