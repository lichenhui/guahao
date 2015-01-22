#!/usr/bin/env python
#coding=utf8
import pycurl
import StringIO

def spider(url):
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	# ch.setopt(ch.VERBOSE, 1)		#查看http信息
#	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	ch.setopt(ch.URL, url)	#传入url
	# ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	return html
