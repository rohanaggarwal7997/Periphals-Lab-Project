import paho.mqtt.client as mqtt
import time

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    client.disconnect()
    
client = mqtt.Client()
client.connect("172.16.114.166",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()


time.sleep(5)

client2 = mqtt.Client()
client2.connect("172.16.114.166",1883,60)
client2.publish("topic/test", "Hello Roopansh and Abhishek");
client2.disconnect();



