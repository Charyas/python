#coding=utf-8

from ctypes import *
import sys
import os
import hashlib
import httplib2
import urllib
import string
import zlib
import binascii
import random

# reload(sys)
# sys.setdefaultencoding('utf8')

def getFileMd5(strFile):
    file = None
    bRet = False
    strMd5 = ""
    try:
        file = open(strFile, "rb")
        md5 = hashlib.md5()
        strRead = ""
        while True:
            strRead = file.read(8096)
            if not strRead:
                break
            md5.update(strRead)
        #read file finish
        bRet = True
        strMd5 = md5.hexdigest()
    except:
        bRet = False
    finally:
        if file:
            file.close()

    return [bRet, strMd5]

def getFileCRC(filename):
    f = None
    bRet = False
    crc = 0
    blocksize = 1024 * 64
    try:
        f = open(filename, "rb")
        str = f.read(blocksize)
        while len(str) != 0:
                crc = binascii.crc32(str,crc) & 0xffffffff
                str = f.read(blocksize)
        f.close()
        bRet = True
    except:
        print("compute file crc failed!"+filename)
        return 0
    return [bRet, '%x' % crc]

def checkResult(dllResult, s_id, softVerifyKey, codeid):
    bRet = False;
    #print(dllResult)
    #print(len(dllResult))
    if(len(dllResult) < 0):
        return [bRet, dllResult]
    items=dllResult.split('_')
    verify=items[0]
    code=items[1]

    localMd5=hashlib.md5('%d%s%d%s'%(s_id, softVerifyKey, codeid, (code.upper()))).hexdigest().upper()
    if(verify == localMd5):
        bRet = True;
        return [bRet, code];
    return [bRet, "md5 failed"]

def look_result(pic_file_path):
    UUDLL='UUWiseHelper.dll'
    #os.path.join(os.path.dirname(__file__), 'UUWiseHelper.dll')

    s_id  = 109952
    s_key = "ebeb931edec04a74b56f63a476b29624"
    UU = windll.LoadLibrary(UUDLL)

    setSoftInfo = UU.uu_setSoftInfoW
    login = UU.uu_loginW
    recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
    getResult = UU.uu_getResultW
    uploadFile = UU.uu_UploadFileW
    getScore = UU.uu_getScoreW
    checkAPi=UU.uu_CheckApiSignW

    dllMd5=getFileMd5(UUDLL)
    dllCRC32=getFileCRC(UUDLL)
    randChar=hashlib.md5(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()').encode('utf-8')).hexdigest()
    softVerifyKey="D51593F6-D44E-4DE3-8DB6-BB93173810F4"

    checkStatus=hashlib.md5(('%d%s%s%s%s'%(s_id,(softVerifyKey.upper()),(randChar.upper()),(dllMd5[1].upper()),(dllCRC32[1].upper()))).encode('utf-8')).hexdigest()

    serverStatus=c_wchar_p("")
    checkAPi(c_int(s_id), c_wchar_p(s_key.upper()),c_wchar_p(randChar.upper()),c_wchar_p(dllMd5[1].upper()),c_wchar_p(dllCRC32[1].upper()),serverStatus)
    if not (checkStatus == serverStatus.value):
    	#print("sorry, api file is modified")
    	sys.exit(0)
    user = c_wchar_p("zecharywoo")
    passwd = c_wchar_p("tbihia1234!@#$")

    #setSoftInfo(c_int(s_id), c_wchar_p(s_key))
    ret = login(user, passwd)

    if ret < 0:
        #print('login error,errorCode:%d' %ret )
        sys.exit(0)

    ret = getScore(user, passwd)
    #print('The Score of User : %s  is :%d' % (user.value, ret))
    result=c_wchar_p("                                              ")
    #print pic_file_path
    code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(8003),result)
    if code_id <= 0:
        return ""
        #print('get result error ,ErrorCode: %d' % code_id)
    else:
        checkedRes=checkResult(result.value, s_id, softVerifyKey, code_id)
        print("the resultID is :%d result is %s" % (code_id,checkedRes[1]))
        return checkedRes[1]

if __name__ == '__main__':
    # pic_file_path = os.path.join(os.path.dirname(__file__), 'test_pics', 'test_001.jpg')
    # print pic_file_path
    pic_file_path = r'test_pics\\test_001.jpg'
    print(look_result(pic_file_path))