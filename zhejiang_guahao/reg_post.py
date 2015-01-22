#!/usr/bin/env python
#coding=utf8
#注册提交信息
#
import pycurl
import StringIO
from urllib import urlencode

def spider(post_data,cookie_file,proxy):
	url = "http://www.zj12580.cn/patient/reg2"
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
############################################
#----------本文件主函数
#传参：data:字典类型－－注册提交的数据,patientMobile手机号，password－＞密码patientName－＞姓名；gender－＞性别；sms_code－＞短信验证码
#	cookie_file:cookie文件
#	proxy:代理服务器
#返回：成功返回：success
#	失败返回：不太清楚
def reg_post(data,cookie_file,proxy):
	post_data = {}
	post_data['patientMobile'] =data['patientMobile'] 	#手机号
	post_data['password'] =data['password'] 		#密码
	post_data['password2'] =data['password'] 		#重复密码
	post_data['patientName'] =data['patientName'] 		#真实姓名
	post_data['patientCard'] =data['patientCard'] 		#身份证号
	post_data['txtsex'] =data['gender'] 		#性别
	post_data['patientMediCardType'] =""		#空着就行
	post_data['code'] = data['sms_code']				#短信验证码
	res_con = spider(post_data,cookie_file,proxy)
	return res_con
if __name__ == '__main__':
	data = {}
	data['patientMobile'] = '13141367238'
	data['password'] = '12345678'
	data['patientName'] = '袁静'
	data['patientCard'] = '430725199203205521'
	data['gender'] = 'on'
	data['sms_code'] = '801814'
	cookie_file = 'cookie.txt'
	proxy = False
	res = reg_post(data,cookie_file,proxy)
	fo = open('reg_return.html','w')
	fo.write(res)
	fo.close()
	print res
