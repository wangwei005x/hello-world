# -*- coding: utf-8 -*-  

import ConfigParser
import os
import string
import commands
import datetime
import json 
import codecs
import time

base_dir = '/data/aclog/dynamicuser/new'

#上传同步时间
last_mtime_file = 0;
new_file={}

def get_last_modify_file():
    list = os.listdir(base_dir)
    filelist = []
    global last_mtime_file;
    global new_file;
    new_file={};
    #上次更新文件的时间
    last_mtime_file_tmp = last_mtime_file;
    for i in range(0, len(list)):
        path = os.path.join(base_dir,list[i])
        if os.path.isfile(path):
            filelist.append(list[i])
            
    for i in range(0, len(filelist)):
        path = os.path.join(base_dir, filelist[i])
        if os.path.isdir(path) or path.find("UserName") >=0:
            continue
        mtime = os.stat(path).st_mtime
        
        #将上传同步后修改的文件加入更新列表
        if mtime > last_mtime_file and mtime < time.time():
            new_file[path] = mtime;
            
        #更新下最近修改时间
        if  last_mtime_file_tmp < mtime:
            last_mtime_file_tmp = mtime;        
    return last_mtime_file_tmp
    
def get_local_user_list():
    global timestart;
    global last_mtime;
    global user_info
    user_info = {}          
    group_path = ""
    localacuser = ""
    now=datetime.datetime.now().strftime('%Y%m%d')
    
    localacuser = input_fileold
    
    if os.path.exists(input_file):
        localacuser = input_file;
   
    if not os.path.exists(localacuser):
        return 1;
    
   # mtime=os.stat(localacuser).st_mtime;
 #   if mtime == last_mtime and now == timestart:
   #     print localacuser + " no need to update\n"
  #      return 1;
    
    #last_mtime = mtime;
    timestart = now;
    
    config.readfp(open(localacuser))
    user_num  = config.get("config","Count")
    print user_num
    
    for i in range(0,int(user_num)):
        group_info = {};
        session = "user"+ str(i)
        user_name = config.get(session,"user")
        group_path = config.get(session,"path")
        group_path = group_path.strip();
        if group_path != "/" and group_path[len(group_path)-1] == '/':
            group_path = group_path[0:len(group_path)-1]
        if group_path.find("未分组") >=  0 or group_path.find("Ungrouped") >=  0:
            continue;
        print group_path
        showname = config.get(session,"showname")
        group_info[acid] = group_path.strip();
        user = [now,showname,group_info]
        user_info[user_name] = user 
    return 0

def get_guest_user_list():
    
    global timestart;
    global user_info    
    global new_file;
    group_path = ""
    now=datetime.datetime.now().strftime('%Y%m%d')
    last_mtime = get_last_modify_file();
   # if last_mtime == last_mtime_file and now == timestart:
  #      print "guest file mtime " + str(last_mtime)+ ",last update:" +str(last_mtime_file) +", no need to update\n"
  #      return 1;
    
    timestart = now;
    order = sorted(new_file.items(),key=lambda e:e[1],reverse=False)
    for  files in order:
        filename=files[0]
        file_object = open(filename)
        print filename
        for line in file_object:
            list = line.split('\t')
            group_info = {};
            if len(list) == 6:
                group_path = list[5]    
                showname = list[4]      
            else:
                continue;
            user_name=list[3]
            group_path = group_path.strip();
            if group_path != "/" and group_path[len(group_path)-1] == '/':
                group_path = group_path[0:len(group_path)-1]            
            if group_path.find("未分组") >= 0 or group_path.find("Ungrouped") >= 0:
                continue;
            print group_path
            group_info[acid] = group_path.strip();
            user = [now,showname,group_info]    
            user_info[user_name] = user 
        file_object.close()
    return last_mtime;

    
if not os.path.exists('/data/aclog/db/log_data/aclog'):
    exit ;


input_file = '/ac/etc/config/fw/acuser.ini.bak'
input_fileold = '/ac/etc/config/fw/acuser.ini'
if os.path.exists('/ac/i18n/chs_flag'):
    js_path = '/data/aclog/db/log_data/aclog/accfg/user.chs/'
    js_file = '/data/aclog/db/log_data/aclog/accfg/user.chs/data.js'
else :
    js_path = '/data/aclog/db/log_data/aclog/accfg/user.eng/'
    js_file = '/data/aclog/db/log_data/aclog/accfg/user.eng/data.js'
    
file_object = open('/AcId.txt')
try:
     acid = file_object.readline().strip()
finally:
     file_object.close( )

timestart=datetime.datetime.now().strftime('%Y%m%d')

statinfo = 0
last_mtime = 0
    
config = ConfigParser.ConfigParser()

user_info = {}


while 1:

    if os.path.exists(js_path):
        print "wait for ldbd to update " + js_path;
        time.sleep(2);
        continue;
    get_local_user_list();  
    last = get_guest_user_list();
    if not user_info:
        time.sleep(2);
        continue;

    json_data = json.dumps(user_info, ensure_ascii=False, encoding='utf-8')
    print json_data
    #json_data = json_data.replace('本地用户','LocalUser')
    os.makedirs(js_path);
    #js_file="test.js"
    fp = file(js_file,'w');
    fp.write(json_data)
    fp.close()
    last_mtime_file = last;
    


