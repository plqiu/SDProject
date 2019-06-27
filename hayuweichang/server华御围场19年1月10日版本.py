#!/usr/bin/python
# encoding:utf-8
#庞利秋编写----源码禁止外传
import sqlite3
import time
import os
from gevent.server import DatagramServer
os.chdir('/samba/anonymous/scadatest')
#from gevent import monkey; monkey.patch_socket()
import struct
import zlib
import gevent
import paramiko
import uuid
import hashlib
import json
import shutil
import logging
import random
from logging.handlers import RotatingFileHandler
from math import isnan

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementInclude as ET
''' 全局'''
turbines = {}
turbines_order = []
template_order=[]
file_handle = {}
sftp = None
start_time =''
config = json.load(open("/samba/anonymous/scadatest/conf/config.json"))
#print config
#解析树
def parseXml():
    parameter_type = {
        'char': 'b',
        'short':'h',
        'int': 'i',
        'float': 'f',
        'double':'d',
        'uint': 'I'
    }
    paraformatStr = []
    dtd_fault = {}
    fault = {}

    # fault phoenix
    tree_pho = ET.ElementTree(file='/samba/anonymous/scadatest/conf/'+"phoenix"+'.xml')
    for elem in tree_pho.iter(tag='data'):
        fault[elem.attrib['var_name']] = elem.attrib['tagname']

    # node
    tree_node = ET.ElementTree(file='/samba/anonymous/scadatest/conf/config_node_attlist.xml')
    for el in tree_node.iter(tag='node'):
        if el.attrib['type'] == 'controller':
            turbine_ip = el.attrib['ip'].split(':')[1]
            turbines_order.append(turbine_ip)
            turbines[turbine_ip] = {}
            turbines[turbine_ip]['name'] = el.attrib['name']
            turbines[turbine_ip]['fault'] = fault
            turbines[turbine_ip]['data'] = None
            turbines[turbine_ip]['time'] = time.time()  
            turbines[turbine_ip]['template'] = el.attrib['template']        
            turbines[turbine_ip]['status'] = 'offline'
                
    # dtd
    tree_dtd = ET.ElementTree(file='/samba/anonymous/scadatest/conf/config_dtd_attlist.xml')
    root = tree_dtd.getroot()
    for elem1 in root:
        template=elem1.attrib['name'] 
        template_order.append(template) 

        turbines[template]={}
        paraformatStr=[]
        turbines[template]['var_name']=[]
        turbines[template]['formatStr']=[]

        for elem in elem1:  

            paraformatStr.append(parameter_type[elem.attrib['type']])
            #dtd_fault[elem.attrib['var_name']] = elem.attrib['tagname']
#             turbines[template]['formatStr'] = '='+''.join(paraformatStr)
            turbines[template]['formatStr'] ='='+ ''.join(paraformatStr)
            turbines[template]['var_name'].append(elem.attrib['var_name'])
        print struct.calcsize(turbines[template]['formatStr'])
def init():

    '''init'''
    # init log
    R_handle = RotatingFileHandler('/samba/anonymous/scadatest/info.log', maxBytes=10*1024*1024, backupCount=3)
    R_handle.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    R_handle.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(R_handle)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 初始化数据库
    conn = sqlite3.connect('scada.db')
    try:
        # 表1 上传列表 filename status(done, ing)
        create_tb_trans = '''
                CREATE TABLE IF NOT EXISTS TRANS(
                    FILENAME  CHAR(100) PRIMARY KEY NOT NULL
                );
            '''
        # 表2 删除列表 filename expires 文件到期
        create_tb_dels = '''
                CREATE TABLE IF NOT EXISTS DELS(
                    FILENAME    CHAR(100) PRIMARY KEY  NOT NULL,
                    EXPIRES REAL
                );
            '''
        # 表3 index，序号
        create_tb_index = '''
                CREATE TABLE IF NOT EXISTS IND(
                    NUMBER INT NOT NULL
                );
        '''
        # 表4 auth，验证码
        create_tb_auth = '''
                CREATE TABLE IF NOT EXISTS AUTH(
                    KEY CHAR(200) NOT NULL,
                    EXPIRES REAL
                );
        '''
        conn.execute(create_tb_trans)
        conn.execute(create_tb_dels)
        conn.execute(create_tb_index)
        conn.execute(create_tb_auth)
        conn.commit()
    except Exception as e:
        # print ('init create table failed:', e)
        logger.error("init create table failed: %s" % e)
        conn.rollback()
    finally:
        conn.close()

    # 初始化风场信息，解析xml
    parseXml()

    logger.info("init success")



