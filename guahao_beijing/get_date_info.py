#!/usr/bin/env python
#coding=utf8
#
#负责抓取挂号信息页面
import pycurl
import StringIO
from BeautifulSoup import BeautifulSoup
import re
# from urllib import urlencode

def spider_date_info(url,year,month,cookie_file,referer_url,proxy):
	spider_url = url+'&haoscore=web&getyear='+year+'&getmonth='+month
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
		#"Accept-Encoding:gzip,deflate,sdch",
		"Cache-Control:max-age=0", 
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
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	#ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	if proxy: ch.setopt(ch.PROXY, proxy)	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	html = unicode(html,'gbk').encode('utf8')
	return html


#开始html页面解析　
def html_parse(html,month):
	soup = BeautifulSoup(html)
	content = soup.findAll('td' ,{"class":"detailtext"})
	next_url = soup.find('p',{'class':'nyr_down'}).find('a')['href']
#	content.php?hpid=108&keid=高血压科&haoscore=web&getyear=2014&getmonth=09
	match_obj = re.match(r'.*getmonth=(\d{1,2})',next_url)
	next_month = match_obj.group(1)
	dic = {}
	if next_month == month:
		dic['next_month'] = False
		print dic['next_month']
	else:
		dic['next_month'] = True
	for td in content:
		tag = td.contents[0].name
		if tag == 'b':
			if (str(td.contents[0].text) != ""):
				key = td.contents[0].text.encode("UTF-8")
				key = int(key)
				value = 0
				dic[key] = value
		elif tag == 'div':
			base = td.contents[0]
			key = base.find('p').text.encode("UTF-8")
			key = int(key)
			value = []
			status = base.find('span').text.encode("UTF-8")
			url = "http://www.bjguahao.gov.cn/"+base.find('a')['href'].encode('UTF-8')
			if status == "约满":
				status = 1
			elif status == "预约":
				status = 2
			value.append(status)  #base.find('a')['href'].encode('UTF-8')
			value.append(url)  #base.find('a')['href'].encode('UTF-8')
			# value[1] = base.find('span').text.encode("UTF-8")
			dic[key] = value
	return dic
#核心函数，文件主函数，获取html页面并解析
#返回：dic 字典类型  
def GetDateInfo(url,year,month,cookie_file,referer_url,proxy):
	html = spider_date_info(url,year,month,cookie_file,referer_url,proxy)
	dic = html_parse(html,month)
	return dic
if __name__ == '__main__':
	referer_url = "http://www.bjguahao.gov.cn/comm/yyks-108.html"
	year = '2014'
	month = '08'
	url = "http://www.bjguahao.gov.cn/comm/content.php?hpid=108&keid=%B8%DF%D1%AA%D1%B9%BF%C6"
	cookie_file = 'cookie.txt'
	proxy = False
	dic = GetDateInfo(url,year,month,cookie_file,referer_url,proxy)
	print dic

