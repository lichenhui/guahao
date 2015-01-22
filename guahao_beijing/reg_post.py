#!/usr/bin/env python
#coding=utf-8
#负责注册,所有注册信息填写完整后，ｐｏｓｔ请求提交的ｕｒｌ
#
import pycurl
import StringIO
from urllib import urlencode
import urllib
from BeautifulSoup import BeautifulSoup
import reg_get_sms_code

def reg_post_spider(url,post_data,cookie_file,referer_url,proxy):
	#url = "http://www.bjguahao.gov.cn/comm/reg1.php"
	#cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded;", 
		"Accept: */*", 
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"X-Requested-With:XMLHttpRequest",
		"Referer:"+referer_url,
		"Origin:http://www.bjguahao.gov.cn",
	]
	post_data = urlencode(post_data)
	#print post_data
	ch.setopt(ch.URL, url)
	#ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy: ch.setopt(ch.PROXY, proxy)      #设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html
def reg_confirm(cookie_file,data,proxy):
	truenamereg = unicode(data['truename'],'utf8').encode('gbk')
	sex= unicode(data['gender'],'utf8').encode('gbk')
	post_data = {
		"truenamereg":truenamereg,
		"sex":sex,
		"cardtype":1,
		"sfzhmreg":data['idcard_num'],
		"qrsfzhm":data['idcard_num'],
		"province":unicode("北京市",'utf8').encode('gbk'),
		"yzmreg":data['code'],
		"flagmib":"mibok",
		"reg_mib":data['phone_num'],
		"mib":data['phone_num'],
		"reg_dxcode":data['sms_code'],
		"dxcode":data['sms_code'],
		"box":1
	}
	reg_confirm_url = "http://www.bjguahao.gov.cn/comm/reg1.php"
	referer_url = 'http://www.bjguahao.gov.cn/comm/index.html'
	html = reg_post_spider(reg_confirm_url,post_data,cookie_file,referer_url,proxy)
	return html
def reg_post(cookie_file,data,proxy):
	truenamereg = unicode(data['truename'],'utf8').encode('gbk')
	sex= unicode(data['gender'],'utf8').encode('gbk')
	reg_confirm_html = reg_confirm(cookie_file,data,proxy)
	soup = BeautifulSoup(reg_confirm_html)
	action_flag = soup.find('input',{'name':'action_flag'})['value'].encode('gbk')
	post_data = {
		"action_flag":action_flag,
		"truenamereg":truenamereg,
		"sex":sex,
		"cardtype":1,
		"sfzhmreg":data['idcard_num'],
		"province":unicode("北京市",'utf8').encode('gbk'),
		"yzmreg":data['code'],
		"mib":data['phone_num'],
		"dxcode":data['sms_code'],
	}
	reg_post_url = "http://www.bjguahao.gov.cn/comm/register.php"
	referer_url = 'http://www.bjguahao.gov.cn/comm/reg1.php'
	html = reg_post_spider(reg_post_url,post_data,cookie_file,referer_url,proxy)
	#fo = open('reg_post_rs..html','w')
	#fo.write(html)
	#fo.close()
	soup_2 = BeautifulSoup(html)
	try:
		result = soup_2.find('div',{'class':'logtxtwtr'}).find('h1').text.encode('utf8')
	except:
		result = soup_2.find('div',{'class':'erroralltxt'}).text.encode('utf8')
	return result
	
if __name__ == '__main__':
	data = {
		'truename':'张佳',
		'gender':'男',
		'idcard_num':'640321199001020977',
		'code':'9692',
		'phone_num':'15210860284',
		'sms_code':'2526'
	}
	html = reg_post('cookie.txt',data,False)
	print html
#	html = unicode(html,'gbk').encode('utf8')
	fo = open('reg_response.html', 'w')
	fo.write(html)
	fo.close()
