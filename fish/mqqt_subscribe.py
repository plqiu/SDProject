#!encoding=utf-8
import json
import threading
from time import sleep
import redis
import gl_var
import paho.mqtt.client as mqtt
import sys
import uuid

broker = '06y0e2v.mqtt.iot.gz.baidubce.com'
port = 1883
username = '06y0e2v/fish'
password = 'x4oEZlsM4UxOiu3P'

clientid = 'test_mqtt_python_' + str(uuid.uuid4())
topic = '$baidu/iot/shadow/fish/update/accepted'
redis =redis.Redis(host='localhost', port=6379, decode_responses=True)
def on_connect(client, userdata, rc):
    print('Connected. Client id is: ' + clientid)
    client.subscribe(topic)
    print('Subscribed to topic: ' + topic)

def on_publish(client, userdata, rc):
    topic = '$baidu/iot/shadow/fish/update'
    content= '{"desired":{"temperature":16}}'
    client.publish(topic,content )
    print('MQTT message published.')
'''
{
    "requestId": "b38de570-a771-4c86-8429-53a186d8795a",
    "reported": {
        "temperature": 13,
        "ph_value": 7,
        "water_pump": true,
        "disinfect": true,
        "oxygen_supply": true,
        "heater": true
    },
    "desired": { },
    "lastUpdatedTime": {
        "reported": {
            "temperature": 1556528768910,
            "ph_value": 1556528768910,
            "water_pump": 1556528768910,
            "disinfect": 1556528768910,
            "oxygen_supply": 1556528768910,
            "heater": 1556528768910
        },
        "desired": { }
    },
    "profileVersion": 373
}'''
def on_message(client, userdata, msg):
    # msg = json.loads(str(msg.payload))
    data = json.loads(msg.payload)
    print data["reported"]
    for key ,value in data["reported"].items():
        redis.set(key, str(value))
def start_subscribe():

    client = mqtt.Client(clientid)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    # client.reconnect_delay_set(min_delay=1, max_delay=2000)
    print('Connecting to broker: ' + broker)
    client.connect(host= broker,port=port)
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    # client.loop_start()
    # client.loop_forever() 有掉线重连功能
    client.loop_forever(retry_first_connection=True)

if __name__ == '__main__':
    t = threading.Thread(target=start_subscribe)
    t.setDaemon(True)
    t.start()
    t.join()



