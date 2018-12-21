# -*- coding: utf-8 -*-
# @Date     : 2018-12-17 17:56:11
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6




import subprocess, os 
images = os.listdir('./images') 
#qss = os.listdir('./qss') 
f = open('images.qrc', 'w+') 
f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource>\n') 
for item in images: 
	f.write(u'<file alias="images/'+ item +'">images/'+ item +'</file>\n') 
#for item in qss: 
#	f.write(u'<file alias="qss/'+ item +'">qss/'+ item +'</file>\n') 
f.write(u'</qresource>\n</RCC>') 
f.close() 

pipe = subprocess.Popen(r'pyrcc5 -o images.py images.qrc', stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, creationflags=0x08)

