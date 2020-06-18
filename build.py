#THE BUILD SCRIPT FOR THE POMODORO CLOCK

#creating classes and methods for the timer

import time

class Timer:

	def __init__(self, name):
		self.name = name

	def set_timer(self, minutes_to_go, seconds_to_go, alert_message):
		self.minutes_to_go = minutes_to_go
		self.seconds_to_go = seconds_to_go
		self.time_to_go = minutes_to_go * 60 + seconds_to_go
		self.alert_message = alert_message

	def set_start_time(self):
		return time.perf_counter()
		
	def get_time_to_go(self):
		self.time_to_go = self.time_to_go % 60 - 1
		if self.time_to_go == -1: 
			self.time_to_go = 59
			if self.minutes_to_go > 0:
				self.minutes_to_go -= 1
			else:
				self.time_to_go = 0
				self.minutes_to_go = 0