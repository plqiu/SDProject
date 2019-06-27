# encoding:utf-8
from functools import wraps
import json
import sqlite3
import threading
import logging
from logging.handlers import RotatingFileHandler

with open("./conf/config.json") as f:
    config = json.load(f)

def singleton(cls):
    _instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]
    return getinstance


@singleton
class Message(object):
    message = {}


@singleton
class Sftp(object):
    sftp = None


@singleton
class Config(object):
    config = config


@singleton
class Conn(object):
    conn = sqlite3.connect("./DB.db")

@singleton
class Lock(object):
    t_lock = threading.Lock()


log = logging.getLogger('worker')
log.setLevel(logging.DEBUG)
format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

handle_1 = RotatingFileHandler(filename='./worker.log', mode='a', maxBytes=10*1024*1024,
                               backupCount=2)
handle_1.setFormatter(format)

handle_2 = logging.StreamHandler()
handle_2.setFormatter(format)

log.addHandler(handle_1)
log.addHandler(handle_2)

if __name__ == "__main__":
    m = Message().message
    n = Message().message
    #print m == n
   # print id(m), id(n)
