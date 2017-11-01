import threading
import time
import smbus
import RPi.GPIO as GPIO
from adafruit import Adafruit_I2C
import grovepi
import os
import random


#Global Variables
MOTOR_TIMEOUT = 10
LIGHTTHRESHHOLD = 100000
BOX_CHANGE_TIMEOUT = 5
LIGHT1_VALID = True
LIGHT2_VALID = True
LIGHT3_VALID = True
global I2C_ADDRESS
global I2C_SMBUS
global _CMD
global _CMD_CLEAR
global _CMD_WORD
global _CMD_BLOCK
global _REG_CONTROL
global _REG_TIMING
global _REG_ID
global _REG_BLOCKREAD
global _REG_DATA0
global _REG_DATA1
global _POWER_UP
global _POWER_DOWN
global _GAIN_LOW
global _GAIN_HIGH
global _INTEGRATION_START
global _INTEGRATION_STOP
global _INTEGRATE_13
global _INTEGRATE_101
global _INTEGRATE_402
global _INTEGRATE_DEFAULT
global _INTEGRATE_NA
global _GAIN
global _MANUAL
global _INTEG
global _CHANNEL0
global _CHANNEL1
global _D0
global _D1
global _LUX


# bus parameters
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    I2C_SMBUS = smbus.SMBus(1)
else:
    I2C_SMBUS = smbus.SMBus(0)

# Default I2C address
I2C_ADDRESS = 0x29

# Commands
_CMD       = 0x80
_CMD_CLEAR = 0x40
_CMD_WORD  = 0x20
_CMD_BLOCK = 0x10

# Registers
_REG_CONTROL   = 0x00
_REG_TIMING    = 0x01
_REG_ID        = 0x0A
_REG_BLOCKREAD = 0x0B
_REG_DATA0     = 0x0C
_REG_DATA1     = 0x0E

# Control parameters
_POWER_UP   = 0x03
_POWER_DOWN = 0x00

# Timing parameters
_GAIN_LOW          = 0b00000000
_GAIN_HIGH         = 0b00010000
_INTEGRATION_START = 0b00001000
_INTEGRATION_STOP  = 0b00000000
_INTEGRATE_13      = 0b00000000
_INTEGRATE_101     = 0b00000001
_INTEGRATE_402     = 0b00000010
_INTEGRATE_DEFAULT = _INTEGRATE_402
_INTEGRATE_NA      = 0b00000011

# Testing parameters
ambient  = None
IR       = None
_ambient = 0
_IR      = 0
_LUX     = None


# Turn Off GPIO Warnings
GPIO.setwarnings(False)

# GPIO Mode Set to BCM
GPIO.setmode(GPIO.BCM)

# Ultrasonic Sensors
Ultra1_Trigger = 21
Ultra1_Echo = 26
Ultra2_Trigger = 20
Ultra2_Echo = 19
Ultra3_Trigger = 16
Ultra3_Echo = 13
Ultra4_Trigger = 12
Ultra4_Echo = 6

# Light Sensors
Light1 = 17
Light2 = 27
Light3 = 22

# DC Motors
Motor_A = 23
Motor_B = 24

## Set GPIO direction (IN / OUT)
#Light Detect Sensors
GPIO.setup(Light1,GPIO.OUT)
GPIO.setup(Light2,GPIO.OUT)
GPIO.setup(Light3,GPIO.OUT)

# Ultra Sonic Sensors
GPIO.setup(Ultra1_Trigger, GPIO.OUT)
GPIO.setup(Ultra1_Echo, GPIO.IN)

GPIO.setup(Ultra2_Trigger, GPIO.OUT)
GPIO.setup(Ultra2_Echo, GPIO.IN)

GPIO.setup(Ultra3_Trigger, GPIO.OUT)
GPIO.setup(Ultra3_Echo, GPIO.IN)

GPIO.setup(Ultra4_Trigger, GPIO.OUT)
GPIO.setup(Ultra4_Echo, GPIO.IN)

# DC-Motor Pins Set pins as output
GPIO.setup(Motor_A,GPIO.OUT)
GPIO.setup(Motor_B,GPIO.OUT)

# Allow module to set up
time.sleep(0.01)

class BackgroundThreadForUltraSonicSensing(object):
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


class BackgroundThreadForMotorMovement(object):

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
        while 1:
            GPIO.output(Motor_A, True)
            GPIO.output(Motor_B, False)
            time.sleep(MOTOR_TIMEOUT)
            GPIO.output(Motor_A, False)
            GPIO.output(Motor_B, True)
            time.sleep(MOTOR_TIMEOUT)


class BackgroundThreadForBoxNumber(object):
    ValidBox = 0
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
        while 1:
            Box = randint(1,4)
            self.ValidBox = Box
            time.sleep(BOX_CHANGE_TIMEOUT)


