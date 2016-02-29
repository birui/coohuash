#!/usr/bin/env python
import os
import json
import sys

#t=os.popen(""" tail -n 4000  /data/coohua/logs/nginx/log.asp_coohua_com """)

t=os.popen("""  cat /data/coohua/logs/nginx/log.asp_coohua_com |grep $(date +%Y-%m-%dT%H:%M)  """)
status = []
response_time = []
statuscode = []

for status in  t.readlines():
        t=json.loads(status)
        #print t["upstream_ip"] , t["response_time"], t["status"]
        response_time.append(t["response_time"])
        statuscode.append(t["status"])


#print statuscode 
#responsenumb = len(response_time)
#statuscodenumb = len(statuscode)
#print response_time

responsemaxtime=max(response_time)

countstatuscode = len(statuscode)+.0

if 'response_max' in sys.argv:
        print  responsemaxtime

if '200' in sys.argv:
        count200 = statuscode.count('200')
        #proportion200 = round (count200 / countstatuscode,2)
        #print proportion200
        print count200

if '301' in sys.argv:
        count301 = statuscode.count('301')
        #proportion301 = round (count301 / countstatuscode,2)
        #print proportion301
        print count301

if '302' in sys.argv:
        count301 = statuscode.count('301')
        #proportion301 = round (count301 / countstatuscode,2)
        #print proportion301
        print count301

if '404' in sys.argv:
        count404 = statuscode.count('404')
        #proportion404 = round (count404 / countstatuscode,2)
        #print proportion404
        print count404

if '403' in sys.argv:
        count404 = statuscode.count('404')
        #proportion404 = round (count404 / countstatuscode,2)
        #print proportion404
        print count404

if '500' in sys.argv:
        count500 = statuscode.count('500')
        #proportion500 = round (count500 / countstatuscode,2)
        #print proportion500
        print count500

if '503' in sys.argv:
        count503 = statuscode.count('503')
        #proportion503 = round (count503 / countstatuscode,2)
        #print proportion503
        print count503
