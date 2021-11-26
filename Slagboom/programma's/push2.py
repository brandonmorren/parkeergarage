#!/usr/bin/env python
import http.client, urllib
import RPi.GPIO as GPIO 
import cgitb ; cgitb.enable() 
import spidev 
import time 
import sys 
from simplepush import send
while True:
    send('qe4awa','event1','hello','event1')
    time.sleep(1) 



