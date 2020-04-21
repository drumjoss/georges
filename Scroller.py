#!/usr/bin/env python

import sys
import time

import scrollphat

class Scroller:
	def __init__(self):
        	scrollphat.set_brightness(95)

	def Display(self, string, times):
		scrollphat.write_string(string, 11)
		length = (scrollphat.buffer_len())*times
		for i in range(length):
			try:
				scrollphat.scroll()
				time.sleep(0.1)
			except KeyboardInterrupt:
				scrollphat.clear()
				sys.exit(-1)

	def DisplayGraph(self, matrix, low, high):
		scrollphat.graph(matrix, low, high)

if __name__ == "__main__":
	pHatScroller = Scroller()
	pHatScroller.Display("Yo pelz !", 4)
	
