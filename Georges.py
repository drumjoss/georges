#!/usr/bin/env python

import Speaker
import Scroller
import MusicLibrary 

import time

class Georges:
	def __init__(self, GeorgesSpeaker, GeorgesScroller, GeorgesMusicLibrary):
		print("Hello, I'm Georges")
		self.GeorgesSpeaker = GeorgesSpeaker
		self.GeorgesScroller = GeorgesScroller
		self.GeorgesMusicLibrary = GeorgesMusicLibrary  
		self.Ringing = False

	def newMailReceived(self, body):
		self.GeorgesSpeaker.playSong("fart.wav")
		self.GeorgesScroller.Display(body, 3)
	
	def incomingEvent(self):
		self.Ringing = True
		while self.Ringing:
			self.GeorgesSpeaker.playSong(self.GeorgesMusicLibrary.pickUpSong())
			time.sleep(60)
	
	def buttonPressed(self):
		self.Ringing = False
		self.GeorgesSpeaker.Stop()
	
if __name__ == "__main__":
	pHatScroller = Scroller.Scroller()
	xMini = Speaker.Speaker(pHatScroller)
	GeorgesStephenson = Georges(xMini , pHatScroller)
	GeorgesStephenson.GeorgesSpeaker.playSong("fart.wav")
	GeorgesStephenson.GeorgesScroller.Display("sry!", 2)

