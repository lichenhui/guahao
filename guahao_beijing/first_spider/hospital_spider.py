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

num = 0
for x in xrange(1,12):	#遍历医院类型
	for y in xrange(1,4):	#遍历医院等级
		for z in xrange(1,17):		#遍历医院所属地区
			p = 1
			while True:
				#开始抓取页面并解析
				hos_class = x
				hos_level = y
				hos_region = z
				#url地址说明：list-0(地区)-0（等级）-1（类型）-1（分页页码）
				url = "http://www.bjguahao.gov.cn/comm/list-"+`hos_region`+"-"+`hos_level`+"-"+`hos_class`+"-"+`p`+".html"
				html = spider(url)
				# 进行页面解析
				soup = BeautifulSoup(html)
				content = soup.find('div',{"class":"yy_content"})
				hos_list = content.findAll("ul")
				# 当页面没有有效内容时，结束此次循环
				if len(hos_list) == 0:		
					break
				for n in range(len(hos_list)):
					hos_name = hos_list[n].find("a").text.encode("UTF-8")
					hos_url = hos_list[n].find('a')['href'].encode("UTF-8")
					hos_url = "http://www.bjguahao.gov.cn"+hos_url
					sql = "insert into hospital(hos_name,class,level,region,hos_url)\
					values('%s',%d,%d,%d,'%s')" %(hos_name,hos_class,hos_level,hos_region,hos_url)
					try:
					   # 执行sql语句
					   
					   cursor.execute(sql)
					   # 提交到数据库执行
					   db.commit()
					except:
					   # 发生错误时回滚
					   db.rollback()
					print hos_name,hos_url
					num +=1
				# 每个页面解析完后，p＋１进行下一页的抓取并解析
				p+=1
# 关闭数据库连接
db.close()	
print num
