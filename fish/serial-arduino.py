#!/usr/bin/env python
# -*- coding: utf-8 -*

import serial
import serial.tools.list_ports

port_list = list(serial.tools.list_ports.comports())

if len(port_list) <= 0:
    print ("The Serial port can't find!")

else:
    port_list_0 = list(port_list[0])

    port_serial = port_list_0[0]

    ser = serial.Serial(port_serial, 115200, timeout=0.1)
    print (ser)
    print ("Link...", ser.name)
    data = ''
    while 1:
        num = ser.inWaiting() > 0
        if ser.inWaiting():
            print (ser.readline())
#
#
# class Ser(object):
#     def __init__(self):
#         # 打开端口
#         self.port = serial.Serial(port='3', baudrate=115200, timeout=2)
#         print (self.port)
#
#     # 发送指令的完整流程
#     def send_cmd(self, cmd):
#         self.port.write(cmd)
#         response = self.port.readall()
#         response = self.convert_hex(response)
#         return response
#
#     # 转成16进制的函数
#     def convert_hex(self, string):
#         res = []
#         result = []
#         for item in string:
#             res.append(item)
#         for i in res:
#             result.append(hex(i))
#         return result
