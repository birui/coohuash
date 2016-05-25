#!/usr/bin/env python
# -*- coding: utf-8 -*-
#通过zabbix数据库获取需要监控的itemid和要显示的监控图id
#然后插入cmdb数据库，通过zabbix_api脚本通过各个itemid获取
#相应的监控数据放入cmdb库的CMDB_iterms表内
import os
import json
import sys
import MySQLdb
import re
import time
import datetime

# startTime = datetime.datetime.now().strftime("%Y-%m-%d 00:00")
# endTime = datetime.datetime.now().strftime("%Y-%m-%d 23:59")
startTime = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d 00:00")
endTime = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d 23:59")
coStart = time.strptime(startTime, "%Y-%m-%d %H:%M")
coEnd = time.strptime(endTime, "%Y-%m-%d %H:%M")

timeStampStart = int(time.mktime(coStart))
timeStampEnd = int(time.mktime(coEnd))


conn_local = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
cur_local = conn_local.cursor()
conn_local.autocommit(True)


conn = MySQLdb.connect(host='#',user='#',passwd='#',db='#',port=)
cur = conn.cursor()
# update_db = """ update CMDB_hosts set config = %s  where  hostname = %s """
conn.autocommit(True)

cur.execute("select hostid,host  from  hosts where host not like '%Template%' and host not like '%CooHua%' and host not like '{%' and hostid != 10378 and hostid != 10329 and hostid !=  10392;")

#返回上面查询是所有日志type 'tuple'。
host_id = cur.fetchall()

