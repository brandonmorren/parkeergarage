import RPi.GPIO as GPIO
import time

servoPIN = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
p.ChangeDutyCycle(11)
try:
  while True:
    time.sleep(5)
    p.ChangeDutyCycle(6.5)
    time.sleep(5)
    p.ChangeDutyCycle(11)
    # for i in range(6, 12):
    #     p.ChangeDutyCycle(i)
    #     time.sleep(0.5)
    
    # time.sleep(1)
    # p.ChangeDutyCycle(10)
    # time.sleep(1)
    # p.ChangeDutyCycle(7.5)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(10)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(12.5)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(10)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(7.5)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(5)
    # time.sleep(0.5)
    # p.ChangeDutyCycle(2.5)
    # time.sleep(0.5)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()