import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

#Global Variables
MOTOR_TIMEOUT = 10

# Define GPIO to use on Pi
Motor_A = 17
Motor_B = 27

print "Motor Movement"

# Set pins as output
GPIO.setup(Motor_A,GPIO.OUT)
GPIO.setup(Motor_B,GPIO.OUT)

# Set trigger to False (Low)
GPIO.output(Motor_A, False)
GPIO.output(Motor_B, False)

# Allow module to settle
time.sleep(0.5)

while 1:

	# Send 10us pulse to trigger
	GPIO.output(Motor_A, True)
	GPIO.output(Motor_B, False)
	time.sleep(MOTOR_TIMEOUT)
	GPIO.output(Motor_A, False)
	GPIO.output(Motor_B. True)
	time.sleep(MOTOR_TIMEOUT)

# Reset GPIO settings
GPIO.cleanup()
