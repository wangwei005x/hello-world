# -*- coding: utf-8 -*-

def triangles():
    a=1;
    b=0;
    his=[]
    max=11;
    while a:
      tmp=[]
      while b<a:
        if b==0 or b==a-1:
          tmp.append(1);
        else:
          tmp.append(his[a-2][b]+his[a-2][b-1])
        b=b+1;
      yield tmp
      his.append(tmp)  
      a=a+1;
      b=0;
    return 'done'
	
n=0	
for t in triangles():
    print(t)
    n = n + 1
    if n == 20:
        break
