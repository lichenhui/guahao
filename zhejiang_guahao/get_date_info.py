#!/usr/bin/env python
#coding=utf8
#获取７天内是否可挂号情况
#
import pycurl
import StringIO
from urllib import urlencode
from BeautifulSoup import BeautifulSoup

def spider(url,cookie_file,proxy):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"application/x-www-form-urlencoded", 
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
	buffer_con.close()
	ch.close()
	return html
#####################################################################
#--------------本文件主函数
#传参：out_offi_id：官网门诊id
#      cookie_file:cookie文件
#      proxy:代理服务器
#return:info_dic:字典类型
#           |
#	   {'date_info',        'detail'}
#	        |                   |
#		字典　　         　字典
#	键：{0,1,2,3,4,5,6}  键：{0,1,2,3,4,5,6}
#	                          |
#				 列表[one_data,one_data,one_data]
#				         |
#				      某一天的某一个医生信息，字典类型
#				         |
#					{time,doc_name,doc_level,text,input}
#					                                |
#									字典,传给下一个爬虫
def get_date_info(out_offi_id,cookie_file,proxy):
	url = 'http://www.zj12580.cn/dept/'+`out_offi_id`
	html = spider(url,cookie_file,proxy)
	soup = BeautifulSoup(html)
	tr = soup.find('div',{'class':'right_box_1_r'}).findAll('tr')
	info_dic = {}
	date_info = {0:0,1:0,2:0,3:0,4:0,5:0,6:0}		#后７天是否可挂号情况，０＝否１＝可
	detail = {}						#7天的挂号详细信息
	detail[0] = []
	detail[1] = []
	detail[2] = []
	detail[3] = []
	detail[4] = []
	detail[5] = []
	detail[6] = []
	day = 0
	for x in xrange(2,len(tr)):				#遍历每一行
		td = tr[x].findAll('td')
		try:
			doc_name = td[0].find('a').text.encode('utf8')			#如果能找见这个元素，则医生有名称，职称
			doc_level = td[0].findAll('p')[1].text.encode('utf8')
		#	print doc_name,doc_level
		except:							#如果找不见，说明是普通医生
			doc_name = td[0].text.encode('utf8')
			doc_level = td[0].text.encode('utf8')
		#	print doc_name,doc_level
		for y in xrange(1,len(td)):			#遍历每一行的单元格
			if td[y].find('form'):			#如果此单元格内能找见form元素，说明有可能可以预约
				if td[y].find('form').find('input',{'type':'submit'}):			#如果此单元格内form内可提交，说明的确可以预约，否则可能为约满或者未放号
					one_data = {}
					form_con = td[y].find('form')
					if y % 2 == 1:		#根据单元格位置求出时间时上午还是下午
						one_data['time'] = 'am'
						day = y/2
					else:
						one_data['time'] = 'pm'
						day = y/2-1
					date_info[day] = 1
					one_data['doc_name'] = doc_name		#某一天的某一格医生
					one_data['doc_lavel'] = doc_level
					one_data['text'] = form_con.find('input',{'type':'submit'})['value'].encode('utf8')	#此单元格内的文字
					#print one_data['text']
					hidden_input = form_con.findAll('input',{'type':'hidden'})	#此单元格内的隐藏表单
					one_data['input'] = {}
					for z in hidden_input:
						key = z['name'].encode('utf8')
						value = z['value'].encode('utf8')
						one_data['input'][key] = value
					detail[day].append(one_data)
					#print day
					
	info_dic['date_info'] = date_info
	info_dic['detail'] = detail
	return info_dic
if __name__ == '__main__':
	#url = 'http://www.zj12580.cn/dept/113'
	out_offi_id = 113
	cookie_file = 'cookie.txt'
	proxy = False
	info_dic = get_date_info(out_offi_id,cookie_file,proxy)
	print info_dic
