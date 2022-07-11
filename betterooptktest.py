import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import numpy as np
import sys
from matplotlib import pyplot as plt
import data_manipulator 

ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

fnames = []
sample_dir = sys.argv[1]
for (dirpath, dirnames, filenames) in os.walk(sample_dir):
	fnames.extend(filenames)
	break

# TODO make it so that you can chose directories as well.
# TODO THe dropdown menu does not include the original file
# When multiple of the same file inserted already dd
# Averages
# for widget in self.graph_frame.winfo_children():
# print(widget)
# widget.destroy()
# fix errors about deleting files when there are none left
# TODO use print ("\a")
# Fit the Ion Saturation TODO
# m,b = np.polyfit(x[:fit_top],y[:fit_top],1)
# plotting the graph
# plot1.plot(x,m*x+b)	
# Graph legend
# Try to update graph without redrawing the whole thing, messing up scales
# Hold data in a map to not reaccesss it every time you regraph, this might be slowing down the code
# Box average manipulation

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		
		# Set up the basic window things	
		self.WIDTH = 1000
		self.HEIGHT = 5000
		self.title("Langmuir Experiment Analyzer Program")
		self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))
		self.img = tk.Image("photo", file="icon.png")
		self.tk.call('wm', 'iconphoto', self._w, self.img)
		self.data_analyzer = data_manipulator.data_manipulator()

		# This list holds the filenames of the graphs that are displayed.
		self.currently_displayed = []
		self.view_mode = 0	
		self.fit_bound = [tk.IntVar(value=0), tk.IntVar(value=0)]
	
		# Frames 
		self.graph_frame = ctk.CTkFrame() 	# Holds the graph
		self.control_frame = ctk.CTkFrame()	# Holds the controls for manipulating the graphs.
		self.adding_frame = ctk.CTkFrame()	# Holds the controls for adding and removing files from the graph.
		self.cursor_frame = ctk.CTkFrame(master = self.control_frame)	
		
		# Plots a new graph on the screen	
		self.plot_button = ctk.CTkButton(master = self.adding_frame,
			command = self.add_new_graph,
			text = "Plot", 
			width = 10)
		self.plus_button = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(1),
			text = ">",
			width = 5)
		self.plus_button_l = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(10),
			text = ">>",
			width = 5)
		self.plus_button_el = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(100),
			text = ">>>",
			width = 5)
		self.minus_button = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(1),
			text = "<",
			width = 5)
		self.minus_button_l = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(10),
			text = "<<",
			width = 5)
		self.minus_button_el = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(100),
			text = "<<<",
			width = 5)
		self.deletion_button = ctk.CTkButton(master = self.control_frame,
			command = lambda: self.delete_file(self.file_selector.get()),
	                text = "Delete")
		self.viewmode_button = ctk.CTkButton(master = self.control_frame,
			command = lambda: self.plot(True),
			text = "Viewmode")

		self.fit_counter = ctk.CTkLabel(master = self.control_frame, textvar = self.fit_bound[0])
		self.file_addition_selector = ctk.CTkOptionMenu(master = self.adding_frame, values=fnames)
		self.file_selector = ctk.CTkOptionMenu(master = self.control_frame, values=self.currently_displayed)

		# Put the widgets on the screen
		self.redraw_widgets()
	
	def redraw_widgets(self):
		self.control_frame.grid(row=0,column=1, padx = 10, pady = 10)
		self.graph_frame.grid(row=0, column = 0)
		self.adding_frame.grid(row=1, column = 0)
		self.plot_button.grid(row=0, column=1)
		self.cursor_frame.pack()
		self.minus_button_el.grid(row=0,column=0)
		self.minus_button_l.grid(row=0,column=1)
		self.minus_button.grid(row=0,column=2)
		self.plus_button.grid(row=0,column=3)
		self.plus_button_l.grid(row=0,column=4)
		self.plus_button_el.grid(row=0,column=5)
		self.fit_counter.pack()
		self.file_addition_selector.grid(row=0, column=0)
		self.file_selector.pack()
		self.deletion_button.pack()
		self.viewmode_button.pack()
	
	def delete_file(self,f):
		self.currently_displayed.remove(f)
		self.plot(False)

	def update(self):
		self.file_selector.pack_forget()
		self.file_selector.__init__(master = self.control_frame, values = self.currently_displayed)
		self.file_selector.pack()

	def incr(self,n):
		self.fit_bound[0].set(self.fit_bound[0].get()+n)		
		self.plot(False)

	def minu(self,n):
		self.fit_bound[0].set(self.fit_bound[0].get()-n)
		self.plot(False)
	
	def vm_toggle(self):	
		if self.view_mode == 0:
			self.view_mode = 1
		elif self.view_mode == 1:
			self.view_mode = 0
	
	def add_new_graph(self):
		self.currently_displayed.append(self.file_addition_selector.get())
		self.plot(False)

	def get_data(self, fname):
		f = open(sys.argv[1] + "/" + fname, "r")
		vi_data = f.readlines()
		f.close()
		
		# Fix the data into a format usable by the code
		vi_data = vi_data[0]
		vi_data = vi_data.split(",")
		x = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 0])
		y = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 1])
		
		return x,y	
	
	def plot(self,viewmode_toggle):
		# Switch the viewmode between point-by-point and connected
		if viewmode_toggle:
			self.vm_toggle()		
	
		# Remake the graph frame. Probably a better way than doing this.	
		self.graph_frame = ctk.CTkFrame(width = 500, height = 500)

		# The figure that will contain the plot and adding the plot
		fig = Figure(figsize = (10, 10), dpi = 100)
		plot1 = fig.add_subplot(111)

		for fname in self.currently_displayed:
			# Take the data from the file given	
			x,y = self.get_data(fname)		

			if self.view_mode == 0:
				plot1.plot(x,y,'o')
			else:
				plot1.plot(x,y)
			
			[xder,yder] = self.data_analyzer.derivative([x,y],1)
			plot1.plot(xder,yder)
		
			plot1.plot([x[self.fit_bound[0].get()]], [y[self.fit_bound[0].get()]], marker="o", markersize=20, markeredgecolor="red") 
		
		self.canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		plot1.legend(self.currently_displayed)
		self.canvas.get_tk_widget().pack()
		self.update()

		self.graph_frame.grid(row=0, column = 0)
	
if __name__ == "__main__":
	app = App()
	app.mainloop()
