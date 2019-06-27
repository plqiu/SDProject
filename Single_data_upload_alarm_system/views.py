# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import threading
import json,sys,time
import datetime
import time
import os
import operator
import json

# Create your views here.
#def home(request):
    #return render(request,'home.html')

#读取log文件
def readlogs():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\info.log')
    
    f = open(file_path)

    dicList = {} 
    fileList = f.readlines()  
  
    i = 0
    for fileLine in fileList:       
        dicList[i] = fileLine
        i = i + 1
    f.close()
    
    return dicList

def getOldErrorNumber():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\errorNumber.txt')
    
    f = open(file_path)

    oldNumber = f.read();
    
    f.close()
    return oldNumber

def getNewErrorNumber():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\info.log')
    f = open(file_path)

    dicList = {} 
    fileList = f.readlines()  
  
    i = 0
    for fileLine in fileList:       
        dicList[i] = fileLine
        i = i + 1
    f.close()
    
    select = "ERROR"
    i = 0
    for key , value in dicList.items():
        if select in value:
            i = i + 1;
    
    return i
def setErrorNumber():

    newNumber = getNewErrorNumber()

    Number = str(newNumber)
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\errorNumber.txt')
    f = open(file_path,'w')
    f.write(Number)
    f.close()

    
def load(request):

    if request.method == 'GET':
        offset = request.GET['offset']
        size = request.GET['size']

    value_split = [] 
    dicList_list = []
    loadData = {}
    
    #获取所有日志信息
    dicList = readlogs()
  

    #将日志信息按key值逆序
   
    file_list_rev = sorted(dicList.items(), key=lambda x:x[0], reverse=True)

    

    #将列表转化成字典
    
    dic_list_rev = dict(file_list_rev) 
    
    counter = 0
    for key in dic_list_rev.keys():
        counter = counter + 1

    startIndex = counter-int(offset) - 1
    endIndex = startIndex - int(size)
    #if int(counter) <= int(size):
        #startIndex = counter - 1
        #endIndex = -1
    #else:
        #startIndex = counter-int(offset) - 1
        #endIndex_re = startIndex - int(size)
        #if int(startIndex) < int(size):
            #endIndex = -1
        #else:
           # endIndex = endIndex_re
    print(counter)
    print(startIndex)
    print(endIndex)

    
    #根据offset 和 size 读取要增加显示的日志
    j = 0
    for key , value in file_list_rev:
        dicList_display = {}
        if int(key) <= startIndex and int(key) > endIndex:

            value_split.append(value.split('-'))
            dicList_display['date'] = value_split[j][0] +'-' +value_split[j][1] +'-'+ value_split[j][2]
            dicList_display['location'] = value_split[j][3]
            #dicList_display['type'] = value_split[j][3] + value_split[j][4]
            dicList_display['type'] = value_split[j][4]
            dicList_display['content'] = value_split[j][5]
            dicList_list.append(dicList_display)
            j = j + 1
            print(dicList_display['date']) 
    

    loadData['data'] = dicList_list

  
    loadData['number'] = counter

    #警告判断
    alarm = False
    oldNumber = getOldErrorNumber()
    newNumber = getNewErrorNumber()
    
    if int(newNumber) > int(oldNumber):
        alarm = True

    loadData['alarm'] = alarm
    
    setErrorNumber()
    
    

    return JsonResponse(loadData)

#首页展示
def home(request):

    
    return render(request, 'home.html')