for i in host_id:
    item_sql = {}
    item_sql['hostid'] = i[0]
    item_sql['hostname'] = i[1]
    
    print i[0]
    cur_local.execute("select hostid  from  CMDB_iterms where hostid=%s" ,i[0]) #在cmdb库找出hostid方便判断是否已经在库里面
    hostid_local = cur_local.fetchall()
    try:
        hostid_local_cu = hostid_local[0][0]
    except IndexError, e:
        #print 'null %s',e
        hostid_local_cu = ''
    else:
        print hostid_local_cu

    if hostid_local_cu == i[0]: #表示已经有这个hostid就不用再插入了
        newValue = {}
        print '已经存在！'
        cur_local.execute(" select cpu_itemid,cpu_load_itemsid,eth0_in_itemsid,eth0_out_itemsid,eth1_in_itemsid,eth1_out_itemsid,memory_available_itemsid,memory_total_itemsid from  CMDB_iterms where hostid=%s;" ,i[0])
        itemid_local = cur_local.fetchall()
        print 'cpu_itemid:' ,itemid_local[0][0]
        #cpu idle 值获取
        cur.execute("select  min(value)  from history  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][0],timeStampStart,timeStampEnd])
        cpu = cur.fetchall()
        #print 'cpu:' , cpu
        #print 'min', min(cpu[0])
        newValue['cpu_idle'] = cpu[0][0]
        #cpu load 值获取
        print 'cpu_load_itemsid:' ,itemid_local[0][1]
        cur.execute("select  max(value)  from history  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][1],timeStampStart,timeStampEnd])
        cpuLoad = cur.fetchall()
        newValue['cpu_load'] = cpuLoad[0][0]
        #eth0_in
        print 'eth0_in_itemsid:' ,itemid_local[0][2]
        cur.execute("select  max(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][2],timeStampStart,timeStampEnd])
        eth0_in = cur.fetchall()
        newValue['eth0_in'] = eth0_in[0][0]
        #eth0_out
        print 'eth0_out_itemsid:' ,itemid_local[0][3]
        cur.execute("select  max(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][3],timeStampStart,timeStampEnd])
        eth0Out = cur.fetchall()
        newValue['eth0_out'] = eth0Out[0][0]
        #eth1_in
        print 'eth1_in_itemsid:' ,itemid_local[0][4]
        cur.execute("select  max(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][4],timeStampStart,timeStampEnd])
        eth1In = cur.fetchall()
        if eth1In[0][0] is None:
            newValue['eth1_in'] = 'null'
        else:
            newValue['eth1_in'] = eth1In[0][0]
        
        #eth1_out
        print 'eth1_out_itemsid:' ,itemid_local[0][5]
        cur.execute("select  max(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][5],timeStampStart,timeStampEnd])
        eth1Out = cur.fetchall()
        if eth1Out[0][0] is None:
            newValue['eth1_out'] = 'null'
        else:
            newValue['eth1_out'] = eth1Out[0][0]

            
        #memory_available
        print 'memory_available_itemsid:' ,itemid_local[0][6]
        cur.execute("select  min(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][6],timeStampStart,timeStampEnd])
        memory_available = cur.fetchall()
        newValue['memory_available'] = memory_available[0][0]
        #memory_total
        print 'memory_total_itemsid:' ,itemid_local[0][7]
        cur.execute("select  max(value)  from history_uint  where itemid=%s and  clock between %s and %s ;",[itemid_local[0][7],timeStampStart,timeStampEnd])
        memory_total = cur.fetchall()
        newValue['memory_total'] = memory_total[0][0]
        
        print newValue
        for j in newValue.items():
            update = ''' update CMDB_iterms set %s=%s  where hostid=%s ;''' % (  j[0],j[1],i[0] )
            print update
            cur_local.execute(update)
            conn_local.commit()
            #print j[0],j[1]

#如果hostid在cmdb里面没有这添加
    else:
    
        #cpu 空闲率id
        cur.execute("select itemid from items where  key_ = 'system.cpu.util[,idle]' and hostid=%s " ,i[0] )
        cpu_idle = cur.fetchall()
        try:
            cpu_idle_num = cpu_idle[0][0]
        except Exception, e:
            item_sql['cpu_itemid'] = 'null'
        else:
            item_sql['cpu_itemid'] = cpu_idle_num
            cur.execute("select graphid  from  graphs_items where  itemid=%s ",cpu_idle_num)
            cpu_graphs_itemsid = cur.fetchall()[0][0]
            item_sql['cpu_graphs_itemsid'] = cpu_graphs_itemsid

        #print item_sql
        #cpu load id
        cur.execute("select itemid from items where  key_ = 'system.cpu.load[percpu,avg1]' and hostid=%s " ,i[0] )
        cpu_load = cur.fetchall()
        try:
            cpu_load_num = cpu_load[0][0]
        except Exception, e:
            item_sql['cpu_load_itemsid'] = 'null'
        else:
            item_sql['cpu_load_itemsid'] = cpu_load_num
        #print item_sql
        #eth0_in_itemsid  
        cur.execute("select itemid from items where  key_ = 'net.if.in[eth0]' and hostid=%s " ,i[0] )
        eth0_in = cur.fetchall()
        try:
            eth0_in_num = eth0_in[0][0]
        except Exception, e:
            item_sql['eth0_in_itemsid'] = 'null'
        else:
            item_sql['eth0_in_itemsid'] = eth0_in_num
        #print item_sql
        #eth0_out_itemsid
        cur.execute("select itemid from items where  key_ = 'net.if.out[eth0]' and hostid=%s " ,i[0] )
        eth0_out = cur.fetchall()
        try:
            eth0_out_num = eth0_out[0][0]
        except Exception, e:
            item_sql['eth0_out_itemsid'] = 'null'
            item_sql['eth0_graphs_itemsid'] = 'null' 
        else:
            item_sql['eth0_out_itemsid'] = eth0_out_num
            cur.execute("select graphid  from  graphs_items where  itemid=%s ",eth0_out_num)
            eth0_graphs_itemsid = cur.fetchall()[0][0]
            item_sql['eth0_graphs_itemsid'] = eth0_graphs_itemsid

        #print item_sql
        #eth1_in_itemsid  
        cur.execute("select itemid from items where  key_ = 'net.if.in[eth1]' and hostid=%s " ,i[0] )
        eth1_in = cur.fetchall()
        try:
            eth1_in_num = eth1_in[0][0]
        except Exception, e:
            item_sql['eth1_in_itemsid'] = 'null'
        else:
            item_sql['eth1_in_itemsid'] = eth1_in_num
        #print item_sql
        #eth1_out_itemsid
        cur.execute("select itemid from items where  key_ = 'net.if.out[eth1]' and hostid=%s " ,i[0] )
        eth1_out = cur.fetchall()
        try:
            eth1_out_num = eth1_out[0][0]
        except Exception, e:
            item_sql['eth1_out_itemsid'] = 'null'
            item_sql['eth1_graphs_itemsid'] = 'null'
        else:
            item_sql['eth1_out_itemsid'] = eth1_out_num
            cur.execute("select graphid  from  graphs_items where  itemid=%s ",eth1_out_num)
            eth1_graphs_itemsid = cur.fetchall()[0][0]
            item_sql['eth1_graphs_itemsid'] = eth1_graphs_itemsid
        #print item_sql
        #memory_available_itemsid
        cur.execute("select itemid from items where  key_ = 'vm.memory.size[available]' and hostid=%s " ,i[0] )
        memory_available  = cur.fetchall()
        try:
            memory_available_itemsid = memory_available[0][0]
        except Exception, e:
            item_sql['memory_available_itemsid'] = 'null'
        else:
            item_sql['memory_available_itemsid'] = memory_available_itemsid

        #print item_sql
        #memory_total_itemsid
        cur.execute("select itemid from items where  key_ = 'vm.memory.size[total]' and hostid=%s " ,i[0] )
        memory_total  = cur.fetchall()
        try:
            memory_total_itemsid = memory_total[0][0]
        except Exception, e:
            item_sql['memory_total_itemsid'] = 'null'
        else:
            item_sql['memory_total_itemsid'] = memory_total_itemsid

        try:
            insert =  '''insert into CMDB_iterms(hostid,hostname,cpu_itemid,cpu_graphs_itemsid,eth0_graphs_itemsid,eth1_graphs_itemsid,cpu_load_itemsid,eth0_in_itemsid,eth0_out_itemsid,eth1_in_itemsid,eth1_out_itemsid,memory_available_itemsid,memory_total_itemsid,cpu_idle,cpu_load,eth0_in,eth0_out,eth1_in,eth1_out,memory_available,memory_total) values(%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''  % (item_sql['hostid'],item_sql['hostname'],item_sql['cpu_itemid'],item_sql['cpu_graphs_itemsid'],item_sql['eth0_graphs_itemsid'],item_sql['eth1_graphs_itemsid'],item_sql['cpu_load_itemsid'],item_sql['eth0_in_itemsid'],item_sql['eth0_out_itemsid'],item_sql['eth1_in_itemsid'],item_sql['eth1_out_itemsid'],item_sql['memory_available_itemsid'],item_sql['memory_total_itemsid'],'null','null','null','null','null','null','null','null')
            #value = [ item_sql['hostid'],item_sql['hostname'],item_sql['cpu_itemid'],item_sql['cpu_graphs_itemsid'],item_sql['eth0_graphs_itemsid'],item_sql['eth1_graphs_itemsid'],item_sql['cpu_load_itemsid'],item_sql['eth0_in_itemsid'],item_sql['eth0_out_itemsid'],item_sql['eth1_in_itemsid'],item_sql['eth1_out_itemsid'],item_sql['memory_available_itemsid'],item_sql['memory_total_itemsid'],'null','null','null','null','null','null','null','null' ]
            
            #print item_sql
            # print insert
            #cur_local.execute('''insert into CMDB_iterms(hostid,hostname,cpu_itemid,cpu_graphs_itemsid,eth0_graphs_itemsid,eth1_graphs_itemsid,cpu_load_itemsid,eth0_in_itemsid,eth0_out_itemsid,eth1_in_itemsid,eth1_out_itemsid,memory_available_itemsid,memory_total_itemsid,cpu_idle,cpu_load,eth0_in,eth0_out,eth1_in,eth1_out,memory_available,memory_total) values(%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',value)
            #print insert
            cur_local.execute(insert)
        except Exception, e:
            print 'error %s', e
        else:
            conn_local.commit()

cur.close()
conn.close()
cur_local.close()
conn_local.close()





