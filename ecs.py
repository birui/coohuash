#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys
import MySQLdb
import re
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
cur = conn.cursor()
update_db = """ update CMDB_hosts set config = %s  where  hostname = %s """

conn.autocommit(True)

t = os.popen(""" cat /Users/admin/coohua/ecs-api/vmList.txt """)

# os.system('echo > /Users/admin/coohua/ecs-api/test.txt')

for i in  t.readlines():
    i = i.replace('\n','')
    print i
    os.system("aliyuncli ecs ExportInstance --InstanceId %s --filename ./test.txt" %(i))
    lip1 = os.popen("aliyuncli ecs DescribeInstanceAttribute --InstanceId %s  --output json  --filter InnerIpAddress.IpAddress\[0\]" %(i),"r")
    wip1 = os.popen("aliyuncli ecs DescribeInstanceAttribute --InstanceId %s  --output json  --filter PublicIpAddress.IpAddress\[0\]" %(i),"r")

    lip = lip1.read()
    lip = lip.replace('"','')
    wip = wip1.read()
    wip = wip.replace('"','')
    #print lip,wip

    file = '/Users/admin/coohua/ecs-api/test.txt'
    fp = open(file, 'r')
    dict = json.loads(fp.read())
    instance_id = dict["InstanceId"]
    hostname = str(dict["InstanceName"])
    cpu = dict["Cpu"]
    mem = dict["Memory"]
    band = dict["InternetMaxBandwidthOut"]

    conf = "CPU:%s Memory:%s Band:%s" %(cpu,mem,band)
    #print conf
    config1 = str(conf)
    a1 = re.compile('\{.*\}' )
    config = a1.sub('',config1)
    cur.execute("select hostname from  CMDB_hosts where hostname = %s",hostname)
    #fetchone()返回一条查询结果
    st_hostname = cur.fetchone()
    db_hostname = st_hostname[0]
     
    print config
    # print(type(config))
    # print db_hostname
    # print hostname
    # print(type(db_hostname))
    # print(type(hostname))
    # print(cmp(hostname,db_hostname))
    #如果主机名一样，就看配置
    if cmp(hostname,db_hostname) == 0 :
        cur.execute("select config from  CMDB_hosts where hostname = %s",hostname)
        st_config = cur.fetchone()
        db_config = st_config[0]
        # print db_config
        # print type(db_config)
        # print type(config)
        # print(cmp(db_config,config))
    #配置不一样的改配置
        if cmp(db_config,config) != 0:
            cur.execute(update_db,[config,hostname])
            conn.commit()
            print " %s != %s  update db" %(db_config,config)

    #库里没的主机新添加
    else:
        value = [instance_id,hostname,lip,wip,config,1,'online',1,1,'test',1]
        cur.execute('insert into CMDB_hosts(instance_id,hostname,lip,wip,config,data_center,environment,status,cost,remark,service_model_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
        conn.commit()
        print "%s no find create hosts" % hostname 
    fp.close()

cur.close()
conn.close()






