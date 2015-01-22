#!/usr/lib/env python 
#coding=utf8
#根据数据库里的医院url提取出官网医院的地理位置，经纬度
import MySQLdb
import re
import spider
from BeautifulSoup import BeautifulSoup

db = MySQLdb.connect("localhost","root","123456","guahao" )
cursor = db.cursor()
sql_charset = 'set names utf8'
cursor.execute(sql_charset)
sql = 'select hos_id,hos_url,hos_name from hospital '
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
	hos_id = int(row[0])
	hos_url = row[1]
	hos_name = row[2]
	print hos_name
	if hos_url == 'http://www.bjguahao.gov.cn/comm/yyks-91.html':
		print '朝阳医院出现问题'
	else:
		html = spider.spider(hos_url)
		soup = BeautifulSoup(html)
		link_a = soup.find('a',{'rel':'#gm-ditu'})
		img_src = link_a.find('img')['src'].encode('utf8')
		match_obj = re.match(r'.*center=(\d{1,4}\.\d{4,7}),(\d{1,4}\.\d{5,7}).*',img_src)
		longitude = match_obj.group(1)
		latitude = match_obj.group(2)
		sql_2 = 'update hospital set longitude =%s,latitude=%s where hos_id = %d' % (longitude,latitude,hos_id)
		cursor.execute(sql_2)
		db.commit()
		print longitude,latitude
db.close()

