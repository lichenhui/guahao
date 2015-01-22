#!/usr/bin/env python
#coding=utf8
#
#检测注册页面用户身份证输入是否合法
import pycurl
import StringIO
from BeautifulSoup import BeautifulSoup
# from urllib import urlencode
def check_id_card(idcard_num,cookie_file,proxy):
	spider_url = "http://www.bjguahao.gov.cn/comm/getajaxuser.php?sfzhm="+idcard_num
	#cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
		#"Accept-Encoding:gzip,deflate,sdch",
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"Referer:http://www.bjguahao.gov.cn/comm/reg.php",
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, spider_url)
#	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	# ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)      #设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html
if __name__ == '__main__':
	re = check_id_card('142726199305301217','cookie.txt')
	print re
