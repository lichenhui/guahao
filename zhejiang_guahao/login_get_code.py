#!/usr/bin/env python
#coding=utf8
#
#登陆时，此文件用来获取官网验证码，并获取cookie并保存
#返回验证码图片字节流并另存为图片
import pycurl
import StringIO

# index_url = "http://www.bjguahao.gov.cn/comm/index.html"
def GetLoginCodeImg(cookie_file,code_img,proxy):
	index_url = "http://www.zj12580.cn/authCode.svl?type=captcha"
	#cookie_file = cookie_file

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
	ch.setopt(ch.URL, index_url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	#ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	fo = open(code_img, 'w')
	fo.write(html)
	fo.close()
	buffer_con.close()
	ch.close()
	return code_img
#####################################
#----------本文件主函数
#获得登陆时的验证码图片，并返回验证码名称
def GetLoginCode(cookie_file,code_img,proxy):
	code_img = GetLoginCodeImg(cookie_file,code_img,proxy)
	return code_img

if __name__ == '__main__':
	return_data = 	GetLoginCode('cookie.txt','login_code_img.gif',False)
	print return_data
