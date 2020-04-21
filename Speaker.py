#!/usr/bin/env python

import os
import sys
import wave
import alsaaudio as aa
from struct import unpack
import numpy as np
import threading
import time
import RPi.GPIO as GPIO

import Scroller

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

class Speaker:
	def __init__(self, SpeakerScroller):
		self.SpeakerScroller = SpeakerScroller
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)

	def playSong(self, audioFileString):
		GPIO.output(17, GPIO.LOW)
		self.practicethread = MyThread(target=self.SongPlaybackLoop)
		self.wavfile = wave.open(audioFileString, 'r')
		self.sample_rate = self.wavfile.getframerate()
		no_channels = self.wavfile.getnchannels()
		self.chunk = 4096

		self.output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
		self.output.setchannels(no_channels)
		self.output.setrate(self.sample_rate)
		self.output.setformat(aa.PCM_FORMAT_S16_LE)
		self.output.setperiodsize(self.chunk)

		self.mix = aa.Mixer('Software')
		self.mix.setvolume(65)

		self.matrix    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		power     = []
		self.weighting = [1, 1, 2, 4, 8, 8, 8, 8, 16, 16, 16]
		self.data = self.wavfile.readframes(self.chunk)
        	self.practicethread.start()

	def power_index(self, val):
		return int(2 * self.chunk * val / self.sample_rate)

	def compute_fft(self, data, chunk, sample_rate):
		self.data = unpack("%dh" % (len(self.data) / 2), self.data)
		self.data = np.array(self.data, dtype='h')

		fourier = np.fft.rfft(self.data)
		fourier = np.delete(fourier, len(fourier) - 1)

		power = np.abs(fourier)
		self.matrix[0] = int(np.mean(power[self.power_index(0)    :self.power_index(156) :1]) )
		self.matrix[1] = int(np.mean(power[self.power_index(156)  :self.power_index(313) :1]) )
		self.matrix[2] = int(np.mean(power[self.power_index(313)  :self.power_index(625) :1]) )
		self.matrix[3] = int(np.mean(power[self.power_index(625)  :self.power_index(1000) :1]))
		self.matrix[4] = int(np.mean(power[self.power_index(1000) :self.power_index(2000) :1]))
		self.matrix[5] = int(np.mean(power[self.power_index(2000) :self.power_index(3000) :1]))
		self.matrix[6] = int(np.mean(power[self.power_index(3000) :self.power_index(4000) :1]))
		self.matrix[7] = int(np.mean(power[self.power_index(4000) :self.power_index(5000) :1]))
		self.matrix[8] = int(np.mean(power[self.power_index(5000) :self.power_index(6000) :1]))
		self.matrix[9] = int(np.mean(power[self.power_index(6000) :self.power_index(7000) :1]))
		self.matrix[10] = int(np.mean(power[self.power_index(7000):self.power_index(8000) :1]))

		self.matrix = np.divide(np.multiply(self.matrix, self.weighting), 100000)
		self.matrix = self.matrix.clip(0, 5)
		self.matrix = [float(m) for m in self.matrix]

	def Stop(self):
        	self.practicethread.stop()
		self.mix.setvolume(0)
		self.matrix    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.SpeakerScroller.DisplayGraph(self.matrix, 0, 5)
		GPIO.output(17, GPIO.HIGH)

	def SongPlaybackLoop(self):
        	while not self.practicethread.stopped() and (len(self.data) % 4096) == 0: #Some wav files may provide truncated final chunk: Check size is modulo 4096
			self.output.write(self.data)
			self.compute_fft(self.data, self.chunk, self.sample_rate)
			self.SpeakerScroller.DisplayGraph(self.matrix, 0, 5)
			self.data = self.wavfile.readframes(self.chunk)
		self.mix.setvolume(0)
		self.matrix    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.SpeakerScroller.DisplayGraph(self.matrix, 0, 5)

if __name__ == "__main__":
	Scrolly = Scroller.Scroller()
	xMini = Speaker(Scrolly)
	xMini.playSong("Hi.wav")
