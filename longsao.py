#coding=utf-8

import requests

def get1():
	url = "https://api2.iavnight.com/v2/genres/all"

	headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VfaWQiOiI1Mzg1YTYyNzIwMTk4NyIsImF1ZCI6ImF2bmlnaHQiLCJpYXQiOjE1MDI3MDI1NjgsInZpZGVvX2V4cGlyZWQiOjE1OTczMTA1NjgsIm1vZGVsIjoiUmFnZW50ZWsgZDk4NjdfMzVNNjVVIiwicGxhdGZvcm0iOiJhbmRyb2lkIiwidmVyc2lvbiI6IjIuMS4xIiwiZXhwIjoxNTAzMTM0NTY4fQ.qeuKcA3lZl5TOLSF_vJQioImoiUm2NJLsHJ4ZA6pUak',
	'Host': 'api2.iavnight.com',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'User-Agent': 'okhttp/3.3.1'
	}

	r = requests.get(url, headers=headers)

	print r.text

def get2():
	url = "https://api2.iavnight.com/v2/actors"

	headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VfaWQiOiI1Mzg1YTYyNzIwMTk4NyIsImF1ZCI6ImF2bmlnaHQiLCJpYXQiOjE1MDI3MDI1NjgsInZpZGVvX2V4cGlyZWQiOjE1OTczMTA1NjgsIm1vZGVsIjoiUmFnZW50ZWsgZDk4NjdfMzVNNjVVIiwicGxhdGZvcm0iOiJhbmRyb2lkIiwidmVyc2lvbiI6IjIuMS4xIiwiZXhwIjoxNTAzMTM0NTY4fQ.qeuKcA3lZl5TOLSF_vJQioImoiUm2NJLsHJ4ZA6pUak',
	'Host': 'api2.iavnight.com',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'User-Agent': 'okhttp/3.3.1'
	}

	r = requests.get(url, headers=headers)

	print r.text


def get3():
	url = "https://api2.iavnight.com/v2/videos/GACHI1144?v=122&lang=CN"
	headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VfaWQiOiI1Mzg1YTYyNzIwMTk4NyIsImF1ZCI6ImF2bmlnaHQiLCJpYXQiOjE1MDI3MDI1NjgsInZpZGVvX2V4cGlyZWQiOjE1OTczMTA1NjgsIm1vZGVsIjoiUmFnZW50ZWsgZDk4NjdfMzVNNjVVIiwicGxhdGZvcm0iOiJhbmRyb2lkIiwidmVyc2lvbiI6IjIuMS4xIiwiZXhwIjoxNTAzMTM0NTY4fQ.qeuKcA3lZl5TOLSF_vJQioImoiUm2NJLsHJ4ZA6pUak',
	'Host': 'api2.iavnight.com',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'User-Agent': 'okhttp/3.3.1'
	}

	r = requests.get(url, headers=headers)

	print r.text

if __name__ == '__main__':
	#get()
	get3()