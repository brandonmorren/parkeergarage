import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

while True:
    GPIO.output(17, 1)
    time.sleep(0.000001)
    GPIO.output(17, 0)
    while(GPIO.input(27) == 0):
        pass
    localtime = time.time()
    starttime = localtime
    while(GPIO.input(27) == 1):
        pass
    localtime = time.time()
    endtime = localtime
    tijd = endtime - starttime
    distance = tijd*17000
    afstand = round(distance,0)
    if(afstand < 10):
        print('auto')
    else:
        print('geen auto')
    time.sleep(2)