# de nodige libraries importeren
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)# pin1 voor ultrasoon sensor ingang
GPIO.setup(27, GPIO.IN)# pin2 voor ultrasoon sensor ingang
GPIO.setup(14, GPIO.OUT)# pin1 voor ultrasoon sensor uitgang
GPIO.setup(15, GPIO.IN)# pin2 voor ultrasoon sensor uitgang
GPIO.setup(23, GPIO.OUT)# led voor parking 1 bezet 
GPIO.setup(24, GPIO.OUT)# led voor parking 2 bezet 
GPIO.setup(25, GPIO.OUT)# led voor parking 3 bezet 
GPIO.setup(16, GPIO.OUT)# led voor parking 4 bezet 
GPIO.setup(18, GPIO.OUT)# led voor parking vol
GPIO.setup(5, GPIO.OUT)# pin voor slagboom motor

# slagboom motor instellen
servo = GPIO.PWM(5, 50)
servo.start(2.5)

servo.ChangeDutyCycle(11)# slagboom dicht zetten

legeparkings = 4 # lege parkings bijhouden
ticketbetaald = 1 # is het parkingticket betaald -> 1

parking1Vol = 0
parking2Vol = 0
parking3Vol = 0
parking4Vol = 0

#afstand meten 
def meetAfstand(inOfUitgang):
    if(inOfUitgang == "ingang"):
        pinInput = 27
        pinOutput = 17
    if(inOfUitgang == "uitgang"):
        pinInput = 15
        pinOutput = 14
    GPIO.output(pinOutput, 1)
    time.sleep(0.000001)
    GPIO.output(pinOutput, 0)
    while(GPIO.input(pinInput) == 0):
        pass
    starttime = time.time()
    while(GPIO.input(pinInput) == 1):
        pass
    endtime = time.time()
    return round(((endtime - starttime)*17000),0)

try:
    while True:
        #ingang parking
        if(meetAfstand("ingang") < 10):# er staat auto ingang  
            if(legeparkings > 0):# er is een plaats vrij
                servo.ChangeDutyCycle(6.5)# slagboom open
                print('slagboom open')
                while (meetAfstand("ingang") < 10 or meetAfstand("uitgang") < 10):# staat de auto er nog ?
                    time.sleep(4)
                servo.ChangeDutyCycle(11)# auto weg -> slagboom dicht
                print('slagboom dicht')
                legeparkings -= 1# auto naar binnen -> parkings vrij -1
            else:# GEEN plaats
                GPIO.output(18, 1)# led aan
                while (meetAfstand("ingang") < 10):# staat de auto er nog ?
                    time.sleep(1)
                GPIO.output(18, 0)# auto weg -> led uit
        
        #uitgang parking
        if(meetAfstand("uitgang") < 10):# auto aan uitgang
            if(ticketbetaald == 1):# hij heeft betaald
                servo.ChangeDutyCycle(6.5)# slagboom open
                print('slagboom open')
                while (meetAfstand("uitgang") < 10 or meetAfstand("ingang") < 10):# staat de auto er nog ?
                    time.sleep(4)
                servo.ChangeDutyCycle(11)# auto weg -> slagboom dicht
                print('slagboom dicht')
                if(legeparkings < 4):
                    legeparkings += 1# auto naar buiten -> parkings vrij +1
            else:# NIET betaald
                print('Gelieve eerst te betalen en dan naar buiten te rijden.')

        if(parking1Vol == 1):
            GPIO.output(23, 1)
        else:
            GPIO.output(23, 0)
        if(parking2Vol == 1):
            GPIO.output(24, 1)
        else:
            GPIO.output(24, 0)
        if(parking3Vol == 1):
            GPIO.output(25, 1)
        else:
            GPIO.output(25, 0)
        if(parking4Vol == 1):
            GPIO.output(16, 1)
        else:
            GPIO.output(16, 0)
        time.sleep(1)
        
except KeyboardInterrupt:# stop programma -> proper afsluiten
  servo.stop()
  GPIO.cleanup()