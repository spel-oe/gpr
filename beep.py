import RPi.GPIO as GPIO
import time

class beep():
    def __init__(self):
        self.running = False
        self.errorstate = False
        self.PIN = 17 
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
    

    def beep(self):
        #for i in range(100):
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(0.200)
        GPIO.output(self.PIN, GPIO.LOW)
        #    time.sleep(0.0005)

    def beep_long(self):

        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.PIN, GPIO.LOW)
        #    time.sleep(0.0005)

    def error(self):
        self.errorstate = True  

    def worker(self):
        while True:
            if (self.running and self.errorstate):
                self.beep_long()
                self.stop
                self.errorstate = False
                print('error state')
            elif (self.running and not self.errorstate):
                self.beep()
                time.sleep(1)
        
    def start(self):
        self.running = True

    def stop(self):
        self.running = False
#laerm = beep()
#laerm.worker()
