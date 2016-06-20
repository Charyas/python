#coding=utf-8
#
# import requests
# from bs4 import BeautifulSoup

# # get the control news from github option
# url = 'https://github.com/Charyas/python/blob/master/urlcontrol'

# r = requests.get(url)

# text = r.text

# soup = BeautifulSoup(text)

# for tag in soup.find_all("td", class_="blob-code blob-code-inner js-file-line"):
# 	print (tag.contents)

# # send back to email

import smtplib

from email.mime.text import MIMEText
_user = "3153319826@qq.com"
_pwd  = "Tbihia1234!@#$"
_to   = "358155255@qq.com"

msg = MIMEText("您有一个包裹")
msg["Subject"] = "don't panic"
msg["From"] = _user
msg["To"] = _to

s = smtplib.SMTP("smtp.qq.com", 465)
s.ehlo()
s.starttls()
s.ehlo()
s.login(_user, _pwd)
s.sendmail(_user, _to, msg)
s.close()