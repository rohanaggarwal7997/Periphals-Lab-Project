import paho.mqtt.client as mqtt
import time


import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


# Define GPIO to use on Pi
Motor_A = 17
Motor_B = 27

# Set pins as output
GPIO.setup(Motor_A,GPIO.OUT)
GPIO.setup(Motor_B,GPIO.OUT)


GPIO.output(Motor_A, True)
GPIO.output(Motor_B, False)

start=time.time()
# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
	if(msg.payload.decode()=="left"):
	    GPIO.output(Motor_A, True)
	    GPIO.output(Motor_B, False)
	    time.sleep(1)
	else:
   	    GPIO.output(Motor_A, False)
	    GPIO.output(Motor_B, True)
	    time.sleep(1)

	end=time.time()
	if(end-start>30):
		client.disconnect()


    #client.disconnect()

try:
	while(1):
		client = mqtt.Client()
		client.connect("172.16.114.166",1883,60)

		client.on_connect = on_connect
		client.on_message = on_message

		client.loop_forever()

		client.connect("172.16.114.166",1883,60)
		client.publish("topic/test2", "Game OVER");
		client.disconnect()
		break


except KeyboardInterrupt:
        print("Stopped by User!")
        GPIO.cleanup()
        time.sleep(1)


GPIO.cleanup()
time.sleep(1)

# time.sleep(5)

# client2 = mqtt.Client()
# client2.connect("172.16.114.166",1883,60)
# client2.publish("topic/test", "Hello Roopansh and Abhishek");
# client2.disconnect();



