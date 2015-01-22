#!/usr/bin/env python
#encoding=utf-8

#识别验证码返回由验证码数字组成的字符串

import Image,ImageEnhance,ImageFilter

#将图片切成四份，并获得四个数字图形的序列,并将序列保存到data.txt文件中
#此函数是用来获取１－９数字的参照序列的
def split_pic_save(image_name):
	im = Image.open(image_name)
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1')
	#im.show()
			#all by pixel
	s = 4          #start postion of first number
	w = 7          #width of each number
	h = 15          #end postion from top
	im_new = []
	#split four numbers in the picture
	for i in range(4):
	    im1 = im.crop((s+w*i,0,s+w*(i+1),15))
	    im_new.append(im1)
	f = file("data.txt","a")
	for k in range(4):
	    l = []
	    #im_new[k].show()
	    for i in range(15):
		for j in range(7):
		    if (im_new[k].getpixel((j,i)) == 255):
			l.append(0)
		    else:
			l.append(1)
	    f.write("l=[")
	    n = 0
	    for i in l:
		if (n%10==0):
		    f.write("\n")
		f.write(str(i)+",")
		n+=1
	    f.write("]\n")
#将图片转为黑白，取出噪点
def  getverify(name):
	# 二值化
	threshold = 140
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	#打开图片
	im = Image.open(name)
	#转化到亮度
	imgry = im.convert('L')
	#imgry.save('g'+name)	#保存图片
	#二值化
	out = imgry.point(table,'1')
	out.save(name)


#将图片切片，并获得四个数字的序列
def split_pic(image_name):
	#调用getverify函数将图片做预处理
	getverify(image_name)
	im = Image.open(image_name)
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1')
	#im.show()
			#all by pixel
	s = 4          #start postion of first number
	w = 7          #width of each number
	h = 15          #end postion from top
	im_new = []
	#split four numbers in the picture
	for i in range(4):
	    im1 = im.crop((s+w*i,0,s+w*(i+1),15))
	    im_new.append(im1)
	    code_data = []
	for k in range(4):
	    l = []
	    for i in range(15):
		for j in range(7):
		    if (im_new[k].getpixel((j,i)) == 255):
			l.append(0)
		    else:
			l.append(1)
	    code_data.append(l) 
	return code_data
def getcode(img):
	refer_dic = {
	1:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,1,0,0,0,0,0,1,1,1,
		0,0,0,0,1,1,1,0,0,0,
		0,0,1,1,0,0,0,0,0,1,
		1,0,0,0,0,0,1,1,0,0,
		0,0,1,1,1,1,0,0,0,0,
		1,1,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	2:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,1,1,1,
		1,1,0,0,0,0,0,1,1,0,
		0,0,0,1,1,1,0,0,0,0,
		1,0,0,0,0,1,1,0,0,0,
		0,1,1,1,0,0,0,0,0,1,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	3:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,1,
		1,1,0,0,0,0,1,1,1,0,
		0,0,0,1,1,1,0,0,0,0,
		1,1,1,0,0,0,0,0,1,1,
		0,0,0,0,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	4:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,1,0,0,0,0,0,1,
		1,1,0,0,0,1,1,1,1,0,
		0,1,1,1,1,1,0,1,1,1,
		1,1,1,1,0,1,0,1,1,1,
		0,0,0,0,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	5:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		1,0,0,0,0,0,1,1,1,1,
		1,0,0,1,1,1,0,0,0,0,
		0,1,0,1,1,1,0,0,0,0,
		0,1,1,0,0,0,0,0,1,1,
		0,0,0,0,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	6:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,1,1,0,
		0,0,1,1,1,1,0,0,0,1,
		1,1,1,0,0,0,1,1,1,1,
		1,1,1,1,1,1,0,0,1,1,
		0,1,1,1,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	7:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,1,0,0,0,0,0,1,
		1,1,0,0,0,0,1,1,0,0,
		0,0,0,1,1,0,0,0,0,1,
		1,0,0,0,0,0,1,1,0,0,
		0,0,1,1,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	8:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,1,1,1,
		1,1,0,1,1,1,1,1,1,0,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,0,0,1,1,
		0,1,1,1,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,],
	9:[
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,1,1,1,
		1,1,0,1,1,0,0,1,1,0,
		1,1,1,1,1,1,0,0,0,0,
		1,1,1,0,0,0,0,1,1,1,
		0,0,0,0,1,1,1,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,]
	}
	code_data = split_pic(img)
	code = ""
	for x in range(len(code_data)):			#循环验证码数字
		for y in refer_dic:					#循环对照序列
			n = 0
			for z in range(len(code_data[x])):	#循环验证码单个数字的０１序列，与对照的１－９学列对照
				if code_data[x][z] == refer_dic[y][z]:
					n+=1
			if n >= len(code_data[x])*0.95:
				code+=`y`
	return code
