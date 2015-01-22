#!/usr/bin/env python#coding=utf-8 #此文件为挂号系统总接口api import reg_check_idcard_num	#此文件文检查注册人身份证号码合法性
import reg_check_phone
import reg_get_sms_code	#注册时获取图片验证码，获取短信验证码
import reg_post
import login
import get_date_info
import get_detail
import confirm
import get_confirm_sms_code
import confirm_post
import cancel

#注册时检查身份证是否已经在北京挂号官网注册过
#传参：idcard_num:身份证号
#      cookie_file:cookie文件
#       proxy:代理服务器，若传入False则不用代理
#返回：result:布尔类型－－true:此身份证号没有被注册过；flase(官网返回此字符串，应该是官网程序员拼写错误):该号已经被注册
def reg_check_id_card(idcard_num,cookie_file,proxy):
	return  reg_check_idcard_num.check_id_card(idcard_num,cookie_file,proxy)
##################################################################################
#------------------注册时检查手机号是否已经注册过２次
#传参：phone_num:手机号
#       cookie_file:cookie文件
#       proxy:代理服务器
#返回：若为空：手机号未被注册超过２次
#       其他，字符串形式，手机号已经注册超过２次
def check_phone(phone_num,cookie_file,proxy):
	return reg_check_phone.check_phone(phone_num,cookie_file,proxy)

#注册时获取官网的短信验证码
#传参：phone_num:手机号
#      cookie_file:cookie文件
#      proxy:代理服务器
#返回：result:字典类型　code-->图片验证码；res------->获取短信验证码的回复，来自官方网站,若为false,则短信发送已达今日上限（一天最多发４此）
#                                                      否则为用｜分割的字符串，其中一部分为短信验证码
def reg_get_sms_code(phone_num,cookie_file,proxy):
	return reg_get_sms_code.get_sms_code(phone_num,cookie_file,proxy)
	
#注册提交信息注册完成
#传参：cookie_file:cookie文件
#      data:传入的注册信息:字典类型键名分别为：truename真实姓名
 #                                              　gender性别:男／女　
#					       idcard_num身份证号　
#					       code图片验证吗:get_sms_code返回的字典中的code值
#					       　phone_num手机号　
#					       　sms_code短信验证码
#      proxy:代理服务器
#返回：注册成功的提示信息中文字符串
def reg_post(cookie_file,data,proxy):
	result = reg_post.reg_post(cookie_file,data,proxy)
	return result
#登陆北京挂号官网
#   传参:        ------------truename:真实姓名; 
#                   ------------id_card_num:身份证号
#                   ------------cookiefile:存放cookie的文件
#                   ------------code_img:验证码图片，登陆后应注意删除
#                   ------------proxy:代理服务器如：'http://125.46.100.198:9999'
#      返回:        ------------字符串：若为空，则登陆成功，
#	                        其他情况就是出现问题，此字符串则为问题提示
def login(truename,id_card_num,cookie_file,code_img,proxy):
	return login.Login(truename,id_card_num,cookie_file,code_img,proxy)

#选择门诊后，进入该门诊的具体近期可否挂号情况,
#         传参：url:选择门诊的url          -------------------------------------------------------------------------(1)
#	              比如： http://www.bjguahao.gov.cn/comm/content.php?hpid=108&keid=%D0%C4%CD%E2%BF%C6
#		year:年
#		month:月份
#             cookie_file:保存cookie的文件
#            referer_url:来自那个url,就是选择医院的url 
#              proxy:代理服务器如：'http://125.46.100.198:9999'
#        返回:   字典类型的数据，对应一个月所有日期的可否挂号情况，
#                                  键为日（１－３０／３１），
#                                 值为可否挂号情况,０＝过去的或者无号
##                                  若值为list类型，list[0]＝＝１：约满，若list[0] == 2:可预约
#	                                          list[1] = 具体那一天的url-------------------------------------------------(2)
#				!!!!!其中：键next_month对应下一个月是否可挂号,True可以,False不可以
def GetDateInfo(url,year,month,cookie_file,referer_url,proxy):
	return GetDateInfo(url,year,month,cookie_file,referer_url,proxy)

#####################################################################################
#---------------获得某个门诊某个日期详细挂号信息,包括医生，职称，是否约满等信息
#                传参：spider_url:要抓取的url,即标号为(2)的url-------------------------------------------------------------(3)
#                      cookie_file:存放cookie文件
#                     referer_url:来自那个url,即标号为(1)的url
#                       proxy:代理服务器如：'http://125.46.100.198:9999'
#               返回:list类型，每个元素也为list类型，代表一个可挂号的医生的具体信息
#                               每个元素为11或者12个长度的list类型(11:约满；12:可预约):
#                                    0:日期；1：星期几；2：午别；３：科室；４：医生；５：医生职称；
#                                   ６：挂号费；７专长：８：可挂号数；９：剩余号；１０：操作（预约挂号／约满）
#                                          !!!!!!若１０为预约挂号，则还有11：挂号的url-------------------------------------------(4)
#
def get_detail(spider_url,cookie_file,referer_url,proxy):
	return get_detail.get_detail(spider_url,cookie_file,referer_url,proxy)

###########################################################################################
#获取挂号信息确认页面，抓取加密字段信息
#传参：spider_url:要抓取的确认页面，即前面的url(4)-------------------------------------------------------------------------(5)
#      cookie_file:cookie文件
#      referer_url:来自url,即前面的url(3)
#      proxy:代理服务器
#返回：字典类型:   hidden_data---->页面中加密的字段内容，类型为字典类型-------------------------------------------------(6)
#                  url_part------->用于发送确认短信验证码的部分加密url----------------------------------------------------(7)
def get_confirm_info(spider_url,cookie_file,referer_url,proxy):
	return confirm.get_confirm_page(spider_url,cookie_file,referer_url,proxy)

#############################################################################################
#---------------------------发送确认页面的短信验证码
#传参：url_part:用于拼凑发送短信url，即前面的url(7)
#      cookie_file:cookie文件
#      referer_url:来自哪个url,即前面的url(5)
#返回：来自官网的发送短信验证码提示信息，中文字符串
def get_confirm_sms_code(url_part,cookie_file,referer_url,proxy):
	return get_confirm_sms_code.get_confirm_smscode(url_part,cookie_file,referer_url,proxy)

####################################################################################################
#-----------------------提交挂号确认信息，挂号完成！！！！
#传参：cookie_file:coookie文件
#      referer_url:来自哪个url,即前面的url(5)
#      data:要发送的数据，字典类型：键分别为：jiuzhenka:就诊卡号；
#						yibaoka:医保卡号;
#						baoxiao:报销类型;
#						sms_code:短信验证码
#     hidden_data:从确认页面提取的一些加密字段，即前面的(6)号字典
#     proxy:代理服务器
#返回：如果挂号成功，则返回字典类型：键tag------->True,cdkey------>用户挂号预约的识别码，８为数字
#       若挂号失败，则返回中文字符串，内容为错误的提示
def confirm_post(cookie_file,referer_url,data,hidden_data,proxy):
	return confirm_post.this_main(cookie_file,referer_url,data,hidden_data,proxy)

######################################################################################################
#------------------------取消预约---------------------------------------------
#传参：iden_code:预约识别码
#	offi_hos_id:官网医院id
#	cookie_file:cookie文件
#	proxy:代理服务器，若False则不用代理
#返回:0 = 无挂号记录　１＝取消成功　２＝　其他情况
#
def cancel(iden_code,offi_hos_id,cookie_file,proxy):
	return cancel.this_main(iden_code,offi_hos_id,cookie_file,proxy)

