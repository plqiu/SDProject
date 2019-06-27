# -*- coding: utf-8 -*-
from pymodbus.constants import Endian
from pymodbus.datastore import ModbusSlaveContext
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusServerContext
from pymodbus.datastore.database import SqlSlaveContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
from pymodbus.client.sync import ModbusTcpClient
import random
import redis
import time
import pandas as pd
from twisted.internet.task import LoopingCall
import logging
import numpy as np
import json
# data_table=modbus_release_table.active #读当前sheet
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

'''
var_name,init_value,publish_regisrer,
data_publish_type,publish_address,描述

'''
class Modbus_server:

    def __init__(self):
        global redis
        _data=[]
        self.coil_status_data ={}
        self.input_status_data ={}
        self.holding_register_data ={}
        self.input_register_data = {}
        self.equipment_name={}
        #self.time ：modbus server 循环发布数据时间间隔
        self.time = 1
        '''
        var_name,
        init_value,
        publish_regisrer,
        data_publish_type,
        publish_address,
        scaling,
        description
       '''
        with open("conf/config.json","r") as f:
            self.config=json.loads(f.read())
        self.r = redis.Redis(host=self.config["redis"]["ip"], password=self.config["redis"]["password"], port=self.config["redis"]["port"], decode_responses=True)

        try:
            self._modbus_release_table = pd.read_csv('conf/ModbusServer.csv',
                                                usecols={'var_name':np.string_,
                                                         'equipment_name': np.string_,
                                                         'equipment_addr': np.uint8,
                                                         'init_value': np.float32,
                                                         'publish_regisrer': np.uint8,
                                                         'data_publish_type': np.string_,
                                                         'publish_address': np.uint8,
                                                         'RWmodle':np.string_,
                                                         'scaling': np.string_})

        except:
            print ('load ModbusServer.csv failed')
            log.error('load ModbusServer.csv failed')
        self._init_sparse_data()

    def _init_sequential_data(self):
        """
        连续地址发布，默认起始地址为1，
        """
        self.coil_status_data =[]
        self.input_status_data =[]
        self.holding_register_data = []
        self.input_register_data = []
        for j,i in self._modbus_release_table.iterrows():
            print i
            if i['publish_regisrer']==1:
                self.coil_status_data.append(i['init_value'])
            elif i['publish_regisrer']==2:
                self.input_status_data.append(i['init_value'])
            elif i['publish_regisrer'] == 3:
                if i["data_publish_type"]=="INT":
                    self.holding_register_data.append(i['init_value']*i['scaling'])
                elif i["data_publish_type"]=="FLOAT":
                    for a in self.float32_to_bytecode(i['init_value']*i['scaling']):
                        self.holding_register_data.append(a)
                elif i["data_publish_type"]=="DOUBLE":
                    print ("请完善解析double 数据代码")
            elif i['publish_regisrer'] == 4:
                if i["data_publish_type"]=="INT":
                    self.input_register_data.append(i['init_value']*i['scaling'])
                elif i["data_publish_type"]=="FLOAT":
                    for a in self.float32_to_bytecode(i['init_value']*i['scaling']):
                        self.input_register_data.append(a)

                elif i["data_publish_type"]=="DOUBLE":
                    print ("请完善解析double 数据代码")
            else:
                print ("publish_regisrer 输入错误")
                continue

        if (self.coil_status_data==[]) or (self.input_status_data is None):
            self.coil_status_data=[0]*100
        if (self.input_status_data is None) or (self.input_status_data==[]):
            self.input_status_data=[0]*100
        if (self.holding_register_data is None) or (self.holding_register_data==[]):
            self.holding_register_data=[0]*100
        if (self.input_register_data is None) or (self.input_register_data==[]):
            self.input_register_data=[0]*100
        print self.coil_status_data,self.input_status_data,self.holding_register_data,self.input_register_data
        self._store = ModbusSlaveContext(
            co=ModbusSequentialDataBlock(1, self.coil_status_data),
            di=ModbusSequentialDataBlock(1, self.input_status_data),
            hr=ModbusSequentialDataBlock(1, self.holding_register_data),
            ir=ModbusSequentialDataBlock(1, self.input_register_data))

    def _init_sparse_data(self):
        """
        非连续地址发布，发布地址从配置文件读取，
        """

        for j, i in self._modbus_release_table.iterrows():
            self.equipment_name[i['equipment_name']]="null"
            if i['publish_regisrer'] == 1:
                self.coil_status_data[i['publish_address']]=i['init_value']
            elif i['publish_regisrer'] == 2:
                self.input_status_data[i['publish_address']] = i['init_value']
            elif i['publish_regisrer'] == 3:
                if i["data_publish_type"] == "INT":
                    self.holding_register_data.update({self.input_status_data['publish_address']:(i['init_value'])})
                elif i["data_publish_type"] == "FLOAT":
                    self.holding_register_data.update(
                        dict(enumerate(self.float32_to_bytecode(i['init_value'] ), i['publish_address'])))
                elif i["data_publish_type"] == "DOUBLE":
                    print ("请完善解析double 数据代码")
            elif i['publish_regisrer'] == 4:
                if i["data_publish_type"] == "INT":
                    self.input_register_data.update(
                        {self.input_status_data['publish_address']: (i['init_value'] )})
                elif i["data_publish_type"] == "FLOAT":
                    self.input_register_data.update(
                        dict(enumerate(self.float32_to_bytecode(i['init_value'] ), i['publish_address'])))
                elif i["data_publish_type"] == "DOUBLE":
                    print ("请完善解析double 数据代码")
            else:
                print ("publish_regisrer 输入错误")
                continue
        if (self.coil_status_data=={}) or (self.input_status_data is None):
            self.coil_status_data={0:0}
        if (self.input_status_data is None) or (self.input_status_data=={}):
            self.input_status_data={0:0}
        if (self.holding_register_data is None) or (self.holding_register_data=={}):
            self.holding_register_data={0:0}
        if (self.input_register_data is None) or (self.input_register_data=={}):
            self.input_register_data={0:0}
        print 11111, self.coil_status_data
        # print 22222, self.input_status_data
        # print 33333, self.holding_register_data
        # print 44444, self.input_register_data
        self._store = ModbusSlaveContext(
            di=ModbusSparseDataBlock(self.input_status_data),
            co=ModbusSparseDataBlock(self.coil_status_data),
            hr=ModbusSparseDataBlock(self.holding_register_data),
            ir=ModbusSparseDataBlock(self.input_register_data))
    def float32_to_bytecode(self, value):
        '''
        将浮点型数据转化为整数数据，从而保证一个数据占用一个寄存器
        :param value: 输入的浮点型数据数组
        :return: 转化为整数型数据数据
        '''
        code_date = BinaryPayloadBuilder(payload=None, byteorder=Endian.Big,
                 wordorder=Endian.Little, repack=False)
        # if value is dict:
        #     for i in  value:
        #         code_date.add_32bit_float(i)
        code_date.add_32bit_float(value)
        return code_date.to_registers()

    def dict_Merge(dict1, dict2):
        """
        两个字典合并
        """
        return (dict2.update(dict1))
    def start(self):
        context = ModbusServerContext(slaves={1: self._store}, single=False)
        loop = LoopingCall(f=self.updating_writer, modbus_server_context=(context,))
        loop.start(self.time, now=False)  # initially delay by time
        StartTcpServer(context, address=(self.config["modbusserver"]["ip"],self.config["modbusserver"]["port"]))
    def updating_writer(self,modbus_server_context):
        # pass
        """
        modbus server 主动定期调用，该方法实现从redis中读取风机数据并且发布到modbus server
        :param modbus_server_context:
        :return:
        """
        _start_time=int(time.time()*1000)
        _time=0
        context = modbus_server_context[0]
        readfunction = 0x03 # read holding registers
        writefunction = 0x10
        slave_id = 0x01 # slave address
        # print self.r,self.equipment_name.keys()
        #
        # values = context[slave_id].getValues(1, 50000, 7)
        # print 1111111,type(values[2])
        for e in self.equipment_name.keys():
            # print self.r.keys(e+"*")
            try:
                for i in (self.r.keys(e+"*")):

                    if self.r.ttl(i)>_time:
                        _time = self.r.ttl(i)
                        _a = i

                _data=self.r.get(_a)
                # print _data
                # print ([_data.split(",")])
                self.equipment_name[e] = _data.split(",")
                # print len(self.equipment_name[e])
            except :
                print ("read data from redis error")
        # print self.equipment_name
        for j, i in self._modbus_release_table.iterrows():
            if i['publish_regisrer'] == 1:
                if i['RWmodle']=="W":

                    values= context[slave_id].getValues(1,i['publish_address']-1)
                    # print type(values[0])
                    if isinstance(values[0], bool):
                        # print values,i['publish_address']-1
                        print int(i['equipment_name'][2:]),values[0]
                        self.run_sync_client(i['equipment_addr']-1,values[0],int(i['equipment_name'][2:]))

                context[slave_id].setValues(1, i['publish_address']-1, [int(self.equipment_name[i['equipment_name']][i['equipment_addr']])])
                # print  i['publish_address'],type(self.equipment_name[i['equipment_name']][i['equipment_addr']])
            elif i['publish_regisrer'] == 2:
                context[slave_id].setValues(2, i['publish_address'],
                                            [int(self.equipment_name[i['equipment_name']][i['equipment_addr']])])

            elif i['publish_regisrer'] == 3:
                if i["data_publish_type"] == "INT":
                    context[slave_id].setValues(3, i['publish_address'],
                                                [int(self.equipment_name[i['equipment_name']][i['equipment_addr']])])

                elif i["data_publish_type"] == "FLOAT":
                    # print 11111111111111,self.equipment_name[i['equipment_name']],type(self.equipment_name[i['equipment_name']][i['equipment_addr']])
                    context[slave_id].setValues(3, i['publish_address'],
                                                self.float32_to_bytecode(float(self.equipment_name[i['equipment_name']][i['equipment_addr']])))
                    # print i['publish_address'],self.float32_to_bytecode(float(self.equipment_name[i['equipment_name']][i['equipment_addr']]))
                    # print 11111111,type(self.equipment_name[i['equipment_name']][i['equipment_addr']])
                    # self.holding_register_data.update(dict(enumerate(self.float32_to_bytecode(float(self.equipment_name[i['equipment_name']][i['equipment_addr']])), i['publish_address'])))
                elif i["data_publish_type"] == "DOUBLE":
                    print ("请完善解析double 数据代码")
            elif i['publish_regisrer'] == 4:
                if i["data_publish_type"] == "INT":
                    context[slave_id].setValues(4, i['publish_address'],
                                                [int(self.equipment_name[i['equipment_name']][i['equipment_addr']])])
                elif i["data_publish_type"] == "FLOAT":
                    context[slave_id].setValues(4, i['publish_address'],
                                                self.float32_to_bytecode(float(self.equipment_name[i['equipment_name']][i['equipment_addr']])))
                    # self.input_register_data.update(dict(enumerate(self.float32_to_bytecode(float(self.equipment_name[i['equipment_name']][i['equipment_addr']])), i['publish_address'])))
                elif i["data_publish_type"] == "DOUBLE":
                    print ("请完善解析double 数据代码")
            else:
                print ("publish_regisrer 输入错误")
                continue

        # context[slave_id].setValues(1,writefunction,)
        #
        # values = context[slave_id].getValues(0x01, 50000, 8)
        # print values
        # log.debug("Values from datastore: " + str(values))
        stop_time=int(time.time()*1000)
        # print stop_time-_start_time

    def run_sync_client(self,addr,value,UNIT):
        """
        向数据采集器发送数据
        :param addr:
        :param value:
        :param UNIT:
        :return:
        """
        # UNIT = 0x01
        client = ModbusTcpClient(host=self.config['modbustcp']['host'], port=self.config['modbustcp']["port"])
        client.connect()
        log.debug("Reading Coils")
        rq = client.write_coil(addr, value, unit=UNIT)
        assert (not rq.isError())  # test that we are not an error
        client.close()


if __name__ == "__main__":
    m=Modbus_server()
    m.start()