#!/usr/bin/env python
#coding=utf8
#
#选择挂号医生后确认信息，并填写相关报销事宜
import pycurl
import StringIO
from BeautifulSoup import BeautifulSoup
# from urllib import urlencode
import re
import urllib

def spider(spider_url,cookie_file,referer_url,proxy):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		# "Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
		#"Accept-Encoding:gzip,deflate,sdch",
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"Referer:"+referer_url,
#		"Referer:http://www.bjguahao.gov.cn/comm/ghao.php?hpid=108&keid=%B8%DF%D1%AA%D1%B9%BF%C6&date1=2014-07-24",
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
	if proxy : ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	#fo = open('aaaaaaaaaaa.txt','a')
	#fo.write(html)
	#fo.close
	return html
def html_parse(html,spider_url):
	#开始html页面解析　
	soup = BeautifulSoup(html)
	hidden_input = soup.findAll('input',{'type':'hidden'})
	hidden_data = {}
	for x in range(len(hidden_input)):
		key = hidden_input[x]['name'].encode('gbk')
		value = hidden_input[x]['value'].encode('gbk')
		hidden_data[key] = value
	#form = soup.find('form',{'name':'ti'})
	#tpost = form.find('input',{'name':'tpost'})['value'].encode('utf-8')
	#hpid = form.find('input',{'name':'hpid'})['value'].encode('utf-8')
	#ksid = form.find('input',{'name':'ksid'})['value'].encode('utf-8')
	#datid = form.find('input',{'name':'datid'})['value'].encode('utf-8')
	return_dic = {}
	return_dic['hidden_data'] = hidden_data
	#return_dic['tpost'] = tpost
	#return_dic['hpid'] = hpid
	#return_dic['ksid'] = ksid
	#return_dic['datid'] = datid
	#用正则表达式得出ajax请求中一部分参数
	matchObj = re.search( r'shortmsg/dx_code\.php\?hpid=\"\+hpid\+\"\&(.*)\"\+\"\&ksid=\"\+ksid', html, re.M|re.I)
	url_part_1 = matchObj.group(1)
	# type(matchObj.group())
	match_obj = re.search(r'\.php\?(.*)',spider_url,re.M|re.I)
	url_part_2 = match_obj.group(1)
	url_part = url_part_1+url_part_2
	return_dic['url_part'] = url_part
	return return_dic
def get_confirm_page(spider_url,cookie_file,referer_url,proxy):
	html = 	spider(spider_url,cookie_file,referer_url,proxy)
	return_dic = html_parse(html,spider_url)
	return return_dic
	
if __name__ == '__main__':
	spider_url = "http://www.bjguahao.gov.cn/comm/anzhen/guahao.php?hpid=108&ksid=%B8%DF%D1%AA%D1%B9%BF%C6&datid=305816"
	cookie_file = 'cookie.txt'
	referer_url = "http://www.bjguahao.gov.cn/comm/ghao.php?hpid=108&keid=%B8%DF%D1%AA%D1%B9%BF%C6&date1=2014-07-31"
	html = 	spider(spider_url,cookie_file,referer_url,False)
	return_dic = html_parse(html,spider_url)
	print return_dic