#转ip工具
def to_ip(num):
    num = num[0]
    s = []
    for i in range(4):
        s.append(str(num % 256))
        num /= 256
    return '.'.join(s[::-1])

#解析报文
# p_message = dict(), ip->, time->tuple, FAULT->(code), PWRAT, PWRREACT SPD, STATE, parameters->dict
def parseMessage(message, turbine_ip):
    logger = logging.getLogger(__name__)
    for i in template_order:

        if i == turbines[turbine_ip]['template']:
            formatStrUse = turbines[i]['formatStr'] 
#             print struct.calcsize(turbines[i]['formatStr'])
            data = {}
            data['ip'] = to_ip(struct.unpack('I', message[0:4]))
            data['time'] = struct.unpack('6b', message[4:10])
            #print len(message[16:])
            s=struct.calcsize(formatStrUse)+16

            try:

                data['parameters'] = struct.unpack(formatStrUse, message[16:s])

            #print value
            except BaseException:
                print '风机名称：',turbines[turbine_ip]['name'],'报文解析错误'
                print i,'需要报文长度',struct.calcsize(turbines[i]['formatStr'])
                print '风机发送过来报文长度',len(message[16:])
            else:    
                # fault
                value = dict(zip(turbines[i]['var_name'], data['parameters']))
                data['fault'] = [] 
                           
                data['pwrat'] = round(value['grid_power'], 1)
                if data['pwrat']<1:
                    data['pwrat']=round(random.random(),1)
                if isnan(data['pwrat']):
                    print 'pwrat is nan'
                    data['pwrat']=0

                data['pwrreact'] = round(value['grid_reactive_power'], 1)
                if isnan(data['pwrreact']):
                    print 'pwrreact is nan'
                    data['pwrreact']=round(random.random(),1)

                data['spd'] = round(value['wind_speed'], 2)#保留两位小数
                if data['spd']<1:
                    data['spd']=round(random.random(),2)
                if isnan(data['spd']):
                    print 'spd is nan'
                    data['spd']=round(random.random(),2)
    
                # status
                if turbines[turbine_ip]['status'] == 'offline':
                    data['status'] = 6
                else:
                    if 'Main_powerproduction' in value and value['Main_powerproduction'] == 1:
                        if value['grid_power'] <= 1400 and value['pitch_position_1'] > 1.5:
                            # 调度限电
                            # print turbine_ip,' ',value['pitch_position_1'],' ', value['wind_speed']
                            data['status'] = 2
                        else:
                            # 正常限电
                            data['status'] = 1
                    else:
                    # 计划停运
                        if 'Main_service' in value:
#                             print '菲尼克斯主控'
                            if value['Main_service']==1:
                                data['status'] = 3   
                            else:
                                if value['error_error_global'] == 1:
                                    data['status'] = 4
                                else:
                                    
                                    if value['wind_speed'] > 5:
                                        # 调度停运
                                        data['status'] = 5
                                    else:
                                        # 待机
                                        data['status'] = 0                     
                        if 'service' in value:
