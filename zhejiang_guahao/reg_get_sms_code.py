#!/usr/bin/env python
#coding=utf8
#注册时获取短信验证码
#
import pycurl
import  time
import StringIO
from urllib import urlencode

def spider(post_data,cookie_file,proxy):
#	url = "http://www.zj12580.cn/patient/reg1_1"
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
	url = "http://www.zj12580.cn/msg/sendCode?"+post_data
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
#############################################################3
#-----------本文件主函数，注册时获取短信验证码
#传参：mobilePhone：string---手机号码
#	id_card_num:string---身份证号
#	cookie_file:cookie文件
#	proxy:代理服务器	
#返回：成功则为字符串：验证码已发送,有效期10分钟!
#      失败则为：
#def reg_check(mobilePhone,id_card_num,randow,cookie_file,proxy):
def reg_check(mobilePhone,id_card_num,cookie_file,proxy):
	post_data = {}
	post_data['mobilePhone'] =mobilePhone
	post_data['patientCard'] = id_card_num
	#post_data['randow'] =randow
	res_con = spider(post_data,cookie_file,proxy)
	return res_con
if __name__ == '__main__':
	mobilePhone = '13141367238'
	id_card_num = '430725199203205521'
#	randow = time.strftime('%a %b %d %Y %H:%M:%S GMT 0800(CST)',time.localtime())
	cookie_file = 'cookie.txt'
	proxy = False
#	res = reg_check(mobilePhone,id_card_num,randow,cookie_file,proxy)
	res = reg_check(mobilePhone,id_card_num,cookie_file,proxy)
	print res
