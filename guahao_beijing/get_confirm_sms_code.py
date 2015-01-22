#!/usr/bin/env python
#coding=utf8
#
#获取确认挂号页面的短信验证码
import pycurl
import StringIO
# from urllib import urlencode


def get_confirm_smscode(url_part,cookie_file,referer_url,proxy):
	spider_url = 'http://www.bjguahao.gov.cn/comm/shortmsg/dx_code.php?'+url_part
	ch = pycurl.Curl()
	buffer_con = StringIO.StringIO()

	header = [
		"Content-Type: application/x-www-form-urlencoded; charset=UTF-8", 
		"Accept:*/*", 
		#"Accept-Encoding:gzip,deflate,sdch",
		"Cache-Control:max-age=0", 
		"Connection:keep-alive",
		"Host:www.bjguahao.gov.cn",
		"Referer:"+referer_url,
		"User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
	]
	ch.setopt(ch.URL, spider_url)
#	ch.setopt(ch.VERBOSE, 1)		#查看http信息
	ch.setopt(ch.FOLLOWLOCATION, 1)
	ch.setopt(ch.HTTPHEADER, header)
	ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
	# ch.setopt(ch.POSTFIELDS, post_data)	#发送的数据
	ch.setopt(ch.COOKIEFILE, cookie_file)
	ch.setopt(ch.COOKIEJAR, cookie_file)	#保存ｃｏｏｋｉｅ
	if proxy : ch.setopt(ch.PROXY, 'http://125.46.100.198:9999')	#设置代理服务器
	ch.perform()
	html=buffer_con.getvalue()
	buffer_con.close()
	ch.close()
	html = unicode(html,'gbk').encode('utf8')
	return html

if __name__ == '__main__':
	#url_part = 'hpid921227=920868&ksid921227=920868&v921227=920868&PEg921227=920868&lqgalascf921227=920868&aslqgalascf=920868hpid=108&ksid=%B8%DF%D1%AA%D1%B9%BF%C6&datid=305816'
	url_part = 'hpid921227=920868&ksid921227=920868&v921227=920868&PEg921227=920868&lqgalascf921227=920868&aslqgalascf=920868hpid=108&ksid=%B8%DF%D1%AA%D1%B9%BF%C6&datid=305816'
	cookie_file = 'cookie.txt'
	referer_url = 'http://www.bjguahao.gov.cn/comm/anzhen/guahao.php?hpid=108&ksid=%B8%DF%D1%AA%D1%B9%BF%C6&datid=305816'
	response = get_confirm_smscode(url_part,cookie_file,referer_url,False)
	print response
