
'''
h=0
x = int(input('enter a number: '))
while h**3 < abs(x):
	h=h+1;
if h**3 != abs(x):
	print(str(x) + ' is not a perfect cute');
else:
	if x < 0:
		h = -h
	print('cube of '+ str(x) + ' is ' + str(h))

 '''
import os
f=open('test.txt','a')
f.write("abd")
f.close()

p=os.environ
print(str(p))

import json
d=dict(a=1,b=2.3,c="3242",e='abc')

r=json.dumps(d)
print(r)

 
