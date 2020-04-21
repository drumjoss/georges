#!/usr/bin/env python2.7  
# script by Alex Eames http://RasPi.tv  
  
import RPi.GPIO as GPIO  
import time

class Button:
    	def __init__(self, GeorgesInTheHouse):
        	self.GeorgesInTheHouse = GeorgesInTheHouse
		GPIO.setmode(GPIO.BCM)  
		GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
		self.time_stamp = time.time() 
		GPIO.add_event_detect(23, GPIO.RISING, callback=self.ButtonPressed) 
				
	def ButtonPressed(self, channel):
    		time_now = time.time()  
    		if (time_now - self.time_stamp) >= 0.3:  
	 		self.GeorgesInTheHouse.buttonPressed()
    		self.time_stamp = time_now  