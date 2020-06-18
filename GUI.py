#THIS MODULE CREATES THE INTERFACE FOR THE POMODORO CLOCK

from tkinter import *
from build import Timer
import time
import threading

class SetupWindow:
	SHEIGHT = 100
	SWIDTH = 100

	def start_setup(self):
		master = Tk()

		self.minute_entry = Spinbox(master, from_=0, to=500)
		self.minute_entry.grid(row=0, column=0)

		self.second_entry = Spinbox(master, from_=0, to=59)
		self.second_entry.grid(row=0, column=1)

		start_btn = Button(master, text='Start Pomodoro', command=self.start_GUI)
		start_btn.grid(row=1, column=0)

		mainloop()

	def start_GUI(self):
		minutes = int(self.minute_entry.get())
		seconds = int(self.second_entry.get())

		main_gui = GUI(300, 300, minutes, seconds)
		main_gui.build()


class GUI:

	#base constants
	WIN_NAME = "Pomodoro Timer"
	BG_COLOR = "#fffff"
	TEXT_COLOR = '#00000'

	#text
	TITLE_HEIGHT = 0
	TITLE_WIDTH = 0

	TIMER_HEIGHT = 0 
	TIMER_WIDTH = 0
	def __init__(self, height, width, minutes, seconds):
		self.win_height = height
		self.win_width = width
		self.minutes = minutes
		self.seconds = seconds
		self.time_in_sec = minutes * 60 + seconds

		self.timer = Timer("Current")
		self.timer.set_timer(self.minutes, self.seconds, "ALERT")

		self.stopThread = False
		

	def build(self):

		self.start_time = self.timer.set_start_time()

		#root
		root = Tk()
		root.title(GUI.WIN_NAME)
		root.geometry(f'{self.win_height}x{self.win_width}')

		#title text
		clock_text = Label(root, height=GUI.TITLE_HEIGHT, width=GUI.TITLE_WIDTH, text=GUI.WIN_NAME)
		clock_text.grid(row=0, column=0)

		#timer text
		min_text_label = Label(root, height=GUI.TIMER_HEIGHT, width=GUI.TIMER_WIDTH, text=self.timer.minutes_to_go)
		min_text_label.grid(row=1, column=1)

		#timer text
		sec_text_label = Label(root, height=GUI.TIMER_HEIGHT, width=GUI.TIMER_WIDTH, text=self.timer.seconds_to_go)
		sec_text_label.grid(row=1, column=2)

		self.refresh(root, sec_text_label, min_text_label)

		root.mainloop()

		#root.grid_rowconfigure(0, weight=1)
		#root.grid_columnconfigure(0, weight=1)

	def refresh(self, root, sec_text_label, min_text_label):
		self.timer.get_time_to_go()
		if self.timer.time_to_go == 0 and self.timer.minutes_to_go == 0:
			self.alert_and_stop(root)
		sec_text_label.configure(text=str(self.timer.time_to_go))
		min_text_label.configure(text=str(self.timer.minutes_to_go))
		t1 = threading.Timer(1, self.refresh, args=(root, sec_text_label, min_text_label))
		if self.stopThread: t1.cancel()
		t1.start()

	def alert_and_stop(self, root):
		root.withdraw()
		messageBox = Tk()
		messageBox.title("Time for a break :)")
		alert = Label(messageBox, text=self.timer.alert_message,)
		alert.config(font=('Courier', 40))
		alert.grid(row=0, column=0)
		messageBox.mainloop()
		self.stopThread = True