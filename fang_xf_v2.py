#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=gbk

# 脚本名称：dazhou.fang_zddl_*.py
# 作    者：Tang Cheng
# 目标网站：http://dazhou.fang.com/
# 爬点网址：http://dazhou.fang.com/
# 数 据 库：MySQL pymysql
# 创建日期：2016.04.18
# 更新日期：2016.04.18
# 版    本：v1.0
# 修改事项：v1.0-创建爬虫程序。
# 描    述：这个脚本是为了实现自动登陆搜房网。
# 项目结束：
#
# 问题修改：

import re
import urllib
import urllib.request
import pymysql
import time
import chardet
import gzip

start_time = time.time()
print ("开始时间: %s" % time.ctime(start_time))

# headers。http://www.dzfc.com/
headers_fang = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',}

# 测试网站
# http://dazhou.fang.com/
# http://newhouse.dazhou.fang.com/house/web/Search_Result.php
# http://jiangwanchenghy.fang.com/house/3229072754/housedetail.htm
url_fang = 'http://newhouse.dazhou.fang.com/house/web/Search_Result.php'
req_fang = urllib.request.Request(url_fang,headers=headers_fang)
html_fang = urllib.request.urlopen(req_fang)
html_fang = html_fang.read()
# html_fang = html_fang.decode('utf-8', 'ignore')
# print(html_fang)

# 解压数据
# result = gzip.decompress(获取的字节数据))
html_fang_gzip = gzip.decompress(html_fang)
# print(result)
result_charset = chardet.detect(html_fang_gzip)
# print(result_charset)
bianma = result_charset['encoding']
if bianma == 'utf-8' or bianma == 'UTF-8':
    html_fang_gzip = html_fang_gzip
else:
    html_fang_gzip = html_fang_gzip.decode('gb2312', 'ignore')
# print(html_fang_gzip)

# 获取链接
# <div class="sslaimg" id="sjina_.*?"><a target="_blank" href="(.*?)"><img height="120" width="160" border="0" alt=".*?" src=".*?"/></a></div>
url_xf_list = re.findall(r'<div class="sslaimg" id="sjina_.*?"><a target="_blank" href="(.*?)"><img height="120" width="160" border="0" alt=".*?" src=".*?"/></a></div>', html_fang_gzip, re.M|re.I|re.S)[0:]
# print ("新房链接列表：%s" %url_xf_list)

