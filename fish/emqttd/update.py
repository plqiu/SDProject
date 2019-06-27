# encoding: utf-8
import logging
import sqlite3
import time
import datetime
from api.constant import *
import os

def update():
    # logger = logging.getLogger('fish')
    # conn = sqlite3.connect('./DB.db')
    # sql_w = "SELECT *" \
    #         "FROM fish " \
    #         " where id=(select last_insert_id())"
    # # make file
    # Lock.t_lock.acquire()
    # logger.info('enter auto_makefile')
    # # TODO : 获取数据库数据
    # results = conn.execute(sql_w).fetchall()
    # data = results.fetchone()
    #
    # try:
    #     conn.execute("INSERT INTO TRANS  VALUES (?)", (filename, ))
    #     conn.commit()
    # except:
    #     conn.rollback()
    # finally:
    #     conn.close()
    #     Lock.t_lock.release()
    # logger.info("auto_MakeFile OK...")
    #
    print ("进入 update")