#THIS MODULE CREATES THE INTERFACE FOR THE POMODORO CLOCK

from tkinter import *
from build import Timer
import time
import threading

class SetupWindow:
	SHEIGHT = 250
	SWIDTH = 500
	BG_COLOR_SETUP = "#71d96a"

	def start_setup(self):

		#button hover functions
		def enter(e):
			start_btn["background"] = "#b3f0af"
		def leave(e):
			start_btn["background"] = "#ffffff"


		master = Tk()
		master.geometry(f"{SetupWindow.SWIDTH}x{SetupWindow.SHEIGHT}")
		master.maxsize(700, 350)
		master.title("Setup your Pomodoro Clock")
		master.config(bg=SetupWindow.BG_COLOR_SETUP)

		frame = Frame(master, bg=SetupWindow.BG_COLOR_SETUP)
		frame.grid(row=0, column=0)

		minute_label = Label(frame, text="minutes", font=("Roboto Slab", 10), bg="#71d96a",
			fg="#ffffff")
		minute_label.grid(row=0, column=0, sticky=S, pady=(20, 10))
		self.minute_entry = Spinbox(frame, from_=0, to=500, font=("Roboto Extra Bold", 15))
		self.minute_entry.grid(row=1, column=0, ipady=10)

		seconds_label = Label(frame, text="seconds", font=("Roboto Slab", 10), bg="#71d96a",
			fg="#ffffff")
		seconds_label.grid(row=2, column=0, sticky=S, pady=10)
		self.second_entry = Spinbox(frame, from_=0, to=59, font=("Roboto Extra Bold", 15))
		self.second_entry.grid(row=3, column=0, ipady=10)

		start_btn = Button(frame, text='Start Pomodoro', command=self.start_GUI, font=("Roboto Slab Extra", 10)
			,bg="#ffffff", borderwidth=0)
		start_btn.grid(row=4, column=0, pady=30, ipady=10)
		start_btn.bind("<Enter>", enter)
		start_btn.bind("<Leave>", leave)

		master.grid_rowconfigure(0, weight=1)
		master.grid_columnconfigure(0, weight=1)

		rows_setup = [0, 1, 2, 3, 4]
		frame.grid_rowconfigure(rows_setup, weight=2)
		frame.grid_columnconfigure(0, weight=2)

		mainloop()

	def start_GUI(self):
		minutes = int(self.minute_entry.get())
		seconds = int(self.second_entry.get())

		main_gui = GUI(450, 700, minutes, seconds)
		main_gui.build()


class GUI:

	#base constants
	WIN_NAME = "Pomodoro Timer"
	BG_COLOR = "#71d96a" #green: "#71d96a" blue: #1b3863

	
	def __init__(self, height, width, minutes, seconds):
		self.win_height = height
		self.win_width = width
		self.minutes = minutes
		self.seconds = seconds
		self.time_in_sec = minutes * 60 + seconds

		self.timer = Timer("Current")
		self.timer.set_timer(self.minutes, self.seconds, "It's time\nfor a break!")

		self.stopThread = False
		

	def build(self):

		self.start_time = self.timer.set_start_time()

		#root
		root = Tk()
		root.title(GUI.WIN_NAME)
		root.geometry(f'{self.win_width}x{self.win_height}')
		root.config(bg=SetupWindow.BG_COLOR_SETUP)

		main_frame = Frame(root, bg=SetupWindow.BG_COLOR_SETUP)
		main_frame.grid(row=1, column=0,)

		#title text
		clock_text = Label(root, font=("Roboto Extra Bold", 30), text=GUI.WIN_NAME,
			bg=SetupWindow.BG_COLOR_SETUP, fg="#ffffff")
		clock_text.grid(row=0, column=0, pady=(60, 0))

		#timer text
		min_text_label = Label(main_frame, text=self.timer.minutes_to_go, 
			font=("Roboto Slab", 90), bg=SetupWindow.BG_COLOR_SETUP, fg="#ffffff")
		min_text_label.grid(row=0, column=0, pady=(40, 100), ipadx=30)

		#timer text
		sec_text_label = Label(main_frame, text=self.timer.seconds_to_go, 
			font=("Roboto Slab", 90), bg=SetupWindow.BG_COLOR_SETUP, fg="#ffffff")
		sec_text_label.grid(row=0, column=1, pady=(40, 100), ipadx=30)

		self.refresh(main_frame, sec_text_label, min_text_label, root)

		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)

		main_frame_cols = [0, 1]
		main_frame.grid_rowconfigure(0, weight=2)
		main_frame.grid_columnconfigure(main_frame_cols, weight=2)

		root.mainloop()

	def refresh(self, root, sec_text_label, min_text_label, main_root):
		self.timer.get_time_to_go()
		if self.timer.time_to_go == 0 and self.timer.minutes_to_go == 0:
			self.alert_and_stop(main_root)
		sec_text_label.configure(text=str(self.timer.time_to_go))
		min_text_label.configure(text=(str(self.timer.minutes_to_go), ":"))
		t1 = threading.Timer(1, self.refresh, args=(root, sec_text_label, min_text_label, main_root))
		if self.stopThread: t1.cancel()
		t1.start()

	def alert_and_stop(self, main_root):
		main_root.withdraw()
		messageBox = Tk()
		messageBox.title("Time for a break")
		messageBox.geometry("500x250")
		messageBox.config(bg=SetupWindow.BG_COLOR_SETUP)
		alert = Label(messageBox, text=self.timer.alert_message, bg=SetupWindow.BG_COLOR_SETUP,
			fg="#ffffff")
		alert.config(font=('Roboto Slab', 25))
		alert.grid(row=0, column=0)

		messageBox.grid_rowconfigure(0, weight=1)
		messageBox.grid_columnconfigure(0, weight=1)

		messageBox.lift()
		messageBox.attributes('-topmost',True)
		messageBox.after_idle(messageBox.attributes,'-topmost',False)

		messageBox.mainloop()
		self.stopThread = True