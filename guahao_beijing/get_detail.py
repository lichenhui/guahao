#!/usr/bin/env python
#coding=utf8
#
#抓取并解析挂号医生列表
import pycurl
import StringIO
from BeautifulSoup import BeautifulSoup
# from urllib import urlencode

def spider(spider_url,cookie_file,referer_url,proxy):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		# "Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
		#"Accept-Encoding:gzip,deflate,sdch",
		# "Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"Referer:"+referer_url,
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, spider_url)
	#ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	# ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	#ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	# print html
	buffer_con.close()
	ch.close()
	return html
def html_parse(html):
#开始html页面解析　
	soup = BeautifulSoup(html)
	content = soup.findAll('table')[1]
	# print content
	response = []
	tr_list = content.findAll('tr')
	# print tr_list
	for x in xrange(2,len(tr_list)+1):
		# print tr_list[x]
		td_list = tr_list[(x-1)].findAll('td')
		one = []
		for y in range(len(td_list)):
			order_url = td_list[y].find('a')
			# print order_url
			one.append(td_list[y].text.encode('UTF-8'))
			if order_url:
				order_url = "http://www.bjguahao.gov.cn/comm"+order_url['href'][1:].encode('UTF-8')
				one.append(order_url)
		response.append(one)	
	return response
def get_detail(spider_url,cookie_file,referer_url,proxy):
	html =  spider(spider_url,cookie_file,referer_url,proxy)
	return_list = html_parse(html)
	return return_list
if __name__ == '__main__':
	spider_url = "http://www.bjguahao.gov.cn/comm/ghao.php?hpid=108&keid=%B8%DF%D1%AA%D1%B9%BF%C6&date1=2014-07-31"
	cookie_file = 'cookie.txt'
	referer_url = 'http://www.bjguahao.gov.cn/comm/content.php?hpid=108&keid=%B8%DF%D1%AA%D1%B9%BF%C6'
	proxy = 'http://125.46.100.198:9999'
	detail = get_detail(spider_url,cookie_file,referer_url,proxy)
	print detail
