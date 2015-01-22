#!/usr/lib/env python 
#coding=utf8
#根据数据库里的医院url提取出官网医院id，并存到医院表里，为取消挂号功能做准备
import MySQLdb
import re

db = MySQLdb.connect("localhost","root","123456","guahao" )
cursor = db.cursor()
sql = 'select hos_id,hos_url from hospital '
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
	hos_id = row[0]
	hos_url = row[1]
	match_obj = re.match(r'.*yyks-(\d{1,3})',hos_url)
	if match_obj:
#		print hos_url ,match_obj.group(1)
		sql_2 = "update hospital set offi_hos_id = %d where hos_id = %d" % (int(match_obj.group(1)),int(hos_id))
		cursor.execute(sql_2)
		db.commit()
db.close()