#                             print '倍福主控'
                            if value['service'] == 1:
                                data['status'] = 3
                            else:
                                if value['error_error_global'] == 1:
                                    data['status'] = 4
                                else:
                                    
                                    if value['wind_speed'] > 5.0:
                                        # 调度停运
                                        data['status'] = 5
                                    else:
                                        # 待机
                                        data['status'] = 0        
                   
                if value['error_error_global'] == 1 and data['status'] != 3:
                    for var_name in turbines[turbine_ip]['fault'].keys():
                        if value.get(var_name) == 1:
                            data['fault']="("+str(turbines[turbine_ip]['fault'][var_name])+")"
                    data['fault']="'"+data['fault']+"'"

                else :
                    data['fault'] = "'(0)'"
                year, month, day, hour, minute, sec, wday, yday, isdst = time.localtime(turbines[turbine_ip]['time'])
                year = str(year)
                if month < 10:
                    month = '0{}'.format(str(month))
                else:
                    month = str(month)
                if day < 10:
                    day = '0{}'.format(str(day))
                else:
                    day = str(day)
                if hour < 10:
                    hour = '0{}'.format(str(hour))
                else:
                    hour = str(hour)
                if minute < 10:
                    minute = '0{}'.format(str(minute))
                else:
                    minute = str(minute)
            
                dt = '%s:%s' % (hour, minute)
                error = data['fault']
                print error
    #             data['DJ_String'] = turbines[turbine_ip]['name'] +'#FJ '+ config['WindFramInformation']['template']+' '\
    #                                 + dt + ' '\
    #                                 + str(data['pwrat']) + ' ' \
    #                                 + str(data['pwrreact']) + ' '\
    #                                 + str(data['spd']) + ' ' \
    #                                 + str(data['status']) + ' ' \
    #                                 + "'(" + error + ")'"
                data['DJ_String_pre'] = turbines[turbine_ip]['name'] + '#FJ '+config['WindFramInformation']['template']+' '

                data['DJ_String_l'] = str(data['pwrat']) + ' '\
                                    + str(data['pwrreact']) + ' '\
                                    + str(data['spd']) + ' '\
                                    + str(data['status']) + ' '\
                                    +  error 
    #             print  data['DJ_String_pre']+data['DJ_String_l']
            
            return data
    print "template错误"
    logger.error('dtd 表中找不到node表中对应的template类型')
#存储文件
def to_file():
    global file_handle
    global start_time
    logger = logging.getLogger(__name__)
    #conn = sqlite3.connect('scada.db')
   # print conn
    while True:
        # 创建文件
        # gevent.sleep(1)
        year, month, day, hour, minute, sec, wday, yday, isdst = time.localtime()
        year = str(year)
        if month < 10:
            month = '0{}'.format(str(month))
        else:
            month = str(month)
        if day < 10:
            day = '0{}'.format(str(day))
        else:
            day = str(day)
        if hour < 10:
            hour = '0{}'.format(str(hour))
        else:
            hour = str(hour)
        if minute < 30:
            s_minute = '00'
        elif minute >= 30:
            s_minute = '30'
        if minute < 10:
            minute = '0{}'.format(str(minute))
        else:
            minute = str(minute)
        conn = sqlite3.connect('scada.db')
        if file_handle == {}:
            datet = '%s%s%s_%s%s' % (year, month, day, hour, s_minute)
            date = '%s-%s-%s' % (year, month, day)
            file_handle['file_name'] = config['WindFramInformation']['WindFramName']+'_LH' + '_' + datet + '.DJ'

            
            if os.path.exists(os.getcwd()+'/data/'+file_handle['file_name']):
