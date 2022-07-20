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

# TODO plt.style.use('dark_background')

fnames = []
sample_dir = sys.argv[1]
for (dirpath, dirnames, filenames) in os.walk(sample_dir):
	fnames.extend(filenames)
	break

# TODO make it so that you can chose directories as well.
# Averages
# Try to update graph without redrawing the whole thing, messing up scales
# Derivatives or other manipulations don't show up
# Place select all button nicer
# Maybe try making it write to a csv file.
# multiple labels in the selector frame are made for adding the same thing
# vfloat 
# vspace
# xi: = probe radius/ debye length
# formula for debye using epsilong * KT/ne^2


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		
		# Set up the basic window things	
		self.WIDTH = 1400
		self.HEIGHT = 5000
		self.title("Langmuir Experiment Analyzer Program")
		self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))
		self.img = tk.Image("photo", file="icon.png")
		self.tk.call('wm', 'iconphoto', self._w, self.img)
		self.data_analyzer = data_manipulator.data_manipulator()

		# This list holds the filenames of the graphs that are displayed, along with their data
		self.currently_displayed = {}
		self.selector_display = {}
		self.view_mode = 0	
		self.lin_log = 0
		self.select_all = tk.IntVar()
		self.legend_visibility = True
		self.fit_bound = [tk.IntVar(value=0), tk.IntVar(value=0)]
	
		# Frames 
		self.left_frame = ctk.CTkFrame()
		self.right_frame = ctk.CTkFrame()

		self.graph_frame = ctk.CTkFrame(master = self.left_frame) 	# Holds the graph
		self.adding_frame = ctk.CTkFrame(master = self.left_frame)	# Holds the controls for adding and removing files from the graph.


		self.control_frame = ctk.CTkFrame(master = self.right_frame)	# Holds the controls for manipulating the graphs.
		self.selector_frame = ctk.CTkFrame(master = self.right_frame)	
	
		self.options_frame = ctk.CTkFrame(master = self.control_frame)
		self.math_frame = ctk.CTkFrame(master = self.control_frame)


		self.cursor_frame = ctk.CTkFrame(master = self.options_frame)	
	

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
		self.deletion_button = ctk.CTkButton(master = self.options_frame,
			command = self.delete_file,
	                text = "Delete")
		self.viewmode_button = ctk.CTkButton(master = self.options_frame,
			command = self.vm_toggle,
			text = "Viewmode")
		self.derivative_button = ctk.CTkButton(master = self.math_frame,
			command = self.derivative,
			text = "f'")
		self.scale_button = ctk.CTkButton(master = self.options_frame,
			command = self.toggle_graph_scale,
			text = "lin/log")
		self.legend_button = ctk.CTkButton(master = self.options_frame,
			command = self.toggle_legend,
			text = "legend")
		self.box_button = ctk.CTkButton(master = self.math_frame,
			command = self.box_average,
			text = "box average")
		self.all_button = ctk.CTkCheckBox(master = self.selector_frame,
			command = self.all,
			variable = self.select_all,
			text = "")
		self.explorer_button = ctk.CTkButton(master = self.adding_frame,
			command = self.file_browser,
			text = "explorer")
		self.average_button = ctk.CTkButton(master = self.math_frame,
			command = self.average,
			text = "average")
		self.floating_potential_button = ctk.CTkButton(master = self.math_frame,
			command = self.floating,
			text = "floating potential")
		
		self.basic_isat_button = ctk.CTkButton(master = self.math_frame,
			command = self.basic_isat,
			text = "basic isat")
		self.savgol_button = ctk.CTkButton(master = self.math_frame,
			command = self.savgol,
			text = "savgol filter")

		self.fit_counter = ctk.CTkLabel(master = self.cursor_frame, textvar = self.fit_bound[0])
		self.file_addition_selector = ctk.CTkOptionMenu(master = self.adding_frame, values=fnames)

		# Put the widgets on the screen
		self.redraw_widgets()

	def redraw_widgets(self):
		self.grid_columnconfigure(0,weight=1)
		self.grid_columnconfigure(1,weight=1)
		self.grid_rowconfigure(0,weight=1)

		self.left_frame.grid(row=0, column = 0, sticky="nsew")
		self.right_frame.grid(row=0, column = 1, sticky="nsew")
		
		self.left_frame.grid_rowconfigure(0, weight = 4)
		self.left_frame.grid_rowconfigure(1, weight = 1)
		self.left_frame.grid_columnconfigure(0, weight = 1)
		
		self.graph_frame.grid(row=0, column = 0, sticky = "nsew")
		self.adding_frame.grid(row=1, column = 0, sticky = "ew")
	
		self.file_addition_selector.grid(row=0, column=0)
		self.plot_button.grid(row=0, column=1)
		self.explorer_button.grid(row=0, column=2)	
		
		self.right_frame.grid_columnconfigure(0, weight=1)
		self.right_frame.grid_columnconfigure(1, weight=1)
		self.right_frame.grid_rowconfigure(0, weight=1)
		self.selector_frame.grid(row=0, column=0, sticky = "nsew")
		self.control_frame.grid(row=0, column=1, sticky = "nswe")

		self.control_frame.grid_columnconfigure(0, weight=1)
		self.control_frame.grid_rowconfigure(0, weight=1)
		self.control_frame.grid_rowconfigure(1, weight=2)

		self.options_frame.grid(row=0, column=0)
		self.math_frame.grid(row=1, column=0)	

		self.all_button.pack()
		self.deletion_button.pack()
		self.viewmode_button.pack()
		self.scale_button.pack()	
		self.legend_button.pack()

		self.derivative_button.pack()
		self.box_button.pack()
		self.average_button.pack()
		self.floating_potential_button.pack()		
		self.basic_isat_button.pack()
		self.savgol_button.pack()
		
		self.cursor_frame.pack()
		self.minus_button_el.grid(row=0,column=0)
		self.minus_button_l.grid(row=0,column=1)
		self.minus_button.grid(row=0,column=2)
		self.plus_button.grid(row=0,column=4)
		self.plus_button_l.grid(row=0,column=5)
		self.plus_button_el.grid(row=0,column=6)
		self.fit_counter.grid(column=3)
				
	def savgol(self):
		fname = self.get_selected()[0]
		smoothed = self.data_analyzer.savgol_smoothing(self.currently_displayed[fname])	
		self.add_graph(fname + "_sav", self.currently_displayed[fname][0], smoothed)

	# Get rid of the try except
	def basic_isat(self):
		fname = self.get_selected()[0]
		isat,electron_current = self.data_analyzer.ion_saturation_basic(self.currently_displayed[fname],self.fit_bound[0].get())	
		self.add_graph(fname + "_isat", self.currently_displayed[fname][0], isat)
		self.add_graph(fname + "_ecurr", self.currently_displayed[fname][0], electron_current)
	# TODO TODO TODO Broken, problem with directories
	def file_browser(self):
		fname = tk.filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"), ("all files","*.*")))
		[x,y] = self.get_data(fname)
		self.add_graph(fname, x, y)

	def floating(self):
		fname = self.get_selected()[0]
		asdfasdf = self.data_analyzer.floating_potential(self.currently_displayed[fname])
		print(asdfasdf)
		return asdfasdf	

	def all(self):
		v = self.select_all.get()
		for key in self.selector_display:
			self.selector_display[key][1].set(v)

	def toggle_legend(self):
		if self.legend_visibility == False:
			self.legend_visibility = True
		elif self.legend_visibility == True:
			self.legend_visibility = False
		self.plot()

	def toggle_graph_scale(self):
		if self.lin_log == 0:
			self.lin_log = 1
		elif self.lin_log == 1:
			self.lin_log = 0
		self.plot()

	def get_selected(self):
		selected = []
		for key in self.selector_display:
			if self.selector_display[key][0].winfo_children()[1].get() == 1:
				selected.append(key)

		return selected
	
	def delete_file(self):
		for s in self.get_selected():
			try:
				self.currently_displayed.pop(s)
				self.selector_display[s][0].pack_forget()
				self.selector_display[s][0].destroy()
				self.selector_display.pop(s)	

			except KeyError:
				print("\a")
		self.plot()

	def box_average(self):
		for fname in self.get_selected():
			try:
				data = self.data_analyzer.box_average(self.currently_displayed[fname])
				self.add_graph(fname + "_box_av", data[0], data[1])
			except KeyError:
				print("\a")
		self.plot()
	
	def average(self):
		data_to_average = []
		for fname in self.get_selected():
			data_to_average.append(self.currently_displayed[fname])
		# TODO broken
		data = self.data_analyzer.average(data_to_average)
		self.add_graph("average", data[0], data[1])
		self.plot()

	def incr(self,n):
		self.fit_bound[0].set(self.fit_bound[0].get()+n)		
		self.plot()

	def minu(self,n):
		self.fit_bound[0].set(self.fit_bound[0].get()-n)
		self.plot()
	
	def vm_toggle(self):	
		if self.view_mode == 0:
			self.view_mode = 1
		elif self.view_mode == 1:
			self.view_mode = 0
		self.plot()
	
	def add_new_graph(self):
		f = self.file_addition_selector.get()
		[x,y] = self.get_data(f)
		self.add_graph(f, x, y)

	def add_graph(self, f, x, y):
		self.currently_displayed.update({f: [x,y]})
	
		file_frame = ctk.CTkFrame(master = self.selector_frame)

		cb_value = tk.IntVar()
		label = ctk.CTkLabel(master = file_frame, text = f)
		cb = ctk.CTkCheckBox(master = file_frame, text = "",variable = cb_value)
		
		self.selector_display.update({f: [file_frame,cb_value]})

		self.plot()
		file_frame.pack()
		label.grid(row=0, column=0)
		cb.grid(row=0, column=1)	

	def derivative(self):
		for fname in self.get_selected():
			try:		
				data = self.data_analyzer.derivative(self.currently_displayed[fname],1)
				self.add_graph(fname+"_der", data[0], data[1])
			except KeyError:
				print("\a")
		self.plot()

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
	
	def plot(self):
		# Remake the graph frame. Probably a better way than doing this.	
		self.graph_frame = ctk.CTkFrame(master=self.left_frame)

		# The figure that will contain the plot and adding the plot
		fig = Figure(figsize = (10, 10), dpi = 100)
		plot1 = fig.add_subplot(111)

		if self.lin_log == 1:
			plot1.set_yscale("log")			
		else:
			plot1.set_yscale("linear")

		for data in self.currently_displayed.values():
			# Take the data from the file given	
			[x,y] = data	

			if self.view_mode == 0:
				plot1.plot(x,y,'o')
			else:
				plot1.plot(x,y)
			
		self.canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		if self.legend_visibility:
			plot1.legend(self.currently_displayed.keys())
		self.canvas.get_tk_widget().pack()

		self.graph_frame.grid(row=0, column = 0, sticky = "nsew")
	
if __name__ == "__main__":
	app = App()
	app.mainloop()
