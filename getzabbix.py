#!/usr/bin/env python2.7
#coding=utf-8
import urllib2
import json
zabbix_url="http://115.28.203.116/zabbix/api_jsonrpc.php"
api_pass='CooHua007'
auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':'Admin','password':api_pass},'id':1}
#auth function
def get_auth():
    request=urllib2.Request(zabbix_url,json.dumps(auth_data))
    request.add_header('Content-Type','application/json')
    response=urllib2.urlopen(request)
    var1=json.loads(response.read())
    return var1['result'],var1['id']

def get_groupid():
    session=get_auth()
    
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"hostgroup.get",
       "params":{
           "output":["groupid","name"],
       },
       "auth":session[0], 
       "id":session[1],
    })
    # create request object
    request = urllib2.Request(zabbix_url,data)
    request.add_header('Content-Type','application/json')
    # get host list
    try:
       result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()
        print "Number Of Hosts: ", len(response['result'])
        #print response
        for group in response['result']:
            print "Group ID:",group['groupid'],"\tGroupName:",group['name']

def get_hostid():
    session = get_auth()
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"host.get",
       "params":{
           "output":["hostid","name"],
           "groupids":"1", #get groupid是11的机器
       },
       "auth":session[0], 
       "id":session[1],
    })

    request = urllib2.Request(zabbix_url,data)
    request.add_header('Content-Type','application/json')

    try:
       result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()
        print "Number Of Hosts: ", len(response['result'])
        for host in response['result']:
            print "Host ID:",host['hostid'],"HostName:",host['name']

def get_items():
    session = get_auth()
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"item.get",
        "params":{
            "output":["itemids","key_"],
            "hostids":"10157",
        },
        "auth":session[0],
        "id":session[1],
    })
    
    request = urllib2.Request(zabbix_url,data)
    request.add_header('Content-Type','application/json')
    try:
       result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()
        print "Number Of Hosts: ", len(response['result'])
        for host in response['result']:
            print host

def get_history():
    session = get_auth()
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"history.get",
        "params":{
            "output":"extend",
            "history":0, #0 - float; ; 
            "itemids":"28306",
            "limit":10
        },
        "auth":session[0],
        "id":session[1],
    })
    request = urllib2.Request(zabbix_url,data)
    request.add_header('Content-Type','application/json')
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
    	response = json.loads(result.read())
        result.close()
        print "Number Of Hosts: ", len(response['result'])
        for host in response['result']:
            print host
        
    	   


test = get_history()











