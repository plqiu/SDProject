#!encoding=utf-8
import redis
# 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r.set('name', 'junxi')
# key是"foo" value是"bar" 将键值对存入redis缓存
print(r['name'])
print(r.get('name'))
# 取出键name对应的值
print(type(r.get('name')))