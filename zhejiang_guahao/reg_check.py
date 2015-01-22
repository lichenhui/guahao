#!/usr/bin/env python
#coding=utf8
#注册第一步，检查身份证是否已经被注册
#注册时先检查身份证号是否已经被注册
#
import pycurl
import StringIO
from urllib import urlencode

###################################
######爬虫，返回json数据
def spider(post_data,cookie_file,proxy):
	url = "http://www.zj12580.cn/patient/reg1_1"
	#cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"application/x-www-form-urlencoded", 
		"Accept:application/json, text/javascript, */*; q=0.01", 
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"X-Requested-With:XMLHttpRequest",
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
###########################################################################
#------------本文件主函数
#传参：id_card_num:字符串,身份证号码
#	cookie_file:字符串，cookie文件名
#	proxy:代理服务器，若False则不用代理
#返回：json数据：若身份证已经被注册则返回类似：{"chk_cardId":"*晨辉","chk_phone":"188****9457","chk_zcly":"浙江在线"}
#	其他则为未被注册,返回类似：{"chk_cardId":""}
def reg_check(id_card_num,cookie_file,proxy):
	post_data = {}
	post_data['cardId'] =id_card_num 
	res_json = spider(post_data,cookie_file,proxy)
	return res_json
if __name__ == '__main__':
	id_card_num = '430725199203205521'
	cookie_file = 'cookie.txt'
	proxy = False
	res = reg_check(id_card_num,cookie_file,proxy)
	print res
