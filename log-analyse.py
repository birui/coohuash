# -*- coding: utf-8 -*- 
import os
import json
import sys
s = os.sep	#根据unix或win，s为\或/
root = s + "data" + s + "coohua" + s + "logs"+ s + "nginx" + s + "20160301"	#要遍历的目录
asp = {}
remote_addr =[]
coohua_id = []

def func(args,dire,fis):	#回调函数的定义walk(root,callable,args)方法有三个参数：要遍历的目录，回调函数，回调函数的参数（元组形式
    for f in fis:
        dir = dire + s + f
        print dir
        #t = os.popen("zcat %s|grep 'asp.do' " % dir)
        t = os.popen("zcat %s|grep 'getAuthCode.do' " % dir) #os.popen和os.system()一样执行命令的
        for status in  t.readlines(): #按行读
            t = json.loads(status) #解析json
            file = open('getAuthCode.txt', 'a') #追加到打开文件
            file.write("%s:%s:%s \n" %(t["request_time"],t["coohua_id"],t["remote_addr"]))
            file.close( )

os.path.walk(root,func,())#调用

#for k,v in asp.items():
#    print k,v

