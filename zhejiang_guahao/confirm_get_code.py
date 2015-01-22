#!/usr/bin/env python
#coding=utf8
#
#挂号确认页面，此文件用来获取官网验证码，并获取cookie并保存
#返回验证码图片字节流并另存为图片
import pycurl
import StringIO
from urllib import urlencode

def GetConfirmCodeImg(data,cookie_file,code_img,proxy):
	data_url = urlencode(data)
	url = "http://www.zj12580.cn/regCaptcha.svl?"+data_url

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		# "Content-type: text/xml;charset=\"utf-8\"", 
		    "Accept: image/webp,*/*;q=0.8", 
		    "Cache-Control:max-age=0", 
		    # "Accept-Encoding:gzip,deflate,sdch",
		    "Connection:keep-alive",
		    "User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	fo = open(code_img, 'w')
	fo.write(html)
	fo.close()
	buffer_con.close()
	ch.close()
	return code_img
#######################################################################################3
#传参：hidden_data:get_date_info返回中包含
#　　　detail_data:get_detail爬虫返回中包含
#      cookie_file:cookie文件
#      confirm_code_name:图片验证码
#　　　proxy:代理服务器
#返回：成功：返回订单号
#　　　　失败：返回失败原因
def this_main(hidden_data,detail_data,cookie_file,confirm_code_name,proxy):
	data = {}
	data['hospitalId'] = hidden_data['hosId']
	data['numId'] = detail_data['numId']
	return_data = 	GetConfirmCodeImg(data,cookie_file,confirm_code_name,proxy)
	
if __name__ == '__main__':
	hidden_data = {'hosId': '957103', 'deptId': '754', 'hosName': '\xe6\xb5\x99\xe6\xb1\x9f\xe5\xa4\xa7\xe5\xad\xa6\xe5\x8c\xbb\xe5\xad\xa6\xe9\x99\xa2\xe9\x99\x84\xe5\xb1\x9e\xe7\xac\xac\xe4\xb8\x80\xe5\x8c\xbb\xe9\x99\xa2', 'takeNumAddr': '', 'resTimeSign': '0', 'docTitle': '', 'regFee': '2', 'schemeId': '3845133', 'docName': '\xe6\x99\xae\xe9\x80\x9a', 'docId': '', 'deptName': '\xe9\xab\x98\xe8\xa1\x80\xe5\x8e\x8b\xe4\xb8\x93\xe7\xa7\x91', 'orderDate': '2014.08.25'}
	detail_data = {'resNumber': 79, 'numId': '54642895', 'resTime': '09:48'}
	cookie_file = 'cookie.txt'
	confirm_code_name = 'confirm_code_img.gif'
	proxy = False
	data = {}		#需要参入的参数
	data['hospitalId'] = hidden_data['hosId']
	data['numId'] = detail_data['numId']
	return_data = 	GetConfirmCodeImg(data,cookie_file,confirm_code_name,proxy)
	print return_data

