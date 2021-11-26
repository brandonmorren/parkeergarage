#!/usr/bin/env python
import http.client, urllib
import RPi.GPIO as GPIO 
import cgitb ; cgitb.enable() 
import spidev 
import time 
import sys 
from simplepush import send
from urllib import request, parse 

while True:
    data = parse.urlencode({'key': 'qe4awa', 'title': 'title', 'msg': 'encrypted massage', 'event': 'event1'}).encode()
    req = request.Request("https://api.simplepush.io/send", data=data)
    request.urlopen(req)
    time.sleep(1) 





