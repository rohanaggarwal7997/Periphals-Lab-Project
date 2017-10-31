import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

mot = 23

GPIO.setup(mot, GPIO.IN)         #Read output from PIR motion sensor

while True:
       i = GPIO.input(mot)

       if i==0:                 #When output from motion sensor is LOW
             print ("No intruders")
             time.sleep(0.1)

       elif i==1:               #When output from motion sensor is HIGH
             print ("Intruder detected")
             time.sleep(0.1)
