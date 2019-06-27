# _*_ encoding:utf-8 _*_
import logging
import sys
import time

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from api.update import update
from api.init import *
from api.serial_collector import serial_collector

logger = logging.getLogger('worker')
jobstores = {
    'default': SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(4)
}
job_defaults = {
    "coalesce": False,
    "max_instance": 7
}
start_time = time.time()

def test():
    print "test: %s" % time.time()

def main():
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    try:
        scheduler.add_job(serial_collector, 'cron', minute="*/1")
        scheduler.add_job(update, 'cron', minute="*/1")
 #       scheduler.add_job(deleteDb, 'cron', day="*/1")
        scheduler.start()
        # this is here to simulate application activity (which keeps the main thread alive)
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print "异常退出"
        scheduler.shutdown()
    sys.exit()

if __name__ == '__main__':
    init()
    main()


