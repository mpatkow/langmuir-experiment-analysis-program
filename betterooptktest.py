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
# Averages
# Try to update graph without redrawing the whole thing, messing up scales
# multiple labels in the selector frame are made for adding the same thing

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
		self.graph_frame = ctk.CTkFrame() 	# Holds the graph
		self.control_frame = ctk.CTkFrame()	# Holds the controls for manipulating the graphs.
		self.adding_frame = ctk.CTkFrame()	# Holds the controls for adding and removing files from the graph.
		self.cursor_frame = ctk.CTkFrame(master = self.control_frame)	
		self.selector_frame = ctk.CTkFrame()	
	
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
			command = self.vm_toggle,
			text = "Viewmode")
		self.derivative_button = ctk.CTkButton(master = self.control_frame,
			command = self.derivative,
			text = "f'")
		self.scale_button = ctk.CTkButton(master = self.control_frame,
			command = self.toggle_graph_scale,
			text = "lin/log")
		self.legend_button = ctk.CTkButton(master = self.control_frame,
			command = self.toggle_legend,
			text = "legend")
		self.box_button = ctk.CTkButton(master = self.control_frame,
			command = self.box_average,
			text = "box average")
		self.all_button = ctk.CTkCheckBox(master = self.control_frame,
			command = self.all,
			variable = self.select_all,
			text = "")

		self.fit_counter = ctk.CTkLabel(master = self.control_frame, textvar = self.fit_bound[0])
		self.file_addition_selector = ctk.CTkOptionMenu(master = self.adding_frame, values=fnames)
		self.file_selector = ctk.CTkOptionMenu(master = self.control_frame, values=list(self.currently_displayed.keys()))

		# Put the widgets on the screen
		self.redraw_widgets()

	def redraw_widgets(self):
		self.control_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
		self.graph_frame.grid(row=0, column = 0)
		self.adding_frame.grid(row=1, column = 0)
		self.plot_button.grid(row=0, column=1)
		self.selector_frame.grid(row = 0, column = 2)
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
		self.derivative_button.pack()
		self.scale_button.pack()	
		self.legend_button.pack()
		self.box_button.pack()
		self.all_button.pack()

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
	
	def delete_file(self,f):
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
		try:
			fname = self.file_selector.get()
			data = self.data_analyzer.box_average(self.currently_displayed[fname])
			self.currently_displayed.update({fname + "box_av" : data})
		except KeyError:
			print("\a")
		self.plot()

	def update(self):
		self.file_selector.pack_forget()
		self.file_selector.__init__(master = self.control_frame, values = list(self.currently_displayed.keys()))
		self.file_selector.pack()

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
		try:		
			fname = self.file_selector.get()
			data = self.data_analyzer.derivative(self.currently_displayed[fname],1)
			self.currently_displayed.update({fname + "_der" : data})
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
		self.graph_frame = ctk.CTkFrame(width = 500, height = 500)

		# The figure that will contain the plot and adding the plot
		fig = Figure(figsize = (10, 10), dpi = 100)
		plot1 = fig.add_subplot(111)

		if self.lin_log == 1:
			plot1.set_yscale("log")			
		else:
			plot1.set_yscale("linear")
		self.update()

		for data in self.currently_displayed.values():
			# Take the data from the file given	
			[x,y] = data	

			if self.view_mode == 0:
				plot1.plot(x,y,'o')
			else:
				plot1.plot(x,y)
			
			plot1.plot([x[self.fit_bound[0].get()]], [y[self.fit_bound[0].get()]], marker="o", markersize=20, markeredgecolor="red") 
		
		self.canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		if self.legend_visibility:
			plot1.legend(self.currently_displayed.keys())
		self.canvas.get_tk_widget().pack()

		self.graph_frame.grid(row=0, column = 0)
	
if __name__ == "__main__":
	app = App()
	app.mainloop()
