#!/usr/bin/env python
#coding=utf8
#提交登陆信息
#
import pycurl
import StringIO
from urllib import urlencode
from BeautifulSoup import BeautifulSoup

def spider(post_data,cookie_file,proxy):
	url = "http://www.zj12580.cn/login"
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
#########################################
#-----------本文件主函数
#传参：data:字典类型：idcard_num：身份证号
#	password:密码
#	img_code:图片验证码
#返回：成功返回True,失败返回False
def login_post(data,cookie_file,proxy):
	post_data = {}
	post_data['username'] =data['idcard_num']
	post_data['password'] =data['password']
	post_data['captcha'] = data['img_code']
	html = spider(post_data,cookie_file,proxy)	#获得登陆的反馈html代码，分析html代码判断是否登陆成功
	fo = open('login_res.html','w')
	fo.write(html)
	fo.close()
	soup = BeautifulSoup(html)
	result = 0
	welcome = soup.find('div',{'class':'login_next_box'})
	if welcome :
		result = True
	#	print welcome.text.encode('utf8')
	else:
		error_tip =soup.find('div',{'class':'right_box'}).find('span',{'class':'color1'})
		result = error_tip.text.encode('utf8')
	return result
if __name__ == '__main__':
	data = {}
	data['idcard_num'] = '142726199305301214'
	data['password'] = '12345678'
	data['img_code'] = '0211'
	cookie_file = 'cookie.txt'
	proxy = False
	res = login_post(data,cookie_file,proxy)
	print res




