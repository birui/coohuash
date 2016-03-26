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


conn_local = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
cur_local = conn_local.cursor()
conn_local.autocommit(True)


conn = MySQLdb.connect(host='',user='',passwd='',db='',port=)
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
    cur_local.execute("select hostid  from  CMDB_iterms where hostid=%s" ,i[0])
    hostid_local = cur_local.fetchall()
    try:
        hostid_local_cu = hostid_local[0][0]
    except IndexError, e:
        #print 'null %s',e
        hostid_local_cu = ''
    else:
        print hostid_local_cu

   
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

    insert =  '''insert into CMDB_iterms(hostid,hostname,cpu_itemid,cpu_graphs_itemsid,eth0_graphs_itemsid,eth1_graphs_itemsid,cpu_load_itemsid,eth0_in_itemsid,eth0_out_itemsid,eth1_in_itemsid,eth1_out_itemsid,memory_available_itemsid,memory_total_itemsid,cpu_idle,cpu_load,eth0_in,eth0_out,eth1_in,eth1_out,memory_available,memory_total) values(%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''  % (item_sql['hostid'],item_sql['hostname'],item_sql['cpu_itemid'],item_sql['cpu_graphs_itemsid'],item_sql['eth0_graphs_itemsid'],item_sql['eth1_graphs_itemsid'],item_sql['cpu_load_itemsid'],item_sql['eth0_in_itemsid'],item_sql['eth0_out_itemsid'],item_sql['eth1_in_itemsid'],item_sql['eth1_out_itemsid'],item_sql['memory_available_itemsid'],item_sql['memory_total_itemsid'],'null','null','null','null','null','null','null','null')
    #value = [ item_sql['hostid'],item_sql['hostname'],item_sql['cpu_itemid'],item_sql['cpu_graphs_itemsid'],item_sql['eth0_graphs_itemsid'],item_sql['eth1_graphs_itemsid'],item_sql['cpu_load_itemsid'],item_sql['eth0_in_itemsid'],item_sql['eth0_out_itemsid'],item_sql['eth1_in_itemsid'],item_sql['eth1_out_itemsid'],item_sql['memory_available_itemsid'],item_sql['memory_total_itemsid'],'null','null','null','null','null','null','null','null' ]
    
    if hostid_local_cu == i[0]: #表示已经有这个hostid就不用再插入了
        print '已经存在！'
    else:
        #print item_sql
        # print insert
        #cur_local.execute('''insert into CMDB_iterms(hostid,hostname,cpu_itemid,cpu_graphs_itemsid,eth0_graphs_itemsid,eth1_graphs_itemsid,cpu_load_itemsid,eth0_in_itemsid,eth0_out_itemsid,eth1_in_itemsid,eth1_out_itemsid,memory_available_itemsid,memory_total_itemsid,cpu_idle,cpu_load,eth0_in,eth0_out,eth1_in,eth1_out,memory_available,memory_total) values(%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',value)
        #print insert
        try:
            cur_local.execute(insert)
        except Exception, e:
            print 'error %s', e
        else:
            conn_local.commit()

cur.close()
conn.close()
cur_local.close()
conn_local.close()