class Tsl2561(object):
        i2c = None

        def _init__(self, bus = I2C_SMBUS, addr = I2C_ADDRESS, debug = 1, pause = 0.8):  # set debug = 0 stops debugging output on screen
            assert(bus is not None)
            assert(addr > 0b000111 and addr < 0b1111000)

            self.i2c     = Adafruit_I2C(addr)
            self.pause   = pause
            self.debug   = debug
            self.gain    = 0
            self._bus    = bus
            self._addr   = addr

            ambient        = None
            IR             = None
            self._ambient  = 0
            self._IR       = 0
            self._LUX      = None
            self._control(_POWER_UP)
            self._partno_revision()

        def _lux(self, gain):
            '''
            Returns a lux value.  Returns None if no valid value is set yet.
            '''
            var = readLux(gain)
            ambient = var[0]
            IR = var[1]
            self._ambient = var[2]
            self._IR = var[3]
            self_LUX = var[4]
            return (ambient, IR, self._ambient, self._IR, self._LUX)

        def setGain(self, gain = 1):
            """ Set the gain """
            if (gain != self.gain):
                if (gain==1):
                    cmd = _CMD | _REG_TIMING
                    value = 0x02
                    self.i2c.write8(cmd, value)  # Set gain = 1X and timing = 402 mSec
                    if (self.debug):
                        print "Setting low gain"
                else:
                    cmd = _CMD | _REG_TIMING
                    value = 0x12
                    self.i2c.write8(cmd, value)  # Set gain = 16X and timing = 402 mSec
                    if (self.debug):
                        print "Setting high gain"
                self.gain=gain;  # Safe gain for calculation
                time.sleep(self.pause)  # Pause for integration (self.pause must be bigger than integration time)

        def readWord(self, reg):
                """ Reads a word from the TSL2561 I2C device """
                try:
                        wordval = self.i2c.readU16(reg)
                        newval = self.i2c.reverseByteOrder(wordval)
                        if (self.debug):
                                print("I2C: Device 0x%02X: returned 0x%04X from reg 0x%02X" % (self._addr, wordval & 0xFFFF, reg))
                        return newval
                except IOError:
                        print("Error accessing 0x%02X: Chcekcyour I2C address" % self._addr)
                        return -1

        def readFull(self, reg = 0x8C):
                """ Read visible + IR diode from the TSL2561 I2C device """
                return self.readWord(reg);

        def readIR(self, reg = 0x8E):
                """ Reads only IR diode from the TSL2561 I2C device """
                return self.readWord(reg);

        def readLux(self, gain = 0):
                """ Grabs a lux reading either with autoranging (gain=0) or with specific gain (1, 16) """
                if (self.debug):
                        print "gain = ", gain
                if (gain == 1 or gain == 16):
                        self.setGain(gain)  # Low/highGain
                        ambient = self.readFull()
                        IR = self.readIR()
                elif (gain == 0):  # Auto gain
                        self.setGain(16)  # First try highGain
                        ambient = self.readFull()
                        if (ambient < 65535):
                                IR = self.readIR()
                        if (ambient >= 65535 or IR >= 65535):  # Value(s) exeed(s) datarange
                                self.setGain(1)  # Set lowGain
                                ambient = self.readFull()
                                IR = self.readIR()

                # If either sensor is saturated, no acculate lux value can be achieved.
                if (ambient == 0xffff or IR == 0xffff):
                    self._LUX = None
                    self._ambient = None
                    self._IR = None
                    return (self.ambient, self.IR, self._ambient, self._IR, self._LUX)
                if (self.gain == 1):
                    self._ambient = 16 * ambient  # Scale 1x to 16x
                    self._IR = 16 * IR            # Scale 1x to 16x
                else:
                    self._ambient = 1 * ambient
                    self._IR = 1 * IR
                if (self.debug):
                    print "IR Result without scaling: ", IR
                    print "IR Result: ", self._IR
                    print "Ambient Result without scaling: ", ambient
                    print "Ambient Result: ", self._ambient

                if (self._ambient == 0):
                # Sometimes, the channel 0 returns 0 when dark ...
                    self._LUX = 0.0
                return (ambient, IR, self._ambient, self._IR, self._LUX)

                ratio = (self._IR / float(self._ambient))  # Change to make it run under python 2

                if (self.debug):
                        print "ratio: ", ratio

                if ((ratio >= 0) and (ratio <= 0.52)):
                        self._LUX = (0.0315 * self._ambient) - (0.0593 * self._ambient * (ratio ** 1.4))
                elif (ratio <= 0.65):
                        self._LUX = (0.0229 * self._ambient) - (0.0291 * self._IR)
                elif (ratio <= 0.80):
                        self._LUX = (0.0157 * self._ambient) - (0.018 * self._IR)
                elif (ratio <= 1.3):
                        self._LUX = (0.00338 * self._ambient) - (0.0026 * self._IR)
                elif (ratio > 1.3):
                        self._LUX = 0

                return (ambient, IR, self._ambient, self._IR, self._LUX)

        def _partno_revision(self):
                """ Read Partnumber and revision of the sensor """
                cmd = _CMD | _REG_ID
                value = self.i2c.readS8(cmd)
                part = str(value)[7:4]
                if (part == "0000"):
                        PartNo = "TSL2560CS"
                elif (part == "0001"):
                        PartNo = "TSL2561CS"
                elif (part == "0100"):
                        PartNo = "TSL2560T/FN/CL"
                elif (part == "0101"):
                        PartNo = "TSL2561T/FN/CL"
                else:
                        PartNo = "not TSL2560 or TSL 2561"
                RevNo = str(value)[3:0]
                if (self.debug):
                        print "responce: ", value
                        print "PartNo = ", PartNo
                        print "RevNo = ", RevNo
                return (PartNo, RevNo)

        def _control(self, params):
                if (params == _POWER_UP):
                        print "Power ON"
                elif (params == _POWER_DOWN):
                        print "Power OFF"
                        os.system("clear")
                else:
                        print "No params given"
                cmd = _CMD | _REG_CONTROL | params
                self.i2c.write8(self._addr, cmd)  # select command register and power on
                time.sleep(0.4)  # Wait for 400ms to power up or power down.


