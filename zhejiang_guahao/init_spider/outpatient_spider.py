#!/usr/bin/env python
#coding=utf8
from BeautifulSoup import BeautifulSoup
from spider import spider
import MySQLdb
import re

# 打开数据库连接
#db = MySQLdb.connect("localhost","root","123456","guahao" )
# 使用cursor()方法获取操作游标 
#cursor = db.cursor()
#cursor.execute("set names utf8")
#sql_select = "select * from hospital"
# 执行SQL语句
#cursor.execute(sql_select)
# 获取所有记录列表
#results = cursor.fetchall()
results = [1]
for row in results:
#	hos_id = row[0]
#	hos_offi__id  = row[]
#	hos_url = "http://www.zj12580.cn/hos/info/"+hos_offi_id
	hos_url = "http://www.zj12580.cn/hos/info/11"
	html = spider(hos_url)
	soup = BeautifulSoup(html)
	div_list = soup.findAll("div", {"class":"right_list_box"})
#	location_match_obj = re.search(r'MapUtil\.showLabel\(\'(\d{1,4}\.d{3,7})\',.*\'(\d{1,4}\.d{3,7})\'',html)
	location_match_obj = re.search(r'MapUtil\.showLabel\(\'(\d{1,5}\.\d{1,7}).{1,5}\'(\d{1,5}\.\d{1,7})',html)
	latitude = location_match_obj.group(1)	#纬度
	longitude = location_match_obj.group(2)	#经度
	print latitude,longitude
	# print len(base_content)
	for one_div in div_list:
		division_name = one_div.find('h5').text.encode("UTF-8")			##########科室名字
		#插入科室信息表
#		sql_div = "insert into division (div_name,hos_id)values('%s',%d)" %  (division_name,hos_id)
#		cursor.execute(sql_div)
#		db.commit()
#		div_id = cursor.lastrowid	#返回div_id,作为门诊插入信息外键
#		print div_id
#		print division_name
		o_list = one_div.find('ul').findAll("a")
		for one_out in o_list:
			out_name = one_out.text.encode('utf8')				###########门诊名字
			out_url = one_out['href']					###########门诊url
			out_match_obj = re.search(r'dept/(\d{1,5})',out_url)		
			out_offi_id = out_match_obj.group(1)				##########官网门诊id
#			sql_o = "insert into outpatient(div_id,o_name,o_url)values(%d,'%s','%s')" %  (div_id,o_name,o_url)
#			cursor.execute(sql_o)
#			db.commit()
			print division_name,out_name,out_url,out_offi_id
#db.close()
