# GrovePi + Grove Buzzer
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

buzz = 23

GPIO.setup(buzz,GPIO.OUT)

while True:
    try:
        # Buzz for 1 second
        GPIO.output(buzz,True)
        print 'start'
        time.sleep(1)

        # Stop buzzing for 1 second and repeat
        GPIO.output(buzz,False)
        print 'stop'
        time.sleep(1)

    except KeyboardInterrupt:
        GPIO.output(buzz,False)
        break
    except IOError:
        print "Error"