def LightDetectUtility(Light):
    TSL2561 = Tsl2561()
    TSL2561._init__(I2C_SMBUS, I2C_ADDRESS)
    StartTime = time.time()
    while(True):        

        gain=0
        val = TSL2561.readLux(gain)
        ambient = val[0]
        IR = val[1]
        _ambient = val[2]
        _IR = val[3]
        _LUX = val[4]
        
        # Check Light Sensors Cut-Off
        if (_ambient > LIGHTTHRESHHOLD  or ambient > LIGHTTHRESHHOLD):
            # Check Ultrasonic Sensors Box
            if(t1.mindis == t3.ValidBox):
                if (Light == 1):
                    LIGHT1_VALID = False
                elif (Light == 2):
                    LIGHT2_VALID = False;
                elif (Light == 3):
                    LIGHT3_VALID = False;
            else:
                print("WRONG BOX !! \n\n\n\n\n")


        if (ambient == 0xffff or IR == 0xffff):
            print ("Sensor is saturated, no lux value can be achieved:")
            print ("ambient = " + ambient)
            print ("IR = " + IR)
            print ("light = " + _LUX)
        elif (_ambient == 0):
            print ("It's dark:")
            print ("ambient = " + str(ambient))
            print ("IR = " + str(IR))
            print ("_ambient = " + str(_ambient))
            print ("_IR = " + str(_IR))
            print ("Light = " + str(_LUX) + " lux.")
        else:
            print ("There is light:")
            print ("ambient = " + str(ambient))
            print ("IR = " + str(IR))
            print ("_ambient = " + str(_ambient))
            print ("_IR = " + str(_IR))
            print ("Light = " + str(_LUX) + " lux.")

        time.sleep(2)
        ambient  = None
        IR       = None
        _ambient = 0
        _IR      = 0
        _LUX     = None
        TSL2561._control(_POWER_DOWN)
        StopTime = time.time()
        if(StopTime-StartTime>20):
            break
       
    
# if __name__ == '__main__':
try:
    # Thread for Ultrasonic Sensors
    t1 = BackgroundThreadForUltraSonicSensing()

    # Thread for Motor Movements 
    t2 = BackgroundThreadForMotorMovement()

    # Thread for changing the Block Box Number
    t3 = BackgroundThreadForBoxNumber()

    # Light Sensing 

    x = 0

    while (True):

        print('Minimum Distance from ')
        print(t1.mindis)
        print('\n')

        if (x%3 == 0 and LIGHT1_VALID):
                GPIO.output(Light1,True)
                GPIO.output(Light2,False)
                GPIO.output(Light3,False)
                
                time.sleep(1)
                LightDetectUtility(1)

        elif (x%3 == 1 and LIGHT2_VALID):
                    
            GPIO.output(Light1,False)
            GPIO.output(Light2,True)
            GPIO.output(Light3,False)
            
            time.sleep(1)
            LightDetectUtility(2)

        elif (x%3 == 2 and LIGHT3_VALID):

            GPIO.output(Light1,False)
            GPIO.output(Light2,False)
            GPIO.output(Light3,True)
            
            time.sleep(1)
            LightDetectUtility(3)

        x=x+1

except KeyboardInterrupt:
        print("Stopped by User!")
        GPIO.cleanup()