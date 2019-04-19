import paho.mqtt.client as paho
import pandas as pd
df  = pd.DataFrame(columns = ["Voltage 1","Current 1","Power 1","Voltage 2","Current 2","Power 2"])
df.to_csv("data.csv", index=False)

ClientID = "server1"
MQTTServer= "m16.cloudmqtt.com"
MQTTPort=
username = ""
password = ""

LastWillTopic = "LWT"
LastWillMessage = ClientID
OutMessageTopic = "server"
InMessageTopic = "beaglebone"

def on_publish(client, userdata, mid):
    pass
def on_connect(client, userdata, flags, rc):
    if(rc==0):
        mqttclient.subscribe(InMessageTopic)
def on_message(client, userdata, msg):
    msg.payload=eval(msg.payload)
    if(msg.topic==InMessageTopic):
        print(msg.payload)
        dict1={}
        dict1["Power1"]=msg.payload["Voltage1"]*msg.payload["Current1"]
        dict1["Power2"]=msg.payload["Voltage2"]*msg.payload["Current2"]
        df = pd.read_csv("data.csv")
        df.loc[len(df)] = [msg.payload["Voltage1"], msg.payload["Current1"], dict1["Power1"],msg.payload["Voltage2"], msg.payload["Current2"], dict1["Power2"]]
        df.to_csv("data.csv", index=False)
        mqttclient.publish(OutMessageTopic,str(dict1),qos=1)  

mqttclient = paho.Client(ClientID)
mqttclient.username_pw_set(username,password)
mqttclient.will_set(LastWillTopic,LastWillMessage,qos=1,retain=False)
mqttclient.on_publish = on_publish
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.connect(MQTTServer,MQTTPort)
mqttclient.loop_start()

while True:
    pass