#搜索
def search (request):

    dicList = {}
    list_search = []
    search_display = []
    search_all = {}
    search_error = {}
    search_result = {}
    dicList_list = []
    value_split = []
    if request.method == 'POST':
        date_start = request.POST['start']
        date_end = request.POST['end']
        select = request.POST['choice']
        offset = request.POST['pageStart']
        size = request.POST['pageSize']

    #获取所有日志信息
    dicList_search = readlogs()

    j = 0   
    for key,value in dicList_search.items():
        
        start_date_strp = time.mktime(time.strptime(date_start,'%Y-%m-%d %H:%M:%S' ))
        end_date_strp = time.mktime(time.strptime(date_end,'%Y-%m-%d %H:%M:%S' ))
        #获取All信息
        if select == "ALL":
            date_str = value[0:19]    
            date_strp = time.mktime(time.strptime(date_str,'%Y-%m-%d %H:%M:%S' ))
            if date_strp >= start_date_strp and date_strp <= end_date_strp:
                search_all[j] = value 
                j = j + 1

        #获取查询所有的Error信息
        if select in value:
            date_str = value[0:19]    
            date_strp = time.mktime(time.strptime(date_str,'%Y-%m-%d %H:%M:%S' ))
            
            if date_strp >= start_date_strp and date_strp <= end_date_strp:
                search_error[j] = value 
                j = j + 1

    #将search到all日志信息按key值逆序
    search_all_list = sorted(search_all.items(), key=lambda d:d[0], reverse=True)
    #将列表转化成字典
    search_all_rev = dict(search_all_list)
   
    #将search 到的ERROR日志信息按key值逆序
    search_error_list = sorted(search_error.items(), key=lambda d:d[0], reverse=True)
    #将列表转化成字典
    search_error_rev = dict(search_error_list)
 
    #获取按时间查询到的All总数
    searchAllCounter = 0
    for key in search_all_list:
        searchAllCounter = searchAllCounter + 1

    #获取按时间查询到的ERROR总数
    searchErrorCounter = 0
    for key in search_error_list:
        searchErrorCounter = searchErrorCounter + 1

    if select == "ALL":
        if int(searchAllCounter) <= int(size):
            startIndex = searchAllCounter - 1
            endIndex = -1
        else:
            startIndex = searchAllCounter-int(offset) - 1
            endIndex_re = startIndex - int(size)
            if int(startIndex) < int(size):
                endIndex = -1
            else:
                endIndex = endIndex_re

    if select == "ERROR":
        if int(searchErrorCounter) <= int(size):
            startIndex = searchAllCounter - 1
            endIndex = -1
        else:
            startIndex = searchErrorCounter-int(offset) - 1
            endIndex_re = startIndex - int(size)
            if int(startIndex) < int(size):
                endIndex = -1
            else:
                endIndex = endIndex_re
    
    print(searchAllCounter)
    print(searchErrorCounter)
    print(startIndex)
    print(endIndex)
   
    if select == "ALL":
        d = 0
        for key , value in search_all_list:
            dicList_display = {}
            if int(key) <= startIndex and int(key) > endIndex:

                value_split.append(value.split('-'))
                dicList_display['date'] = value_split[d][0] +'-' +value_split[d][1] +'-'+ value_split[d][2]
                dicList_display['location'] = value_split[d][3]
                #dicList_display['type'] = value_split[d][3] + value_split[d][4]
                dicList_display['type'] = value_split[d][4]
                dicList_display['content'] = value_split[d][5]
                dicList_list.append(dicList_display)
                d = d + 1
        search_result['data'] = dicList_list
        search_result['number'] = searchAllCounter

    if select == "ERROR":
        d = 0
        for key , value in search_error_list:
            dicList_display = {}
            if int(key) <= startIndex and int(key) > endIndex:

                value_split.append(value.split('-'))
                dicList_display['date'] = value_split[d][0] +'-' +value_split[d][1] +'-'+ value_split[d][2]
                dicList_display['location'] = value_split[d][3]
                #dicList_display['type'] = value_split[d][3] + value_split[d][4]
                dicList_display['type'] = value_split[d][4]
                dicList_display['content'] = value_split[d][5]
                dicList_list.append(dicList_display)
                d = d + 1

        search_result['data'] = dicList_list
        search_result['number'] = searchErrorCounter
    
   
    #将列表转化成字典
    #print(search_display)
   
    return JsonResponse(search_result)
    #AJax响应List数据
    #return HttpResponse(json.dumps(search_display), content_type='application/json')


#读取配置文件

def readconf (request):

    
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\conf\config.json')
    
    #with open(file_path,"r") as f:
        #temp = json.dumps(f.read())
    f = file(file_path)
    temp = json.load(f)
    return render(request, 'readconf.html',{'data':temp})

def modifyconf(request):

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\conf\config.json')
    
    #with open(file_path,"r") as f:
        #temp = json.dumps(f.read())
    f = file(file_path)
    temp = json.load(f)
    return render(request, 'modifyconf.html',{'data':temp})

@csrf_exempt

def modify (request):

    data = json.loads(request.body)
    #data1 = json.loads(request.body.decode())
    #data = request.POST.get("samba")
    #data2 = request.POST.get("expire")
    #expire = json.loads(request.POST.['expire'])
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,'static\info\conf\config.json')
    
    print(data)
    with open(file_path,"w") as f:
        json.dump(data,f)

    return HttpResponse('修改成功！');