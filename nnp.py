#coding=utf-8

import sys
import math
import numpy as np

def calnt(count):
	X = np.array(count)
	out = np.linalg.eig(X)

	return out

def parse(line):
	line = line.replace("sin", "math.sin")
	line = line.replace("cos", "math.cos")
	line = line.replace("pi", "math.pi")
	print(line)

	return eval(line)

if __name__ == '__main__':

	cnt = list(sys.argv[1])

	data = []
	new = []

	word = ""

	count = 0
	out = 0.0
	for c in cnt:
		count += 1
		if c == ']':
			#parse(word)
			#if (count == len(cnt)):
			out = parse(word)
			new.append(out)
			word = ""

			data.append(new)
			#print (data)
			new = []
			continue

		if c == '[' or c == ',':
			if word == "":
				continue
			out = parse(word)
			word = ""
			new.append(out)
			continue
		word += c

	out = calnt(data)
	print(out)
