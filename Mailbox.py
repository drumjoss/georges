#!/usr/bin/env python

import threading
import time

class MyThread(threading.Thread):
    	"""Thread class with a stop() method. The thread itself has to check
    	regularly for the stopped() condition."""

    	def __init__(self, *args, **kwargs):
        	super(MyThread, self).__init__(*args, **kwargs)
        	self._stop = threading.Event()

    	def stop(self):
        	self._stop.set()

    	def stopped(self):
        	return self._stop.isSet()

class Mailbox:
    	def __init__(self, GeorgesInTheHouse):
        	self.GeorgesInTheHouse = GeorgesInTheHouse
		
    	def EnableMailReceving(self):
        	self.practicethread = MyThread(target=self.MailCheckingLoop)
        	self.practicethread.start()
		
	def DisableMailReceving(self):
        	self.practicethread.stop()

    	def MailCheckingLoop(self):
        	while not self.practicethread.stopped():
            		self.GeorgesInTheHouse.newMailReceived("Mail 1 received !")
			time.sleep(10)
			self.GeorgesInTheHouse.newMailReceived("Mail 2 received !")
			time.sleep(20)



	
