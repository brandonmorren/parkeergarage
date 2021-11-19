import RPi.GPIO as GPIO
import time


LDR1 = 6
LDR2 = 5
LDR3 = 13
LDR4 = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR1, GPIO.IN)
GPIO.setup(LDR2, GPIO.IN)
GPIO.setup(LDR3, GPIO.IN)
GPIO.setup(LDR4, GPIO.IN)



try:
    while True:
        if (GPIO.input(LDR1)==0):
            print("LDR1: Dark")
            time.sleep(0.5)
        else:
            print("LDR1: Light")
            time.sleep(0.5)
        
        if (GPIO.input(LDR2)==0):
            print("LDR2: Dark")
            time.sleep(0.5)
        else:
            print("LDR2: Light")
            time.sleep(0.5)

        if (GPIO.input(LDR3)==0):
            print("LDR3: Dark")
            time.sleep(0.5)
        else:
            print("LDR3: Light")
            time.sleep(0.5)    

        if (GPIO.input(LDR4)==0):
            print("LDR4: Dark")
            time.sleep(0.5)
        else:
            print("LDR4: Light")
            time.sleep(0.5)            


except:
    KeyboardInterrupt
    GPIO.cleanup()

print("")
print("program executed")

# 