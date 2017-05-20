import os
import json
import time
from os.path import join, getsize

new_log="./a"
old_log="./bjson"
old_record_size={};
new_record_size={};
if os.path.exists(old_log):
    os._exit(0)

def store(data,path):
    with open(path, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

##读取json文件，获取已经读取的目录。
if os.path.exists(new_log):
    new_record_size=load(new_log);


#
def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y%m%d")
    return True
  except:
    return False

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size+= sum([getsize(join(root, name)) for name in files])
    return size


aclogdir="./test/a" 
#已经存在于新json中的日期就不要再写入到旧的json
one_day={}
for parent,dirnames,filenames in os.walk(aclogdir):
    for dirname in  dirnames:
        if is_valid_date(dirname) and not (dirname in new_record_size):
            one_day["aclog"]=getdirsize(aclogdir+"/"+dirname);
            one_day["actrace"]=0;
            old_record_size[dirname]=one_day;
            one_day={};
            

            
actracedir="./test/b"

for parent,dirnames,filenames in os.walk(actracedir):
    for dirname in  dirnames:
        if is_valid_date(dirname) and not (dirname in new_record_size):
            if dirname in old_record_size:
                one_day=old_record_size[dirname];           
            else :
                one_day["aclog"]=0;
            one_day["actrace"]=getdirsize(actracedir+"/"+dirname);
            old_record_size[dirname]=one_day;
            

store(old_record_size,old_log);
