__auther__ = 'chenyiqun'

import RPi.GPIO as GPIO


class CarDrive(object):
    
    def __init__(self):
       
        GPIO.setwarnings(False) #取消警告
 
        #轮子连接的引脚
        self.__leftPin1 = 19
        self.__leftPin2 = 13
        self.__rightPin1 = 6
        self.__rightPin2 = 5
        self.__leftPWMPin = 22
        self.__rightPWMPin = 27

        self.__turnPWMPin = 18 #舵机PWM引脚

        #引脚设置为BCM和输出模式
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__leftPin1, GPIO.OUT)
        GPIO.setup(self.__leftPin2, GPIO.OUT)
        GPIO.setup(self.__rightPin1, GPIO.OUT)
        GPIO.setup(self.__rightPin2, GPIO.OUT)
        GPIO.setup(self.__leftPWMPin, GPIO.OUT)
        GPIO.setup(self.__rightPWMPin, GPIO.OUT)
        GPIO.setup(self.__turnPWMPin, GPIO.OUT)
        
        #制动驱动轮
        self.stop()

        self.PWMFreq = 50 #设置PWM的频率(Hz) 

        #舵机不同转向下不同占空比(%)
        self.middleDuty = 6.1  
        self.leftDuty = 3.5 
        self.rightDuty = 9.2
        
        self.leftSpeedDuty = 25 #驱动轮转速的占空比(%)
        self.rightSpeedDuty = 17 #驱动轮转速的占空比(%)

        #PWM的初始化
        self.leftPWM = GPIO.PWM(self.__leftPWMPin, self.PWMFreq)
        self.leftPWM.start(self.leftSpeedDuty)
        self.rightPWM = GPIO.PWM(self.__rightPWMPin, self.PWMFreq)
        self.rightPWM.start(self.rightSpeedDuty)
        self.turnPWM = GPIO.PWM(self.__turnPWMPin, self.PWMFreq)
        self.turnPWM.start(self.middleDuty)

    def forward(self):
        '''
        小车的前进
        '''
        GPIO.output(self.__leftPin1, GPIO.HIGH)
        GPIO.output(self.__leftPin2, GPIO.LOW)
    
        GPIO.output(self.__rightPin1, GPIO.HIGH)
        GPIO.output(self.__rightPin2, GPIO.LOW)
    
 
    def backward(self):
        '''
        小车的后退
        '''
        GPIO.output(self.__leftPin1, GPIO.LOW)
        GPIO.output(self.__leftPin2, GPIO.HIGH)
    
        GPIO.output(self.__rightPin1, GPIO.LOW)
        GPIO.output(self.__rightPin2, GPIO.HIGH)

    
    def stop(self):
        '''
        小车停止
        '''
        GPIO.output(self.__leftPin1, GPIO.LOW)
        GPIO.output(self.__leftPin2, GPIO.LOW)
    
        GPIO.output(self.__rightPin1, GPIO.LOW)
        GPIO.output(self.__rightPin2, GPIO.LOW)
    
        
    def left(self): 
        '''
        左转向
        '''
        self.turnPWM.ChangeDutyCycle(self.leftDuty)


    def right(self): 
        '''
        右转向
        '''
        self.turnPWM.ChangeDutyCycle(self.rightDuty)


    def middle(self): 
        '''
        中间转向
        '''
        self.turnPWM.ChangeDutyCycle(self.middleDuty)




