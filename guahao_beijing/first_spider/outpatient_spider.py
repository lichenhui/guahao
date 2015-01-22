#!/usr/bin/env python
#coding=utf8
from BeautifulSoup import BeautifulSoup
from spider import spider
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","root","123456","guahao" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cursor.execute("set names utf8")
sql_select = "select * from hospital"
# 执行SQL语句
cursor.execute(sql_select)
# 获取所有记录列表
results = cursor.fetchall()
for row in results:
	hos_id = row[0]
	hos_url = row[5]
	html = spider(hos_url)
	soup = BeautifulSoup(html)
	base_content = soup.findAll("div", {"class":"yyksbox"})
	# print len(base_content)
	for x in xrange(len(base_content)):
		division_name = base_content[x].find("div",{"class":"yyksdl"}).text.encode("UTF-8")
		#插入科室信息表
		sql_div = "insert into division (div_name,hos_id)values('%s',%d)" %  (division_name,hos_id)
		cursor.execute(sql_div)
		db.commit()
		div_id = cursor.lastrowid	#返回div_id,作为门诊插入信息外键
		print div_id
		print division_name
		o_list = base_content[x].find("div",{"class":"ks_content"}).findAll("a",{"class":"islogin"})
		for y in xrange(len(o_list)):
			o_name = o_list[y].text.encode('UTF-8')
			o_url = o_list[y]['href'].encode('UTF-8')[1:]
			o_url = "http://www.bjguahao.gov.cn/comm"+o_url
			sql_o = "insert into outpatient(div_id,o_name,o_url)values(%d,'%s','%s')" %  (div_id,o_name,o_url)
			cursor.execute(sql_o)
			db.commit()
			print o_name,o_url
db.close()