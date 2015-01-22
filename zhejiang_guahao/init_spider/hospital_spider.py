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
#定义地区字典
hos_area = {
	3399:'省直',
	3301:'杭州',
	3302:'宁波',
	3303:'温州',
	3304:'嘉兴',
	3305:'湖州',
	3306:'绍兴',
	3307:'金华',
	3308:'衢州',
	3309:'舟山',
	3310:'台州',
	3311:'丽水',
	3312:'义乌',
}
#定义医院类型
hos_class = {
	1:'综合医院',
	2:'儿科医院',
	3:'妇产科医院',
	4:'肿瘤医院',
	5:'五官科医院',
}
#定义等级
hos_level = {
	33:'三级甲等',
	30:'三级医院',
	20:'二级医院',
	10:'一级医院',
}
num = 0
for x in hos_class:	#遍历医院类型
	for y in hos_level:	#遍历医院等级
		for z in hos_area:		#遍历医院所属地区
			#开始抓取页面并解析
			hos_class_key = x
			hos_level_key = y
			hos_area_key = z
			url = "http://www.zj12580.cn/hos/all?page=1&pageSize=30&levelId="+`hos_level_key`+"&typeId="+`hos_class_key`+"&areaId="+`hos_area_key`
			html = spider(url)
			print hos_level[hos_level_key],hos_class[hos_class_key],hos_area[hos_area_key]
			# 进行页面解析
			soup = BeautifulSoup(html)
			content = soup.find('div',{"class":"left_hos_bottom"})
			hos_list = content.findAll("tr")
			# 当页面没有有效内容时，结束此次循环
			if len(hos_list) == 0:		
				continue
			for n in range(len(hos_list)):
				hos_info = hos_list[n].find('p',{'class':'title'}).find('a')
				hos_name = hos_info.text.encode('utf8')		#医院名字
				hos_url = hos_info['href']			#医院url
				match_obj = re.match(r'.*hos/info/(\d{1,4})\?deptCode.*',hos_url)
				hos_offi_id = match_obj.group(1)		#官网医院id
	#			sql = "insert into hospital(hos_name,class,level,region,hos_url)\
				#values('%s',%d,%d,%d,'%s')" %(hos_name,hos_class_key,hos_level_key,hos_area_key,hos_url)
		#		try:
		#		   # 执行sql语句
		#		   
		#		   cursor.execute(sql)
		#		   # 提交到数据库执行
		#		   db.commit()
		#		except:
		#		   # 发生错误时回滚
		#		   db.rollback()
				print hos_name,hos_url,hos_offi_id
				num +=1
				# 每个页面解析完后，p＋１进行下一页的抓取并解析
# 关闭数据库连接
#db.close()	
print num
