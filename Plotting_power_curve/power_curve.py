# -*- coding:utf-8 -*-
import json
import datetime
import pandas
import matplotlib

from Standard_power_curve import standard_power_curve

list_10min_mean = pandas.DataFrame(columns=['WIND_SPEED', "GRID_POWER"])
list_wind_speed_bin = pandas.DataFrame(columns=['WIND_SPEED', "GRID_POWER"])
from matplotlib import pyplot as plt

#设置默认字体
with open("conf/config.json", "r") as f:
    config = json.loads(f.read())
class data_analysis:
    def __init__(self):
        self._start_time =datetime.datetime.strptime(config["start_time"],"%Y-%m-%d %H:%M:%S")
        self._stop_time =datetime.datetime.strptime(config["stop_time"],"%Y-%m-%d %H:%M:%S")
    def data_filter(self):
        for i in self._calc_mumber_days():

            try:
                data = pandas.read_csv(i, usecols=config["collect_var_name"])
            except :
                print (("找到不文件"),i)
                continue

            #删除所有包含空值的行
            data = data.dropna()
            #更改索引列
            data.set_index('timeTick', inplace=True)
            data = data[data["MAIN.POWER_PRODUCTION"] == 1]

            data = data[data["PITCH_POSITION_1"] <= 1]

            #  data =data [data["VISU_CONTROLLER_PITCH_ROTORSPEED_LIMIT"]   >=1549.99 ]
            data = data[data["GEARBOX_OIL_TEMPERATURE_GEARBOX"] <= 75]
            # print data[["WIND_SPEED","GRID_POWER"]]
            self.data_min10_mean(data)
    def data_min10_mean(self,data):
        if pandas.notnull(data.iloc[1:2].index.values):
            global list_10min_mean
            # data.iloc[1:2].index.values[0]第一个索引,data.iloc[-1:].index.values[0]最后一个索引
            for min10 in xrange(data.iloc[1:2].index.values[0], data.iloc[-1:].index.values[0], 600):
                data_min10 = data.loc[min10:min10 + 600]
                #if data_min10.count()['WIND_SPEED'] > 100:
                list_10min_mean = list_10min_mean.append(data_min10.mean(), ignore_index=True)

    def average_power_at_different_wind_speeds(self):

        for i in xrange(6, 50, 1):
            global list_wind_speed_bin
            global list_10min_mean
            _list=list_10min_mean[(list_10min_mean['WIND_SPEED'] <= i / 2.0 + 0.25) & (list_10min_mean['WIND_SPEED'] >= i / 2.0 - 0.25)].mean()

            # print i/2.0
            list_wind_speed_bin = list_wind_speed_bin.append(_list, ignore_index=True)


    def _calc_mumber_days(self):
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

class tools:
    def print_fontlib(self):
    # 查看字体库
        a=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
        for i in a:
            print(i.encode("gbk"))
    def print_all_columns(self):
        data = pandas.read_csv("../data_analysis/data/FJ01_20190201.csv")
        for i in list_10min_mean(data.columns):
            print i

def plot(x_axis_data_list, y_axis_data_list):
    """
    绘制曲线
    :param x_axis_data_list:
    :param y_axis_data_list:
    :return:
    """
    plt.rcParams['font.family'] = ['STFangsong']

    zhfont1 = matplotlib.font_manager.FontProperties(fname="SimHei.ttf")
    plt.title(u"功率曲线")
    plt.xlabel(u"风速", fontproperties=zhfont1)
    plt.ylabel(u"功率", fontproperties=zhfont1)
    a=[]
    for i in xrange(6, 50, 1):
        a.append(i/2.0)
    b= standard_power_curve(a)
    # plt.subplot(2,  1,  1)
    # plt.plot(data["AVERAGE_WIND_SPEED_60S"],data["GRID_POWER"],":b")
    plt.plot(x_axis_data_list, y_axis_data_list, ":b")
    # # plt.plot(x+1,y+1,":r")
    # # plt.subplot(2,  1,  2)
    # # plt.plot(x,y,":b")
    plt.plot(a,b,":r")
    plt.show()
if __name__ == '__main__':
    d = data_analysis()
    d.data_filter()
    d.average_power_at_different_wind_speeds()

    plot(list_wind_speed_bin["WIND_SPEED"], list_wind_speed_bin["GRID_POWER"])
