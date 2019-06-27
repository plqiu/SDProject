# encoding=utf-8
"""
通过mqtt协议从百度物接入中获取数据并存入redis中
"""
import json
from redis import StrictRedis
import paho.mqtt.client as mqtt
import uuid
broker = '06y0e2v.mqtt.iot.gz.baidubce.com'
port = 1883
username = '06y0e2v/fish'
password = 'x4oEZlsM4UxOiu3P'
clientid = 'test_mqtt_python_' + str(uuid.uuid4())
topic_accepted = '$baidu/iot/shadow/fish/update/accepted'
redis = StrictRedis(host='localhost', port=6379, db=0)
def on_connect(client, userdata, rc):
    print('Connected. Client id is: ' + clientid)
    client.subscribe(topic_accepted)
    print('Subscribed to topic: ' + topic_accepted)
def on_message(client, userdata, msg):
    # msg = json.loads(str(msg.payload))
    data = json.loads(msg.payload)
    # print data["reported"]
    for key ,value in data["reported"].items():
        print key ,":",value
        redis.set(key, str(value))
def start_subscribe():
    client = mqtt.Client(clientid)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    # client.reconnect_delay_set(min_delay=1, max_delay=2000)
    # print('Connecting to broker: ' + broker)
    client.connect(host= broker,port=port)
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    # client.loop_start()
    # client.loop_forever() 有掉线重连功能
    client.loop_forever(retry_first_connection=True)
if __name__ == '__main__':
    # t = threading.Thread(target=start_subscribe)
    # t.setDaemon(True)
    # t.start()
    # t.join()
    start_subscribe()




