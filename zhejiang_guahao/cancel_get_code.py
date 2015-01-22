#!/usr/bin/env python
#coding=utf8
#
#取消挂号页面，此文件用来获取图片验证码
#返回验证码图片字节流并另存为图片
import pycurl
import StringIO
from urllib import urlencode

def spider(cookie_file,code_img,proxy):
	url = "http://www.zj12580.cn/captcha.svl"

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		# "Content-type: text/xml;charset=\"utf-8\"", 
		    "Accept: image/webp,*/*;q=0.8", 
		    "Cache-Control:max-age=0", 
		    # "Accept-Encoding:gzip,deflate,sdch",
		    "Connection:keep-alive",
		    "User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	fo = open(code_img, 'w')
	fo.write(html)
	fo.close()
	buffer_con.close()
	ch.close()
	return code_img

if __name__ == '__main__':
	return_data = 	spider('cookie.txt','cancel_code_img.gif',False)
	print return_data