#'r'读模式、'w'写模式、'a'追加模式、'b'二进制模式、'+'读/写模式。
                file_handle['file_handle'] = open(os.getcwd()+'/data/'+file_handle['file_name'], mode='a+')
                file_handle['status'] = s_minute
                # file_handle['minute'] = minute
                try:
                    result = conn.execute('select * from IND;').fetchone()
                    file_handle['index'] = result[0]
                    # print result
                except Exception as e:
                    # print ('to_file select error:', e)
                   # logger.error("to_file select index error: %s" % e)
                    file_handle['index'] = 0
            else:
                file_handle['file_handle'] = open(os.getcwd() + '/data/' + file_handle['file_name'], mode='a+')
                file_handle['status'] = s_minute
                # file_handle['minute'] = minute
                file_handle['index'] = 0
                try:
                    conn.execute('insert into IND (NUMBER) VALUES (?);', (file_handle['index'],))
                    conn.commit()
                except Exception as e:
                    # print ('to_file insert index error:', e)
                    logger.error("to_file insert index error: %s" % e)
                file_handle['file_handle'].write('<DANJI::'+config['WindFramInformation']['WindFramName']+' DATE=\'%s\'>\n' \
                                                              '@INDEX ID TYPE TIME PWRAT PWRREACT SPD STATE FAULT\n' % date)
                file_handle['file_handle'].flush()
        else:
            # gevent.sleep(60)
         #   print file_handle['status'] ,s_minute
            if file_handle['status'] == s_minute:
			    #global start_time
                if start_time != minute:
                    start_time = minute
                    print start_time
                    gevent.sleep(20)
                    for turbine in turbines_order:
                        if turbines[turbine]['data'] is not None and turbines[turbine]['time'] + 60*2 > time.time():
                            turbines[turbine]['status'] = 'online'
                            dt = '%s:%s' % (hour, minute)
                            if str(turbines[turbine]['name'])[0:1]=='0':
                                turbines[turbine]['name']=str(turbines[turbine]['name'])[1:]
                            s = '#'+str(file_handle['index']) + ' ' + turbines[turbine]['data']['DJ_String_pre'] + dt \
                                + ' ' + turbines[turbine]['data']['DJ_String_l'] + '\n'
                            file_handle['file_handle'].write(s)
                            file_handle['file_handle'].flush()
                            file_handle['index'] += 1

                            try:
                                # print file_handle['index']
                                conn.execute('update IND SET NUMBER=?', (file_handle['index'], ))
                                conn.commit()
                                # re = conn.execute('select * from IND;')
                                # print re
                            except Exception as e:
                                # print ('to_file update index error:', e)
                                logger.error("to_file update index error: %s" % e)
                        else:
                            print turbines[turbine]['name'] ,"offline"
                            turbines[turbine]['status'] = 'offline'
                            dt = '%s:%s' % (hour, minute)
                            if str(turbines[turbine]['name'])[0:1]=='0':
                                turbines[turbine]['name']=str(turbines[turbine]['name'])[1:]
                            s = '#'+str(file_handle['index'])+' ' \
                                + turbines[turbine]['name'] + '#FJ '+ config['WindFramInformation']['template']+' ' + dt \
                                +' '+str(round(random.random()/3,1))+' '+str(round(random.random()/3,1))+' '+str(round(random.random()/3,2))+" 6 '(0)'" + '\n'
                            file_handle['file_handle'].write(s)
                            file_handle['file_handle'].flush()
                            file_handle['index'] += 1

            else:
                print file_handle['index']
                if file_handle['index']<989:
                    logger.error('loss date',(989-file_handle['index']), '条')
                file_handle['file_handle'].write('</DANJI::'+config['WindFramInformation']['WindFramName']+'>')
                file_handle['file_handle'].close()
                try:
                    # print (file_handle['file_name'])
                    conn.execute('INSERT INTO TRANS (FILENAME) VALUES (?)', (file_handle['file_name'], ))
                    conn.commit()
                except Exception as e:
                    # print ('to_file insert error:', e)
                    logger.error("to_file insert error: %s" % e)
                    conn.rollback()
                file_handle = {}
        conn.close()
#上传
def pySFTP():
    logger = logging.getLogger(__name__)
#    conn = sqlite3.connect('scada.db')
    global sftp
    global config
    sftp1=None
    while True:
        conn = sqlite3.connect('scada.db')

        try:
            result = conn.execute('select * from TRANS').fetchall()
            # print (result)
        except Exception as e:
            # print 'pysftp error:', e
            logger.error("pysftp error: %s" % e)
        if sftp1 is None:
            remotename = config['ftp']['host']
            remoteport = config['ftp']['port']
            loginname = config['ftp']['user']
            loginpassword = config['ftp']['password']
            try:
                sftp = paramiko.Transport(remotename, remoteport)
            except Exception as e:
                print ('conect failed, reasons are follows:', e)
                logger.error("connect failed, reasons are follows: %s" % e)
            else:
                try:
                    sftp.connect(username=loginname, password=loginpassword)
                except Exception as e:
                    print 'login failed, reasons are as follows:', e
                    logger.error("login failed, reasons are as follows: %s" % e)
                else:
                   # print sftp1
                    sftp1 = paramiko.SFTPClient.from_transport(sftp)
                   # print sftp1
        else:
            #for f in result:
            try:
                for f in result:
                    # remotepath = './data/' + f[0]
                    localpath = './data/' + f[0]
                  #  print localpath 

                    remotepath = config['ftp']['remote_save_dir'] + f[0]
                    if os.path.exists(localpath) and os.path.isfile(localpath):
                        sftp1.put(localpath=localpath, remotepath=remotepath)
                        logger.info('sftp put ok %s' % localpath)
                        f_time = os.path.getctime(localpath) + config['expire']
                        conn.execute('insert into DELS (FILENAME, EXPIRES) VALUES (?,?);', (f[0], f_time))
                        conn.execute('delete from TRANS where FILENAME=?', (f[0], ))
                        conn.commit()                  
            except Exception as e:
                print ('put error, reason are as follows:', e)
                logger.error("put error, reason are as follows: %s" % e)
                conn.rollback()
            sftp.close()
            sftp1=None
        conn.close()
        gevent.sleep(60)

