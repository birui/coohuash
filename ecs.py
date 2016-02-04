#!/usr/bin/env python
import os
import json
import sys
import MySQLdb
import re
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
cur=conn.cursor()

t = os.popen(""" cat /Users/admin/coohua/ecs-api/vmList.txt """)

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
    hostname = dict["InstanceName"]
    cpu = dict["Cpu"]
    mem = dict["Memory"]
    band = dict["InternetMaxBandwidthOut"]

    conf = "CPU:%s Memory:%s Band:%s" %(cpu,mem,band)
    #print conf
    config = str(conf)
    a1 = re.compile('\{.*\}' )
    config = a1.sub('',config)

    value = [instance_id,hostname,lip,wip,config,1,'asp',1,1,'test',1]

    cur.execute('insert into CMDB_hosts(instance_id,hostname,lip,wip,config,data_center,environment,status,cost,remark,service_model_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)

    fp.close()

conn.commit()
cur.close()
conn.close()
