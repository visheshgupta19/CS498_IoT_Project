import RPi.GPIO as GPIO
import time

class Feeder():
    def __init__(self):
        # Set GPIO number mode
        GPIO.setmode(GPIO.BOARD)
        # Set pin 11 as output, and set servo as pin 11 as PWM
        GPIO.setup(11, GPIO.OUT)
        self.servo = GPIO.PWM(11, 50)
        self.servo.start(0)
        time.sleep(0.7)
        self.servo.ChangeDutyCycle(0.0)
        time.sleep(0.7)

    def set_from(self, a, b):
        time.sleep(1.0)
        while a != b:
            if a < b: a += 5
            else: a -= 5
            self.servo.ChangeDutyCycle(a)
            time.sleep(0.3)
            self.servo.ChangeDutyCycle(0)
            time.sleep(0.7)
    
    def run(self):
        self.set_from(7, 2)
        self.set_from(2, 12)
        self.set_from(12, 7)
    
    def cleanup(self): 
        self.servo.stop()
        GPIO.cleanup()

