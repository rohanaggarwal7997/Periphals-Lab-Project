import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

gpio.setmode (gpio.BCM)

output = 19

gpio.setup (output, gpio.OUT)
p = gpio.PWM(output, 50)  #setting the output channel and the frequence
p.start(2.5)

while (True):
	p.ChangeDutyCycle(7.5)
	time.sleep(1)
	p.ChangeDutyCycle(12.5)
	time.sleep(1)
	p.ChangeDutyCycle(2.5)
	time.sleep(1)



