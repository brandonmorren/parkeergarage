#!/usr/bin/env python3 
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Initialize display
dc = digitalio.DigitalInOut(board.D23)  # data/command
cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
reset = digitalio.DigitalInOut(board.D24)  # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
display.bias = 4
display.contrast = 60
display.invert = True
#  Clear the display.  Always call show after changing pixels to make the display update visible!
display.fill(0)
display.show()
# Load default font.
font = ImageFont.load_default()

parking1Vol = 1
parking2Vol = 0
parking3Vol = 0
parking4Vol = 0

while True:
    image = Image.new('1', (display.width, display.height)) 
    draw = ImageDraw.Draw(image)
    
    # Draw a white filled box to clear the image.
    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
    # Write some text.
    nummer=4
    draw.text((1,0), 'Welkom', font=font)
    if(parking1Vol == 0):
        draw.text((1,8), 'P1: vrij', font=font)
    else:
        nummerplaat = '1-ABC-123'
        draw.text((1,8), 'P1: '+str(nummerplaat), font=font)
    if(parking2Vol == 0):
        draw.text((1,16), 'P2: vrij', font=font)
    else:
        nummerplaat = '1-ABC-123'
        draw.text((1,16), 'P2: '+str(nummerplaat), font=font)
    if(parking3Vol == 0):
        draw.text((1,24), 'P3: vrij', font=font)
    else:
        nummerplaat = '1-ABC-123'
        draw.text((1,24), 'P3: '+str(nummerplaat), font=font)
    if(parking4Vol == 0):
        draw.text((1,32), 'P4: vrij', font=font)
    else:
        nummerplaat = '1-ABC-123'
        draw.text((1,32), 'P4: '+str(nummerplaat), font=font)
    display.image(image)
    display.show()
    time.sleep(1)
