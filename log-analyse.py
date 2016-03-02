# -*- coding: utf-8 -*- 
import os
import json
import sys
s = os.sep	#根据unix或win，s为\或/
root = s + "data" + s + "coohua" + s + "logs"+ s + "nginx" + s + "20160301"	#要遍历的目录
asp = {}
remote_addr =[]
coohua_id = []

def func(args,dire,fis):	#回调函数的定义
    for f in fis:
        dir = dire + s + f
        print dir
        #t = os.popen("zcat %s|grep 'asp.do' " % dir)
        t = os.popen("zcat %s|grep 'getAuthCode.do' " % dir)
        for status in  t.readlines():
            t = json.loads(status)
            #remote_addr.append(t["remote_addr"])
            #coohua_id.append(t["coohua_id"])
            #asp[t["coohua_id"]] = t["remote_addr"]
           # file = open('log-asp1.txt', 'a')
            file = open('getAuthCode.txt', 'a')
            file.write("%s:%s:%s \n" %(t["request_time"],t["coohua_id"],t["remote_addr"]))
            file.close( )

os.path.walk(root,func,())

#for k,v in asp.items():
#    print k,v

