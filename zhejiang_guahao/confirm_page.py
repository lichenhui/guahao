#!/usr/bin/env python
#coding=utf8
#此爬虫用不上，可以删除
#挂号选择完所有信息后进入信息确认页面，此爬虫获取确认页面
#
import pycurl
import StringIO
from urllib import urlencode
from BeautifulSoup import BeautifulSoup

def spider(post_data,cookie_file,proxy):
	url = "http://www.zj12580.cn/order/check"
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

def confirm_page(hidden_data,detail_data,cookie_file,proxy):
	post_data = {}
	post_data.update(hidden_data)
	post_data.update(detail_data)
	print post_data
	res = spider(post_data,cookie_file,proxy)
	return res
if __name__ == '__main__':
	hidden_data = {'hosId': '957103', 'deptId': '754', 'hosName': '\xe6\xb5\x99\xe6\xb1\x9f\xe5\xa4\xa7\xe5\xad\xa6\xe5\x8c\xbb\xe5\xad\xa6\xe9\x99\xa2\xe9\x99\x84\xe5\xb1\x9e\xe7\xac\xac\xe4\xb8\x80\xe5\x8c\xbb\xe9\x99\xa2', 'takeNumAddr': '', 'resTimeSign': '0', 'docTitle': '', 'regFee': '2', 'schemeId': '3801152', 'docName': '\xe6\x99\xae\xe9\x80\x9a', 'docId': '', 'deptName': '\xe9\xab\x98\xe8\xa1\x80\xe5\x8e\x8b\xe4\xb8\x93\xe7\xa7\x91', 'orderDate': '2014.08.14'}
	detail_data ={'resNumber': 80, 'numId': '53918171', 'resTime': '09:49'} 
	cookie_file = 'cookie.txt'
	proxy = False
	res = confirm_page(hidden_data,detail_data,cookie_file,proxy)
	fo = open('confirm_page.html','w')
	fo.write(res)
	fo.close()






