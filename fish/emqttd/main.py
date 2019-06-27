# encoding:utf-8
import time

from serial_collector import serial_test
a = serial_test()
for i in a.rec():
    print (i.decode())

a.set('read 6')
data=[]
for i in a.rec():
    data.append(i)
print (data)

