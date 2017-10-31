import threading
import time


import RPi.GPIO as GPIO

# Turn Off GPIO Warnings
GPIO.setwarnings(False)

# GPIO Mode Set to BCM
GPIO.setmode(GPIO.BCM)

Ultra1_Trigger = 21
Ultra1_Echo = 26
Ultra2_Trigger = 20
Ultra2_Echo = 19
Ultra3_Trigger = 16
Ultra3_Echo = 13
Ultra4_Trigger = 12
Ultra4_Echo = 6

## Set GPIO direction (IN / OUT)
# Ultra Sonic Sensors
GPIO.setup(Ultra1_Trigger, GPIO.OUT)
GPIO.setup(Ultra1_Echo, GPIO.IN)

GPIO.setup(Ultra2_Trigger, GPIO.OUT)
GPIO.setup(Ultra2_Echo, GPIO.IN)

GPIO.setup(Ultra3_Trigger, GPIO.OUT)
GPIO.setup(Ultra3_Echo, GPIO.IN)

GPIO.setup(Ultra4_Trigger, GPIO.OUT)
GPIO.setup(Ultra4_Echo, GPIO.IN)

def UltraSonicSensorDistance():
    # Set Trigger to HIGH
    GPIO.output(Ultra1_Trigger, True)
    GPIO.output(Ultra2_Trigger, True)
    GPIO.output(Ultra3_Trigger, True)
    GPIO.output(Ultra4_Trigger, True)

    time.sleep(0.00001)
 
    # Set Trigger after 0.01ms to LOW
    GPIO.output(Ultra1_Trigger, False)
    GPIO.output(Ultra2_Trigger, False)
    GPIO.output(Ultra3_Trigger, False)
    GPIO.output(Ultra4_Trigger, False)
 
    StartTime1 = time.time()
    StopTime1 = time.time()
    StartTime2 = time.time()
    StopTime2 = time.time()
    StartTime3 = time.time()
    StopTime3 = time.time()
    StartTime4 = time.time()
    StopTime4 = time.time()

    Flag1 = True
    Flag2 = True
    Flag3 = True
    Flag4 = False

    # Save StartTimes
    while(Flag1 or Flag2  or Flag3 or Flag4):
        if(Flag1 and GPIO.input(Ultra1_Echo) == 0):
            StartTime1 = time.time()
        else:
            Flag1 = False

        if(Flag2 and GPIO.input(Ultra2_Echo) == 0):
            StartTime2 = time.time()
        else:
            Flag2 = False
    
        if(Flag3 and GPIO.input(Ultra3_Echo) == 0):
            StartTime3 = time.time()
        else:
            Flag3 = False

        if(Flag4 and GPIO.input(Ultra4_Echo) == 0):
            StartTime4 = time.time()
        else:
            Flag4 = False
    
    
    Flag1 = True
    Flag2 = True
    Flag3 = True
    Flag4 = False
    
    # Save StopTimes
    while(Flag1 or Flag2 or Flag3 or Flag4):
        if(Flag1 and GPIO.input(Ultra1_Echo) == 1):
            StopTime1 = time.time()
        else:
            Flag1 = False

        if(Flag2 and GPIO.input(Ultra2_Echo) == 1):
            StopTime2 = time.time()
        else:
            Flag2 = False
    
        if(Flag3 and GPIO.input(Ultra3_Echo) == 1):
            StopTime3 = time.time()
        else:
            Flag3 = False

        if(Flag4 and GPIO.input(Ultra4_Echo) == 1):
            StopTime4 = time.time()
        else:
            Flag4 = False
    
    # Time difference between start and arrival
    TimeElapsed1 = StopTime1 - StartTime1
    TimeElapsed2 = StopTime2 - StartTime2
    TimeElapsed3 = StopTime3 - StartTime3
    TimeElapsed4 = StopTime4 - StartTime4


    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist1 = (TimeElapsed1 * 34300) / 2
    dist2 = (TimeElapsed2 * 34300) / 2 
    dist3 = (TimeElapsed3 * 34300) / 2
    dist4 = (TimeElapsed4 * 34300) / 2
 
    return (dist1, dist2, dist3, dist4)

##########################################################################


class BackgroundThreadForUltraSonicSensing(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    mindis=0
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        x=0
        dist2=[0,0,0,0] 
        while True:
            dist = UltraSonicSensorDistance()
            for i in range(0,3):
                dist2[i]=dist2[i]+dist[i]
            time.sleep(0.25)
            x=x+1
            if(x%3==0):
                mi=0
                for i in range(0,3):
                    if(dist2[i]<dist[mi]):
                        mi=i
                self.mindis=mi
                dist2=[0,0,0,0]

t1 = BackgroundThreadForUltraSonicSensing()
while(1):
    print('Minimum Distance from ')
    print(t1.mindis)
    print('\n')
    time.sleep(1)

