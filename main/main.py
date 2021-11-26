#https://stackoverflow.com/questions/52029233/how-to-make-usb-camera-work-with-opencv
#https://maker.pro/raspberry-pi/tutorial/optical-character-recognizer-using-raspberry-pi-with-opencv-and-tesseract

# de nodige libraries importeren
import RPi.GPIO as GPIO
import time
import cv2
import pytesseract
import imutils
import numpy as np
from PIL import Image
import MySQLdb
from datetime import datetime

#initialize database variable
nummerplaat = 0

#verbinden met database
database = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="parkeergarage")

#database select
cursor = database.cursor()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)# pin1 voor ultrasoon sensor ingang
GPIO.setup(27, GPIO.IN)# pin2 voor ultrasoon sensor ingang
GPIO.setup(14, GPIO.OUT)# pin1 voor ultrasoon sensor uitgang
GPIO.setup(15, GPIO.IN)# pin2 voor ultrasoon sensor uitgang
GPIO.setup(18, GPIO.OUT)# led voor parking vol
GPIO.setup(5, GPIO.OUT)# pin voor slagboom motor



# slagboom motor instellen
servo = GPIO.PWM(5, 50)
servo.start(2.5)

servo.ChangeDutyCycle(11)# slagboom dicht zetten

legeparkings = 4 # lege parkings bijhouden
ticketbetaald = 1 # is het parkingticket betaald -> 1


#variabelen
parking1Vol = 0
parking2Vol = 0
parking3Vol = 0
parking4Vol = 0
afstandauto = 15



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

# nummerplaat scannen
# camera nummerplaat herkenning instellen
cam = cv2.VideoCapture(0)

def scanNummerplaat():  
    #while loop om scannen evt te herhalen
    i = 0
    while i < 1:
        #camera inlezen
        ret,frame=cam.read()
        time.sleep(0.5)
        img=frame
        
        #foto nummerplaat vorm herkennnen
        img = cv2.resize(img, (600,400) )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray, 13, 15, 15) 

        edged = cv2.Canny(gray, 30, 200) 
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in contours:
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        
            if len(approx) == 4:
                screenCnt = approx
                break

        #als er geen nummerplaat is herkent
        if screenCnt is None:
            detected = 0
            print ('No contour detected')
        else:
            detected = 1

        #nummerplaatcontouren tekeken
        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        #tekst van nummerplaat herkennen
        text = pytesseract.image_to_string(Cropped, config='--psm 11')
        print ('License Plate Recognition\n')
        print('Detected license plate Number is:',text,'\n')
        img = cv2.resize(img,(500,300))
        Cropped = cv2.resize(Cropped,(400,200))
        #foto's tonen om te debuggen:
        #cv2.imshow('car',img)
        #cv2.imshow('Cropped',Cropped)
        
        #foto schrijven naar opslag met tijdstip in de naam
        img_name = 'numberplate_image_{}.png'.format(tijdstip)
        cv2.imwrite(img_name, frame)
        
        time.sleep(2)
        i=i+1
    return text
    
try:
    while True:
        #[BUG] alles moet op de pi aangesloten zijn, anders hangt het programma vast bij if(meetAfstand("ingang") < afstandauto):
        #[BUG] kan de nummerplaat waarde niet in de terminal tonen.
        
        #ingang parking
        if(meetAfstand("ingang") < afstandauto):# er staat auto ingang
            if(legeparkings > 0):# er is een plaats vrij
                tijdstip=datetime.now()
                
                #scan nummerplaat
                nummerplaat=scanNummerplaat()
                
                #wegscrhijven naar db
                cursor.execute("INSERT INTO nrplaat(tijdstip,nummerplaat) VALUE(%s, %s)", (tijdstip,nummerplaat))
                database.commit()
                print('nummerplaat is doorgestuurt naar database, [BUG] kan de nummerplaat waarde niet in de terminal tonen\n')

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
        if(meetAfstand("uitgang") < afstandauto):# auto aan uitgang
            print(scanNummerplaat())# nummerplaat scannen
            if(ticketbetaald == 1):# hij heeft betaald
                servo.ChangeDutyCycle(6.5)# slagboom open
                print('slagboom open')
                while (meetAfstand("uitgang") < afstandauto or meetAfstand("ingang") < afstandauto):# staat de auto er nog ?
                    time.sleep(4)
                servo.ChangeDutyCycle(11)# auto weg -> slagboom dicht
                print('slagboom dicht')
                if(legeparkings < 4):
                    legeparkings += 1# auto naar buiten -> parkings vrij +1
            else:# NIET betaald
                print('Gelieve eerst te betalen en dan naar buiten te rijden.')

        # if(parking1Vol == 1):
            
        # else:
            
        # if(parking2Vol == 1):
            
        # else:
            
        # if(parking3Vol == 1):
            
        # else:
            
        # if(parking4Vol == 1):
            
        # else:
            
        time.sleep(1)
        
except KeyboardInterrupt:# stop programma -> proper afsluiten
    
    servo.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()