url_xf_list_len = len(url_xf_list)
# print(url_xf_list_len)
if url_xf_list_len > 0:
    # 遍历一维数组
    # for i in range(0, 1): # 测试使用
    for i in range(0, url_xf_list_len):
        url_xinfang_dan = url_xf_list[i]
        print("新楼盘链接：%s" %url_xinfang_dan)
        # 数据最终来源网页。
        # http://www.dzfc.com/fangyuan/house/201604/42951/1.html#g=1
        req_xf = urllib.request.Request(url_xinfang_dan, headers=headers_fang)
        html_xf = urllib.request.urlopen(req_xf)
        html_xf = html_xf.read()
        # html_xf = html_xf.decode('utf-8', 'ignore')
        # 数据存在乱码，又被压缩了。
        # print(html_xf)

        html_xf_gzip = gzip.decompress(html_xf)
        # print(result)
        result_charset = chardet.detect(html_xf_gzip)
        # print(result_charset)
        bianma = result_charset['encoding']
        if bianma == 'utf-8' or bianma == 'UTF-8':
            html_xf_gzip = html_xf_gzip
        else:
            html_xf_gzip = html_xf_gzip.decode('gb2312', 'ignore')
        # print(html_xf_gzip)

        # http://jiangwanchenghy.fang.com/house/3229072754/housedetail.htm
        # <a href="http://zdgjsq.fang.com/house/3229086052/housedetail.htm" id="xfptxq_B03_08"  target="_self">楼盘详情</a>
        # <a href="(.*?)" id="xfxq_.*?"  target="_self">楼盘详情</a>
        url_xf_housedetail = re.findall(r'<a href="(.*?)" id=".*?"  target="_self">楼盘详情</a>', html_xf_gzip)[0]
        print ("楼盘详情链接：%s" %url_xf_housedetail)

        req_xf_housedetail = urllib.request.Request(url_xf_housedetail, headers=headers_fang)
        html_xf_housedetail = urllib.request.urlopen(req_xf_housedetail)
        html_xf_housedetail = html_xf_housedetail.read()
        # html_xf_housedetail = html_xf_housedetail.decode('utf-8', 'ignore')
        # 数据存在乱码，又被压缩了。
        # print(html_xf)

        html_xf_housedetail_gzip = gzip.decompress(html_xf_housedetail)
        # print(result)
        result_charset_housedetail = chardet.detect(html_xf_housedetail_gzip)
        # print(result_charset_housedetail)
        bianma_housedetail = result_charset_housedetail['encoding']
        if bianma_housedetail == 'utf-8' or bianma_housedetail == 'UTF-8':
            html_xf_housedetail_gzip = html_xf_housedetail_gzip
        else:
            html_xf_housedetail_gzip = html_xf_housedetail_gzip.decode('gb2312', 'ignore')
        # print(html_xf_housedetail_gzip)

        xiangmu = []
        data = []
        # <div class="loupanmingchengc mglr10"><h1><strong>(.*?)基本信息</strong></h1></div>
        loupanmingcheng = re.findall(r'<div class="loupanmingchengc mglr10"><h1><strong>(.*?)基本信息</strong></h1></div>', html_xf_housedetail_gzip)[0]
        print ("楼盘名称：%s" %loupanmingcheng)
        xiangmu.append('loupanmingcheng')
        data.append(loupanmingcheng)

        # 区域
        # <a target="_blank" href="http://newhouse.dazhou.fang.com/house/s/.*?/" title=".*?">(.*?)楼盘</a>
        quyu = re.findall(r'<a target="_blank" href="http://newhouse.dazhou.fang.com/house/s/.*?/" title=".*?">(.*?)楼盘</a>', html_xf_housedetail_gzip)[0]
        print ("楼盘区域：%s" %quyu)
        xiangmu.append('quyu')
        data.append(quyu)

        # 均价
        junjia = re.findall(r' <span class="currentPrice fontStyle_sp">均价<strong class="fontStyle_sp">(.*?)</strong>元/平方米 </span>', html_xf_housedetail_gzip, re.M|re.I|re.S)[0:]
        print ("楼盘均价：%s" %junjia)
        if len(junjia) == 0:
            junjia = ['']
            junjia = junjia[0]
        else:
            junjia = junjia[0]
        # print ("总价：%s" %junjia)
        xiangmu.append('junjia')
        data.append(junjia)
        xiangmu.append('junjia')
        data.append(junjia)

        # 保存到数据库中去。把数据写入到数据中。
        conn=pymysql.connect(host='localhost', user='root', passwd='root', port=3306, charset="gb2312")
        cur=conn.cursor()                             #获取一个游标对象
        # 创建一个数据库来保存数据。
        # cur.execute("CREATE DATABASE fang")         # 执行对应的SQL语句, 创建数据库。
        cur.execute("USE fang")                        # 使用数据库
        # 创建可以存中文的表, 存放达房网上新房的 数据。创建表结束后，要忽略创建。
        # ENGINE=MyISAM DEFAULT CHARSET=gbk CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;
        # cur.execute("CREATE TABLE fang_xf(loupan varchar(256), quyu varchar(256), junjia varchar(256))ENGINE=MyISAM DEFAULT CHARSET=gbk CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;")
        # 把获得的数据插入到数据库中。
        cur.execute("insert into fang_xf(loupan, quyu, junjia) values(%s, %s, %s)", (loupanmingcheng, quyu, junjia))
        cur.close()                                    #关闭游标
        conn.commit()                                 #向数据库中提交任何未解决的事务, 对不支持事务的数据库不进行任何操作
        conn.close()                                    #关闭到数据库的连接, 释放数据库资源
        # 在爬取完一个项目之后，暂停一段时间。
        time.sleep(0.5)
        end_time = time.time()  # 记录程序结束时间
        total_time = end_time - start_time  # 计算程序执行耗时
        print ("耗时：{0:.5f}秒" .format(total_time))  # 格式输出耗时

# 脚本日志 #
# 测试了搜房网，不需要cookie就直接登陆了，
# 测试http://newhouse.dazhou.fang.com/house/web/Search_Result.php