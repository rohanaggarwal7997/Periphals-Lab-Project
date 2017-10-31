import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_X = 23
GPIO_Y = 24

GPIO.setup(GPIO_X,GPIO.IN)
GPIO.setup(GPIO_Y,GPIO.IN)

while True:
    try:
        # Get X/Y coordinates
        x = GPIO.input(GPIO_X)
        y = GPIO.input(GPIO_Y)

        # Calculate X/Y resistance
        #Rx = (float)(1023 - x) * 10 / x
        #Ry = (float)(1023 - y) * 10 / y

        # Was a click detected on the X axis?
        #click = 1 if x >= 1020 else 0

        print("x =", x)
	print(" y =", y)
        time.sleep(.5)

    except IOError:
        print ("Error")
