import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import numpy as np
import sys
from matplotlib import pyplot as plt

ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

fnames = []
sample_dir = sys.argv[1]
for (dirpath, dirnames, filenames) in os.walk(sample_dir):
	fnames.extend(filenames)
	break

fit_top = 10
vm = 0

# TODO make it so that you can chose directories as well.
## TODO THe dropdown menu does not include the original file
#When multiple of the same file inserted already dd
# Averages

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		
		# Set up the basic window things	
		self.WIDTH = 1000
		self.HEIGHT = 5000
		self.title("Langmuir Probe Analizer")
		self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))

		# This list holds the filenames of the graphs that are displayed.
		self.currently_displayed = []
		
		# Frames 
		self.graph_frame = ctk.CTkFrame() 	# Holds the graph
		self.control_frame = ctk.CTkFrame()	# Holds the controls for manipulating the graphs.
		self.adding_frame = ctk.CTkFrame()	# Holds the controls for adding and removing files from the graph.
		
		# Plots a new graph on the screen	
		self.plot_button = ctk.CTkButton(master = self.adding_frame,
			command = lambda: self.plot(True, False),
			text = "Plot", 
			width = 10)
		self.plus_button = ctk.CTkButton(master = self.control_frame,
			command = self.incr,
			text = "+")
		self.minus_button = ctk.CTkButton(master = self.control_frame,
			command = self.minu,
			text = "-")
		self.deletion_button = ctk.CTkButton(master = self.control_frame,
			command = lambda: self.delete_file(self.file_selector.get()),
	                text = "Delete")
		self.viewmode_button = ctk.CTkButton(master = self.control_frame,
			command = lambda: self.plot(False, True),
			text = "Viewmode")

		# self.fit_counter = ctk.CTkLabel(master = self.control_frame, text = "1")
		self.file_addition_selector = ctk.CTkOptionMenu(master = self.adding_frame, values=fnames)
		self.file_selector = ctk.CTkOptionMenu(master = self.control_frame, values=self.currently_displayed)

		# Put the widgets on the screen
		self.redraw_widgets()
	
	def redraw_widgets(self):
		self.control_frame.grid(row=0,column=1, padx = 10, pady = 10)
		self.graph_frame.grid(row=0, column = 0)
		self.adding_frame.grid(row=1, column = 0)
		self.plot_button.grid(row=0, column=1)
		#self.plus_button.pack()
		#self.minus_button.pack()
		#self.fit_counter.pack()
		self.file_addition_selector.grid(row=0, column=0)
		self.file_selector.pack()
		self.deletion_button.pack()
		self.viewmode_button.pack()
	
	def delete_file(self,f):
		self.currently_displayed.remove(f)
		self.plot(False,False)

	def update(self):
		self.file_selector.pack_forget()
		self.file_selector.__init__(master = self.control_frame, values = self.currently_displayed)
		self.file_selector.pack()

	def incr(self):
		global fit_top
		fit_top += 1
		value = int(fit_counter["text"])
		fit_counter["text"] = f"{value + 1}"

	def minu(self):
		global fit_top
		fit_top -= 1
		value = int(fit_counter["text"])
		fit_counter["text"] = f"{value - 1}"

	def plot(self,b,viewmode_toggle):
		self.graph_frame = ctk.CTkFrame(width = 500, height = 500)
		for widget in self.graph_frame.winfo_children():
			print(widget)
			widget.destroy()
		global vm	 
		
		if viewmode_toggle and vm == 0:
			vm = 1
		elif viewmode_toggle and vm == 1:
			vm = 0
		# the figure that will contain the plot
		fig = Figure(figsize = (10, 10),dpi = 100)
		# adding the subplot
		plot1 = fig.add_subplot(111)
		# TODO
		if b:
			self.currently_displayed.append(self.file_addition_selector.get())
		for fname in self.currently_displayed:
			# Take the data from the file given	
			f = open(sys.argv[1] + "/" + fname, "r")
			vi_data = f.readlines()
			f.close()
			
			# Fix the data into a format usable by the code
			vi_data = vi_data[0]
			vi_data = vi_data.split(",")
			x = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 0])
			y = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 1])
			
			# Fit the Ion Saturation TODO
			m,b = np.polyfit(x[:fit_top],y[:fit_top],1)

		
			if vm == 0:
				plot1.plot(x,y,'o')
			else:
				plot1.plot(x,y)
			# plotting the graph
			#plot1.plot(x,m*x+b)	
			#plot1.plot([x[fit_top]], [y[fit_top]], marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")

		self.canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)
		# creating the Tkinter canvas
		# containing the Matplotlib figur	
		self.canvas.draw()
		# placing the canvas on the Tkinter window
		self.canvas.get_tk_widget().pack()
		# creating the Matplotlib toolbar
		toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		toolbar.update()
		# not working properly
		plot1.legend(self.currently_displayed)
		# placing the toolbar on the Tkinter window
		self.canvas.get_tk_widget().pack()
		self.update()
		self.graph_frame.grid(row=0, column = 0)
	
if __name__ == "__main__":
	app = App()
	app.mainloop()
