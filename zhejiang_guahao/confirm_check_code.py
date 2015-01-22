#!/usr/bin/env python
#coding=utf8
#确认页面检查验证码正确性
#
import pycurl
import StringIO
from urllib import urlencode
#from BeautifulSoup import BeautifulSoup
########################################################
#------------主函数
#传参：参见main测试函数
def spider(post_data,cookie_file,proxy):
	post_data = urlencode(post_data)
	url = "http://www.zj12580.cn/order/capchk?"+post_data
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"application/x-www-form-urlencoded", 
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
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
	hidden_data = {'hosId': '957103', 'deptId': '754', 'hosName': '\xe6\xb5\x99\xe6\xb1\x9f\xe5\xa4\xa7\xe5\xad\xa6\xe5\x8c\xbb\xe5\xad\xa6\xe9\x99\xa2\xe9\x99\x84\xe5\xb1\x9e\xe7\xac\xac\xe4\xb8\x80\xe5\x8c\xbb\xe9\x99\xa2', 'takeNumAddr': '', 'resTimeSign': '0', 'docTitle': '', 'regFee': '2', 'schemeId': '3845133', 'docName': '\xe6\x99\xae\xe9\x80\x9a', 'docId': '', 'deptName': '\xe9\xab\x98\xe8\xa1\x80\xe5\x8e\x8b\xe4\xb8\x93\xe7\xa7\x91', 'orderDate': '2014.08.25'}
	detail_data = {'resNumber': 79, 'numId': '54642895', 'resTime': '09:48'}
	confirm_code = 'mtuu3'
	cookie_file = 'cookie.txt'
	proxy = False
	data = {}
	data['hospitalId'] = hidden_data['hosId']
	data['numId'] = detail_data['numId']
	data['cap'] = confirm_code
	res = spider(data,cookie_file,proxy)
	print res
