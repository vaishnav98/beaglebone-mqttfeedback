import paho.mqtt.client as paho
import time
import json
import random
from datetime import datetime
import threading

ClientID = "beaglebone1"

MQTTServer= "m16.cloudmqtt.com"
MQTTPort=
username = ""
password = ""

LastWillTopic = "LWT"
LastWillMessage = ClientID
OutMessageTopic = "beaglebone"
InMessageTopic = "server"

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

def on_publish(client, userdata, mid):
    pass
def on_connect(client, userdata, flags, rc):
    if(rc==0):
        mqttclient.subscribe(InMessageTopic)
def on_message(client, userdata, msg):
    msg.payload=eval(msg.payload)
    if(msg.topic==InMessageTopic):
        print(msg.payload)

def sendData():
    dict1={}
    dict1["Voltage1"]=random.uniform(200.20, 900.45)
    dict1["Current1"]=random.uniform(0.20, 1.50)
    dict1["Voltage2"]=random.uniform(200.20, 900.45)
    dict1["Current2"]=random.uniform(0.20, 1.50)
    mqttclient.publish(OutMessageTopic,str(dict1),qos=1)   

mqttclient = paho.Client(ClientID)
mqttclient.username_pw_set(username,password)
mqttclient.will_set(LastWillTopic,LastWillMessage,qos=1,retain=False)
mqttclient.on_publish = on_publish
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.connect(MQTTServer,MQTTPort)
mqttclient.loop_start()
setInterval(3,sendData)
