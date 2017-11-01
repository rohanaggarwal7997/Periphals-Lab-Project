#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    client.disconnect()


client = mqtt.Client()
client.connect("172.16.114.166",1883,60)
client.publish("topic/test", "Hello Rohan and Surabhi");
client.disconnect();

client2 = mqtt.Client()
client2.connect("172.16.114.166",1883,60)
client2.on_connect = on_connect
client2.on_message = on_message
client2.loop_forever()
