#!/usr/bin/env python
#coding=utf8
#负责模拟登陆
#
import pycurl
import StringIO
from urllib import urlencode
import get_login_code

def GetLoginInfo(post_data,cookie_file,proxy):
	login_url = "http://www.bjguahao.gov.cn/comm/logon.php"
	#cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept: */*", 
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"X-Requested-With:XMLHttpRequest",
		"Referer:http://www.bjguahao.gov.cn/comm/index.html",
		"Origin:http://www.bjguahao.gov.cn",
	]
#	post_data = {
#		"truename":"李晨辉",
#		"sfzhm":"142726199305301214",
#		"yzm":"4811"
#	}
	post_data = urlencode(post_data)
	ch.setopt(ch.URL, login_url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	#ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html

def Login(truename,id_card_num,cookie_file,code_img,proxy):
	post_data = {}
	post_data['truename'] = truename
	post_data['sfzhm'] = id_card_num
	post_data['yzm'] = get_login_code.GetLoginCode(cookie_file,code_img,proxy)
	login_info = GetLoginInfo(post_data,cookie_file,proxy)	
	login_info = unicode(login_info,"gbk").encode('utf8')
	return  login_info
if __name__ == '__main__':
	#login_info = Login('张佳','640321199001020977','cookie.txt','login_code_img.gif','http://125.46.100.198:9999')
	login_info = Login('李晨辉','142726199305301214','cookie.txt','login_code_img.gif',False)
	fo = open('login_response.txt', 'w')
	fo.write(login_info)
	fo.close()
	print login_info

