#!/usr/bin/env python
#coding=utf8
#
#此文件用来获取官网注册时的验证码，并获取cookie并保存(若已有cookie则用已有的)
#返回验证码，字符串
import pycurl
import StringIO

# index_url = "http://www.bjguahao.gov.cn/comm/index.html"
def get_reg_code(cookie_file,proxy):
	index_url = "http://www.bjguahao.gov.cn/comm/make_reg_code.php"
#	cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		# "Content-type: text/xml;charset=\"utf-8\"", 
		    "Accept: image/webp,*/*;q=0.8", 
		    "Cache-Control:max-age=0", 
		    # "Accept-Encoding:gzip,deflate,sdch",
		    "Connection:keep-alive",
		    "Host:www.bjguahao.gov.cn",
		    "Referer:http://www.bjguahao.gov.cn/comm/reg.php",
		    "User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, index_url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)      #设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html
if __name__ == '__main__':
	html = get_reg_code('cookie.txt')
	print html
