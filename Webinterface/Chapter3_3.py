import cgitb ; cgitb.enable()  
import time
import busio
import digitalio
import board
import requests
from adafruit_bus_device.spi_device import SPIDevice
import adafruit_dht
import RPi.GPIO as GPIO
from tabulate import tabulate
from datetime import datetime
import MySQLdb

LED1 = 17
LED2 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize control pins for adc
cs0 = digitalio.DigitalInOut(board.CE0)  # chip select
adc = SPIDevice(spi, cs0, baudrate= 1000000)

#temperature and humidity
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# read SPI data 8 possible adc's (0 thru 7) 
def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    with adc:
        r = bytearray(3)
        spi.write_readinto([1,(8+adcnum)<<4,0], r)
        time.sleep(0.00005)
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout 

# Initiate the DB
database = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry",db="mydb")

#database select
cursor = database.cursor()

#Input data will be programmed here
try:
    while True:
        try:
            #light sensor
            tmp0 = readadc(0)
            tmp1 = readadc(1)
            light = round((tmp0 / 1023) * 100)
            print(tmp0)
            print(tmp1)
            print("HIGH NOW")
            GPIO.output(LED1,0)
            GPIO.output(LED2,0)
            time.sleep(5)
            print("LOW NOW")
            GPIO.output(LED1,1)
            GPIO.output(LED2,1)
        #temperature and humidity
        #     temperature_c = dhtDevice.temperature
        #     temperature_f = round(temperature_c * (9 / 5) + 32)
        #     humidity = dhtDevice.humidity
        #     #Table with data
        #     time.sleep(1)
        #     print()
        #     print(tabulate([["Amount of light: ",light, "%"],["Temperature in C°: ",temperature_c, "° , C"],["Temperature in Fahrenheit: ",temperature_f, "F"],["Humidity: ",humidity, "%"]], ["What is being displayed", "The amount", "Data type"]))
        #     cursor.execute("INSERT INTO Licht_temp(Temperature, Humidity, Light) VALUES(%s, %s, %s)", (temperature_c, humidity, light))
        #     database.commit()
        # # # Sometimes DHT (temperature and humidity) will run into errors. 
        # # # This will prevent the program from stopping.
        # # # and the program will continue to run afterwards.
        except RuntimeError as error:
            print()
            print("An error has occured: ")
            print(error.args[0])
            print("A new table will be printed soon.")
            print()
            time.sleep(1)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error        
except KeyboardInterrupt:
    #Clean up DB when exiting the python loop
    cursor.execute("DELETE FROM Licht_temp")
    database.commit()
    GPIO.cleanup()
    print()
    print("The program has been interrupted.")
    print("This is the end of the program!")
# At the end you can stop the program with CTL+C
# And it will display an "end of program" message.
    

