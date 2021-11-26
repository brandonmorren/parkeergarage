#!/usr/bin/env python
import http.client, urllib
import RPi.GPIO as GPIO 
import cgitb ; cgitb.enable() 
import time

while True:
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": "a51moxw5zs6d624p87rzmccu1nbjg3",
        "user": "ugje37ew2vnuun8bfbsauoheduyui8",
        "message": "Parking vol",
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    time.sleep(2)







 

    

