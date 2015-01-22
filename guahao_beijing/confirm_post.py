#!/usr/bin/env python
#coding=utf8
#
#选择挂号医生后确认信息，并填写相关报销事宜
import pycurl
import StringIO
from urllib import urlencode
import confirm
import gzip
import re
from BeautifulSoup import BeautifulSoup
#提交confirm数据,返回html
def spider(spider_url,cookie_file,post_data,referer_url,proxy):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()
	header = [
		"Host: www.bjguahao.gov.cn",
		"Connection: keep-alive",
		"Cache-Control:no-cache",
		"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		#"Accept-Encoding: gzip,deflate,sdch",
		"Referer: "+referer_url,
		"Content-Type: application/x-www-form-urlencoded",
		"Accept-Language: zh-CN,zh;q=0.8",
		"Origin: http://www.bjguahao.gov.cn",
		"Pragma:no-cache",
		"Expect: "
	]

	#将ｐｏｓｔ信息编码
	post_data = urlencode(post_data)
	ch.setopt(ch.URL, spider_url)
#	ch.setopt(ch.VERBOSE, 1)		#查看http信息
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
	html = unicode(html,'gbk').encode('utf8')
	print html
	return html
#confirm_post提交函数，调用spider提交数据
def confirm_post(cookie_file,referer_url,data,hidden_data,proxy):
	post_data = hidden_data
	post_data["jiuz"] = data['jiuzhenka'] 
	post_data["ybkh"] = data['yibaoka'] 
	post_data["baoxiao"] = data['baoxiao']
	post_data["dxcode"] = data['sms_code'] 
	match_obj = re.search( r'(http.*)guahao\.php', referer_url, re.M|re.I)
	spider_url = match_obj.group(1)+'ghdown.php'
	html = 	spider(spider_url,cookie_file,post_data,referer_url,proxy)
	dic = {}
	dic['html'] = html
	dic['spider_url'] = spider_url
	return dic
#若confirm数据提交成功，则挂号成功，并且会跳转到http://www.bjguahao.gov.cn/comm/show_cont.php页面，此页面包含挂号的具体信息
def spider_result(spider_url,referer_url,proxy):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()
	header = [
		"Host: www.bjguahao.gov.cn",
		"Connection: keep-alive",
		"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Referer: "+referer_url,
		"Accept-Language: zh-CN,zh;q=0.8",
	]

	ch.setopt(ch.URL, spider_url)
	#ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
#	ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html

#此函数用来抓取http://www.bjguahao.gov.cn/comm/show_cont.php页面并提取有用信息	
def confirm_success(referer_url,proxy):
	spider_url = 'http://www.bjguahao.gov.cn/comm/show_cont.php'	
	result_html = spider_result(spider_url,referer_url,proxy)
	soup_2 = BeautifulSoup(result_html)
	res_text = soup_2.find('div',{'class':'guahao'}).text.encode('utf8')
	return res_text
#data---->字典类型键分别为：jiuzhenka:就诊卡号；yibaoka:医保卡号;baoxiao:报销类型;sms_code:短信验证码
def this_main(cookie_file,referer_url,data,hidden_data,proxy):
	confirm_post_res = confirm_post(cookie_file,referer_url,data,hidden_data,proxy)	
	soup = BeautifulSoup(confirm_post_res['html'])
	if soup.find('script'):
		#跳转到show_cont页面，并提取信息
		guahao_info_res = confirm_success(confirm_post_res['spider_url'],proxy)
		match_obj = re.match( r'.*(\d{8}).*', guahao_info_res, re.M|re.I)
		dic = {}
		dic['tag'] = True
		cdkey = match_obj.group(1)
		dic['cdkey'] = cdkey
		return dic
		
	else:
		guahao_info_res = confirm_post_res['html']
		return guahao_info_res

if __name__ == '__main__':
	cookie_file = 'cookie.txt'
        referer_url = "http://www.bjguahao.gov.cn/comm/anzhen/guahao.php?hpid=108&ksid=%B8%DF%D1%AA%D1%B9%BF%C6&datid=305816"
	hidden_data ={'zxGcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhly9430286981': '943250', 'GcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhl6981': '922169', 'datid': '305816', 'tnndetqjMeNUTVSQrDyncFdiRysSDHUIRitVGzQyENefP6981': '943131', 'tpost': 'd01e4272ff69fc454744b5093e080037', 'tqjMeNUTVSQrDyncFdiRysSDHUIRitVGzQyENefP6981': '943131', 'GcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhly9430286981': '943250', 'edcrfvMiGKDnOYhZlZovSSpJbUlHPtKzRWLbHJnhOEYlgHUgrGwuLCTlutQoolOGBJJHKGcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhl9430286981': '943250', 'mscGcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhl6981': '943131', 'djweui34t6GcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhl6981': '943131', 'hpid': '108', 'wsxGcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhly9430286981': '943250', 'tygf6584MiGKDnOYhZlZovSSpJbUlHPtKzRWLbHJnhOEYlgHUgrGwuLCTlutQoolOGBJJHK6981': '922169', 'MiGKDnOYhZlZovSSpJbUlHPtKzRWLbHJnhOEYlgHUgrGwuLCTlutQoolOGBJJHK6981': '922169', 'ksid': '\xb8\xdf\xd1\xaa\xd1\xb9\xbf\xc6', 'MiGKDnOYhZlZovSSpJbUlHPtKzRWLbHJnhOEYlgHUgrGwuLCTlutQoolOGBJJHKGcCGMWlhkoTFxhOsvRhtKjcDQKvFnIqCXSSvFGmKZHRdmayenhl6981': '950212'}
	data = {}
	data["jiuzhenka"] = '' 
	data["yibaoka"] = '' 
	data["baoxiao"] = '0'
	data["sms_code"] = '7683' 
	proxy = False
	guahao_info = this_main(cookie_file,referer_url,data,hidden_data,proxy)
	print guahao_info
