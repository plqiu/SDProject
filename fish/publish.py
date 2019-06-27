#!encoding=utf-8
"""
将数据从redis上摘取下来，并通过mqtt协议上传到百度天工物接入上
"""
from time import sleep
import paho.mqtt.client as mqtt
import uuid
import redis
redis =redis.Redis(host='localhost', port=6379, decode_responses=True)
broker = '06y0e2v.mqtt.iot.gz.baidubce.com'
port = 1883
username = '06y0e2v/fish'
password = 'x4oEZlsM4UxOiu3P'
clientid = 'test_mqtt_python_' + str(uuid.uuid4())
topic_update = '$baidu/iot/shadow/fish/update'
# content = '{"reported":{"temperature":12,\
#                     "ph_value":7 ,\
#                     "water_pump":true ,\
#                     "disinfect":true,  \
#                     "oxygen_supply":true, \
#                     "heater":true }}'
# content = '{"reported":{"temperature":13}}'
def on_connect(client, userdata, rc):
    print('Connected. Client id is: ' + clientid)
    #
    # client.publish(topic,content )
    # print('MQTT message published.',content)
client = mqtt.Client(clientid)
client.on_connect = on_connect
client.username_pw_set(username, password)
client.connect(host= broker,port=port)
client.loop_start()
while True:
    sleep(0.2)
    var_name = redis.lpop("set_value")
    var_value = redis.lpop("set_value")
    if var_name == None:
        continue
    else:
        if var_value =='1':
            var_value= 'true'
        else: var_value= 'false'

        context='{"reported": {"'+var_name+'":'+var_value+'}}'
        print context
        client.publish(topic_update, context)