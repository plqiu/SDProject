# encoding:utf-8

from constant import *
def init():
    # init log
    logger = logging.getLogger('worker')
    global config
    with open("./conf/config.json", 'r') as f:
        config = json.load(f)

    # init database
    Conn.conn = sqlite3.connect('DB.db')
    try:
        fish = '''
                           CREATE TABLE IF NOT EXISTS fish(
                               TIME  CHAR(300)
                           );
                       '''
        Conn.conn.execute(fish)
        Conn.conn.commit()
    except Exception as e:
        print ('init create table failed:', e)
        logger.error("init create table failed: %s" % e)
        Conn.conn.rollback()
    finally:
        Conn.conn.close()
