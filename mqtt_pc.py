#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt

# This is the Publisher

# def on_connect(client, userdata, flags, rc):
#   print("Connected with result code "+str(rc))
#   client.subscribe("topic/test")

# def on_message(client, userdata, msg):
#     print(msg.payload.decode())
#     client.disconnect()
import curses, time

#--------------------------------------
def input_char(message):
    try:
        win = curses.initscr()
        while True: 
            ch = win.getch()
            if ch in range(32, 127): break
            time.sleep(0.05)
    except: raise
    finally:
        curses.endwin()
    return chr(ch)

client = mqtt.Client()
client.connect("172.16.114.166",1883,60)

while(1):

	# uncomment if you don't want dynamic input amd comment the non commented part
	'''
	val = input_char('')
	if(val=="l"):
		client.publish("topic/test", "left")
	else:
		client.publish("topic/test", "right");

	'''
	val = raw_input("Where do you want to go")
	if(val=="l"):
		client.publish("topic/test", "left")
	else:
		client.publish("topic/test", "right");
	time.sleep(0.1)
	


client.disconnect();

# client2 = mqtt.Client()
# client2.connect("172.16.114.166",1883,60)
# client2.on_connect = on_connect
# client2.on_message = on_message
# client2.loop_forever()
