#coding=utf-8
#
import requests

url = 'http://nw-restriction.nttdocomo.co.jp/gifcat/call.php'

headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
	'Connection':'keep-alive',
	'Cookie':'PHPSESSID=3f0f19faa8b6804e3d1ca9bbbaa1653c',
	'Host':'nw-restriction.nttdocomo.co.jp',
	'Referer':'http://nw-restriction.nttdocomo.co.jp/search.php',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
}

r = requests.get(url, headers=headers)

#length = r.content
#print(r.headers['content-length'])
with open("aaa.gif", "wb") as f:
	for chunk in r.iter_content(chunk_size=1024):
		f.write(chunk)

from PIL import Image
def processImage( infile ):
    try:
        im = Image.open( infile )
    except IOError:
        sys.exit(1)

    i = 0
    size        = im.size
    lastframe   = im.convert('RGBA')
    mypalette   = im.getpalette()

    try:
        while 1:

            im2 = im.copy()
            im2.putpalette( mypalette )

            background = Image.new("RGB", size, (255,255,255))

            background.paste( lastframe )
            background.paste( im2 )
            background.save('foo'+str(i)+'.png', 'PNG', quality=100)

            lastframe = background

            i += 1
            im.seek( im.tell() + 1 )

    except EOFError:
        pass # end of sequence


processImage("aaa.gif")