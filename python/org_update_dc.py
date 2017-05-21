# -*- coding: utf-8 -*-  

import ConfigParser
import os
import string
import commands
import datetime
import json 
import codecs
import time


if not os.path.exists('/data/aclog/db/log_data/aclog'):
    exit ;


input_file = '/ac/etc/config/fw/org.ini'
if os.path.exists('/ac/i18n/chs_flag'):
    js_path = '/data/aclog/db/log_data/aclog/accfg/group.chs/'
    js_file = '/data/aclog/db/log_data/aclog/accfg/group.chs/data.js'
else :
    js_path = '/data/aclog/db/log_data/aclog/accfg/group.eng/'
    js_file = '/data/aclog/db/log_data/aclog/accfg/group.eng/data.js'
    
file_object = open('/AcId.txt')
try:
     getacid = file_object.readline().strip()
finally:
     file_object.close( )
     
timestart=datetime.datetime.now().strftime('%Y%m%d')

statinfo = 0
last_mtime = 0   

config = ConfigParser.ConfigParser()     
while 1:

    if os.path.exists(js_path):
        print "wait for ldbd to update " + js_path;
        time.sleep(2);
        continue;

    now=datetime.datetime.now().strftime('%Y%m%d')

    mtime=os.stat(input_file).st_mtime;

    if mtime == last_mtime and now == timestart:
        print input_file + " no need to update\n"
        time.sleep(2);
        continue;
    
    last_mtime = mtime;
    timestart = now;
     
    
    config.readfp(open(input_file))  
    group_num = config.get("Config","Count")

    print group_num

    acid = [getacid];
    group_data = [int(now),acid]

    


    group_info = {}
    for i in range(0,int(group_num)):
        session = "group"+ str(i)
        group_name = config.get(session,"name")
        group_path = config.get(session,"path")
        group = group_path+group_name
        if group_name != "":
            #group = group+"/"
			group = group
        group_info[group] = group_data
        
    json_data = json.dumps(group_info, ensure_ascii=False, encoding='utf-8')
    #json_data = json_data.replace('本地用户','LocalUser')
    print json_data
    os.makedirs(js_path);
    fp = file(js_file,'w');
    fp.write(json_data)
    fp.close()
    


