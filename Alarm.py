import os

import datetime
import dateutil.parser
import pytz
import threading
import time

def main():
    print('Nothing to do')


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

class Alarm:
    	def __init__(self, GeorgesInTheHouse):
        	self.GeorgesInTheHouse = GeorgesInTheHouse
		self.AlarmsList = []
				
	def EnableAlarms(self):
		self.practicethread = MyThread(target=self.AlarmsLoop)
		self.practicethread.start()
			
	def DisableAlarms(self):
		self.practicethread.stop()
		
	def SetAlarm(self, time):
		if self.AlarmsList.count(time) == 0:
			self.AlarmsList.append(time)
			
	def AlarmsLoop(self):
		while not self.practicethread.stopped():
			now = datetime.datetime.now(pytz.utc)			

			for Alarm in self.AlarmsList:
				delta = Alarm - now + datetime.timedelta(minutes=1)
				if delta.days == 0: # Check only today's events 
					if delta.seconds <= 100 :
						print(Alarm)
						self.GeorgesInTheHouse.incomingEvent()
						self.AlarmsList.remove(Alarm)
			time.sleep(50) # Check every 50 seconds

if __name__ == '__main__':
    main()
