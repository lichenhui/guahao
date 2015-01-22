#!/usr/bin/env python
#coding=utf8
#提交挂号预约码，并且解析页面，返回取消的url
#
import pycurl
import StringIO
from urllib import urlencode
from BeautifulSoup import BeautifulSoup

def spider_cancel(post_data,offi_hos_id,cookie_file,proxy):
	spider_url = "http://www.bjguahao.gov.cn/comm/yycx_end.php?hpid="+`offi_hos_id`
	#cookie_file = './Cookie/cookie.txt'

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded;", 
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		"X-Requested-With:XMLHttpRequest",
		"Referer:http://www.bjguahao.gov.cn/comm/yycx.php?hpid="+`offi_hos_id`,
		"Origin:http://www.bjguahao.gov.cn",
	]
	post_data = urlencode(post_data)
	ch.setopt(ch.URL, spider_url)
	#ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy: ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html

def confirm_cancel(url_part,offi_hos_id,cookie_file,proxy):
	spider_url = "http://www.bjguahao.gov.cn/comm/"+url_part

	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded;", 
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
		#"X-Requested-With:XMLHttpRequest",
		"Referer:http://www.bjguahao.gov.cn/comm/yycx.php?hpid="+`offi_hos_id`,
		"Origin:http://www.bjguahao.gov.cn",
	]
	ch.setopt(ch.URL, spider_url)
	#ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy: ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html

def this_main(iden_code,offi_hos_id,cookie_file,proxy):
	post_data = {}
	post_data['yysbm'] = iden_code
	html = spider_cancel(post_data,offi_hos_id,cookie_file,proxy)	#抓取挂号记录列表页面
	fo = open('html_1.html','w')
	fo.write(html)
	fo.close()
	soup = BeautifulSoup(html)
	div_content = soup.find('div',{'class':'tj_content'})
	tr_con = div_content.findAll('tr')[1]
	td = tr_con.findAll('td')
	if len(td) == 1 :
		tr_text = tr_con.text.encode('utf8')
		return 0		#无挂号记录
	else:
		cancel_url = td[len(td)-1].find('a')['href'].encode('utf8')	#获取取消挂号的链接
		result_html = confirm_cancel(cancel_url,offi_hos_id,cookie_file,proxy)	#取消挂号	
		fo = open('html_2.html','w')
		fo.write(result_html)
		fo.close()
		soup = BeautifulSoup(result_html)
		div_content = soup.find('div',{'class':'tj_content'})
		tr_con = div_content.findAll('tr')[0]
		td = tr_con.findAll('td')
		if len(td) == 1:
			return 1
		else:
			return 2
	
if __name__ == '__main__':
	offi_hos_id = 226
	cookie_file = 'cookie.txt'
	proxy = False
	iden_code = '14981925'
	result = this_main(iden_code,offi_hos_id,cookie_file,proxy)
	print result
