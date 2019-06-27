# encoding: utf-8

from logging.handlers import RotatingFileHandler
import logging
import Queue
import os

from modbus_server import Modbus_server

print  os.getcwd()
from TASKS import TASK

logging.basicConfig()
logger = logging.getLogger('worker')
logger.setLevel(logging.ERROR)
format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

handle_1 = RotatingFileHandler(filename='./log.txt', mode='a', maxBytes=10*1024*1024,
                               backupCount=2)
handle_1.setFormatter(format)
handle_1.setLevel(logging.ERROR)
handle_2 = logging.StreamHandler()
handle_2.setLevel(logging.INFO)
handle_2.setFormatter(format)

logger.addHandler(handle_1)
logger.addHandler(handle_2)

Q = Queue.Queue()

def mystart(wind_turbine_number):
    task = TASK(Q)

    #给第三方转发数据modbus   server
    modbus_server = Modbus_server()
    task.addhandler(modbus_server)
    task.start()


if __name__ == "__main__":
    mystart(1)