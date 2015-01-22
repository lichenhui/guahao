#!/usr/bin/env python
#coding=utf8
#提交取消挂号请求
#
import pycurl
import StringIO
from urllib import urlencode
#from BeautifulSoup import BeautifulSoup

def spider(post_data,cookie_file,proxy):
	url = "http://www.zj12580.cn/order/cancel"
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"application/x-www-form-urlencoded", 
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	post_data = urlencode(post_data)
	ch.setopt(ch.URL, url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html

if __name__ == '__main__':
	data = {}
	data['orderId'] = '217823468'	#订单号
	data['hosId'] = '957103'	#医院id
	data['takeCode'] = '51015865'	#识别码
	data['code'] = 'dd3x'	#图片验证码
	cookie_file = 'cookie.txt'
	proxy = False
	res = spider(data,cookie_file,proxy)
	print res





