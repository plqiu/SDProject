#!encoding=utf-8
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import os
import redis
# Create your views here.
redis =redis.Redis(host='localhost', port=6379, decode_responses=True)
data ={}
def fish_home(request):
    module_dir = os.path.dirname(__file__)
    print module_dir
    # file_path = os.path.join(module_dir,'static\info\info.log')
    return render(request,"fishHome.html")
def get_data(request):
    """
    从redis中读取数据并返回给前台界面
    :param request:
    :return:     data[water_pump: 0, disinfect: 0, oxygen_supply: 0, heater: 0, temprature: 0, ph_value: 0]
    """

    data['temperature'] =int(redis.get('temperature'))
    data['ph_value'] = int(redis.get('ph_value'))
    data['water_pump'] = eval(redis.get('water_pump'))
    data['disinfect'] = eval(redis.get('disinfect'))
    data['oxygen_supply'] = eval(redis.get('oxygen_supply'))
    data['heater'] = eval(redis.get('heater'))
    return JsonResponse(data)
def set_data(request):
    """
    从前台界面发送过来的数据传给mqtt服务器，并且存入redis数据库
    :param request:
    :return:
    """
    if request.method == 'POST':
        for i in  request.POST:
            redis.rpush("set_value",i)
            redis.rpush("set_value", request.POST[i])
            print "set_value",i
        print redis.llen('set_value')

    return JsonResponse({'success':True})