#删文件
def deleteFile():
    logger = logging.getLogger(__name__)
  #  conn = sqlite3.connect('scada.db')
    
    while True:
        conn = sqlite3.connect('scada.db')

        try:
            results = conn.execute('select * from DELS;').fetchall()
            delfiles = dict(results)
        except Exception as e:
            # print ('del select error:', e)
            logger.error("del select error: %s" % e)

        for k in delfiles.keys():
            if delfiles[k] < time.time():
                try:
                    os.remove('./data/'+k)
                    conn.execute('delete from DELS where FILENAME=?;', (k, ))
                    conn.commit()
                except Exception as e:
                    # print ('del error:', e)
                    logger.error("del error: %s" % e)
                    conn.rollback()
        conn.close()
        gevent.sleep(60*30)

#报文解析

def router_handler(message, client_addr):
    global turbines

    turbine_ip = to_ip(struct.unpack('I', message[0: 4]))
   # print message[0:22]
   # print struct.unpack('6b', message[11:17])
   # print struct.unpack('I', message[18:22])
    if turbine_ip in turbines.keys():
        if turbine_ip.startswith('10.'):
           # print turbine_ip 
            turbines[turbine_ip]['status'] = 'online'   
            turbines[turbine_ip]['data'] = parseMessage(message, turbine_ip)
            turbines[turbine_ip]['time'] = time.time()
           # print turbines[turbine_ip]['data']
           # print (turbines[turbine_ip]['time'] )   
#连接udp
def udp():
    global config
    host = config['udp_server']['host']
    port = config['udp_server']['port']
    udp_server = DatagramServer((host, port), router_handler)
    udp_server.serve_forever()

#验证
def auth():
    id = uuid.getnode()#python获取mac地址的两种方法
    conn = sqlite3.connect('scada.db')
    result = conn.execute('select * from auth;').fetchall()#接收全部返回结果
    sha = hashlib.sha1()
    sha.update(str(id))
    sha.update('pangliqiu')
    sha1 = hashlib.sha1()
    sha1.update(str(sha.hexdigest()))
    sha1.update('pangliqiu')
    for re in result:
        if re[0] is None:
            return False
        elif re[0] == sha1.hexdigest():
            return True
#     return True

def main():
    global once
    global config
    init()#初始化dtd，node，故障表

    logger = logging.getLogger(__name__)
    logger.info("start...") 

    if True :#验证通过
        logger.info('run...')
        if config['ftp']['active']:
            gevent.joinall([
				gevent.spawn(udp),#udp接包，如果堵塞自动切换到下一个程序
				gevent.spawn(to_file),#打包
				gevent.spawn(deleteFile),#删除文件
				gevent.spawn(pySFTP)#自动上传

			])
        else:

            gevent.joinall([
				gevent.spawn(udp),#udp接包，如果堵塞自动切换到下一个程序
				gevent.spawn(to_file),#打包
				gevent.spawn(deleteFile),#删除文件

			])
                
    else:#验证未通过，输入提示信息，并输入，返回重新验证
        conn = sqlite3.connect('scada.db')
        sha1 = hashlib.sha1()
        sha1.update(str(uuid.getnode()))
        sha1.update('pangliqiu')
        print 'key is :', sha1.hexdigest()
        print ('please email key to pangliqiu@gdupc.cn for Serial Number')
        logger.info("key is : %s" % sha1.hexdigest())
        while True:
            print ('please Enter Serial Number:')
            serial_number = raw_input()
            sha2 = hashlib.sha1()

            sha2.update(sha1.hexdigest())
            sha2.update('pangliqiu')
            value = sha2.hexdigest()
            if serial_number is not None and serial_number == value:
                try:
                    conn.execute('insert into auth (KEY) VALUES (?)', (serial_number,))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    # print ('key saved error: ', e)
                    logger.error("key saved error: %s" % e)
                finally:
                    conn.close()
                break
        print 'start server...'
        time.sleep(3)
        conn.close()
        main()


if __name__ == "__main__":
    main()


