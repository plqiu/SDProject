# encoding:utf-8

from constant import *
from gevent.server import DatagramServer
import zlib
import json



#用于串口数据采集及指令下发
def serial_collector():
    Message.message[message.keys()[0]] = message.values()[0]


