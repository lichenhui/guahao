#!/usr/bin/env python
#coding=utf8
#获取某天详细挂号信息
#
import pycurl
import StringIO
from urllib import urlencode
from BeautifulSoup import BeautifulSoup

def spider(data,cookie_file,proxy):
	data = urlencode(data)
	url = "http://www.zj12580.cn/order/num?"+data
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, url)
	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
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
##############################################33
#---------本文件主函数
#传参：data:get_date_info.py返回中包含这个参数
#      cookie_file:cookie文件
#      proxy:代理服务器
#返回：字典数据：键为挂号的排号，值为每个号对应的值，也是字典类型，需传给后面的spider
def get_detail(data,cookie_file,proxy):
	html = spider(data,cookie_file,proxy)
	soup = BeautifulSoup(html)
	radio = soup.findAll('input',{'type':'radio','name':'num'})
	radio_value = {}
	for x in radio:
		value_dic = {}
		try:
			value = x['value'].encode('utf8')
		except:
			continue
		value_list = value.split(',')	#将以逗号分割的字符串拆分为列表
		value_dic['numId'] = value_list[0]	#将拆分得到的列表值给元组
		value_dic['resTime'] = value_list[1]
		value_dic['resNumber'] = int(value_list[2])
		radio_value[int(value_list[2])] = value_dic	#将一个元组添加到总元组
	return  radio_value
if __name__ == '__main__':
	data = {'hosId': '957103', 'deptId': '754', 'hosName': '\xe6\xb5\x99\xe6\xb1\x9f\xe5\xa4\xa7\xe5\xad\xa6\xe5\x8c\xbb\xe5\xad\xa6\xe9\x99\xa2\xe9\x99\x84\xe5\xb1\x9e\xe7\xac\xac\xe4\xb8\x80\xe5\x8c\xbb\xe9\x99\xa2', 'takeNumAddr': '', 'resTimeSign': '0', 'docTitle': '', 'regFee': '2', 'schemeId': '3845133', 'docName': '\xe6\x99\xae\xe9\x80\x9a', 'docId': '', 'deptName': '\xe9\xab\x98\xe8\xa1\x80\xe5\x8e\x8b\xe4\xb8\x93\xe7\xa7\x91', 'orderDate': '2014.08.25'}
	cookie_file = 'cookie.txt'
	proxy = False
	res = get_detail(data,cookie_file,proxy)
	print res
