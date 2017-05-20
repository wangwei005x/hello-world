# -*- coding: utf-8 -*-  
import os,sys
import json
import time
from os.path import join, getsize
#import commands
group_file="./groupname.js"



group={};


def store(data,path):
    with open(path, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

#读取json文件，获取已经读取的目录。
if os.path.exists(group_file):
    group=load(group_file);
else:
    os._exit(0)

one_group="";
for name in group:
    one_group=group[name];
    if one_group[len(one_group)-1] != '/':
        group[name]=one_group+"/";
        print(group[name]);


store(group,group_file);

