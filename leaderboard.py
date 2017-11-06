import paho.mqtt.client as mqtt
import time

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("topic/test2")

def on_message(client, userdata, msg):
	print(msg.payload.decode())
  
client = mqtt.Client()
client.connect("172.16.114.166",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()