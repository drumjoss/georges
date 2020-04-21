#!/usr/bin/env python

import time
import signal
import sys

import Speaker
import Scroller
import Georges
import Mailbox
import Alarm
import Calendar
import Button
import MusicLibrary


def signal_term_handler(signal, frame):
    	GCalendar.DisableCalendarChecking()
    	AlarmClock.DisableAlarms()
    	sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

if __name__ == "__main__":
	pHatScroller = Scroller.Scroller()
	xMini = Speaker.Speaker(pHatScroller)
	myMusicLibrary = MusicLibrary.MusicLibrary()
	GeorgesStephenson = Georges.Georges(xMini , pHatScroller, myMusicLibrary)
	GreenButton = Button.Button(GeorgesStephenson)
	AlarmClock = Alarm.Alarm(GeorgesStephenson)
	AlarmClock.EnableAlarms()
	GCalendar = Calendar.Calendar(AlarmClock)
	GCalendar.EnableCalendarChecking()
	try:
		while(1):
			print("House Standing")
			time.sleep(3600)
	except KeyboardInterrupt:
		GCalendar.DisableCalendarChecking()
		AlarmClock.DisableAlarms()
		sys.exit(-1)


	
	
