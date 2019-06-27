#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas
import json
import time
import os
import datetime
with open("conf/config.json", "r") as f:
    config = json.loads(f.read())

class data_analysis:
    def __init__(self):
        self._start_time =datetime.datetime.strptime(config["start_time"],"%Y-%m-%d %H:%M:%S")
        self._stop_time =datetime.datetime.strptime(config["stop_time"],"%Y-%m-%d %H:%M:%S")
    def _calc_mumber_days(self):
        '''
        输入开始时间和结束时间，自动计算天数，并生成字符串格式的日期数据
        :return:需要采集的日期数组
        '''
        a=self._start_time
        delta = datetime.timedelta(days=1)
        _time_list = [datetime.datetime.strftime(a,"%Y%m%d")]

        for i in range((self._stop_time-self._start_time).days):
            a+=delta
            _time_list.append(datetime.datetime.strftime(a,"%Y%m%d"))
        _data=[]
        for i in _time_list:
            _data.append(config["raw_data_storage_path"] + config["wind_turbine_name"] + "_" + i + ".csv")
        # output = (pandas.read_csv(_data[0], usecols=['timeTick', 'AVERAGE_WIND_SPEED_60S', 'GRID_UL1']))
        return _data
    def Extract_and_store(self):
        """
         提取数据并存储
        timeTick,AVERAGE_WIND_SPEED_60S,GRID_UL1,GRID_I1
        """
        aa= self._calc_mumber_days()
        print aa
        print time.mktime((self._start_time).timetuple()),time.mktime((self._stop_time).timetuple())
        for i in aa:
            try:
                data = pandas.read_csv(i, usecols=config["collect_var_name"])
            except BaseException as e:
                continue
            #采集第一天和最后一天不是整天的数据
            if i==aa[0]:
                data= data[data['timeTick'] > time.mktime((self._start_time).timetuple())]
            if i==aa[-1]:
                data = data[data['timeTick'] < time.mktime((self._stop_time).timetuple())]
            data = data.iloc[range(1,data.shape[0],int(config["interval"]))]
            data["timeTick"] = data["timeTick"].map(lambda x: time.strftime("%Y-%m-%d %H:%M:%S",(time.localtime(x))))
            #采集后直接进行存储，如果有必要可以单独开进程
            if os.path.exists(config["save_file_name"]):
                data.to_csv(config["save_file_name"],float_format='%.2f',header=0,index=0,mode="ab+")
            else :
                data.to_csv(config["save_file_name"],float_format='%.2f',index=0,mode="ab+")
    def _Generate_test_files(self):
        pass
if __name__=="__main__":
    print (time.time ())
    d=data_analysis()
    d.Extract_and_store()
    print time.time()
