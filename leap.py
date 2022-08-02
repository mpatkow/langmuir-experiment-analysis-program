import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import os
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import numpy as np
import sys
from matplotlib import pyplot as plt
import data_manipulator
import platform
import math
from tkinter.filedialog import asksaveasfilename

ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
plt.style.use("default")

# When adding a product of an original graph it is possible to add multiples. Fix this.
# when doing manipulations improve the name of the new file
######" """""" AUTOFEATURES""""


class App(ctk.CTk):
	def __init__(self):
		super().__init__()


		# Optional starting directory
		try:
			self.starting_dir = sys.argv[1]
		except:
			self.starting_dir = "~"

		# Set up the basic window things
		self.WIDTH = 1400
		self.HEIGHT = 5000
		self.title("Langmuir Experiment Analyzer Program")
		self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))
		if platform.system() == "Darwin":
			self.img = tk.Image("photo", file="icon.png")
			self.tk.call('wm', 'iconphoto', self._w, self.img)
		self.data_analyzer = data_manipulator.data_manipulator()

		option_file = open("options.txt", "r")
		self.options = [l.split("\t")[1][:-1] for l in option_file.readlines()]
		option_file.close()

		# This list holds the filenames of the graphs that are displayed, along with their data
		self.currently_displayed = {}
		self.selector_display = {}
		self.lin_log = 0
		if self.options[2] == "False":
			self.data_type_old = False
		else:
			self.data_type_old = True
		if self.options[1] == "\\t":
			self.xy_split = "\t"
		else:
			self.xy_split = self.options[1]
		self.next_index = 0
		self.select_all = tk.IntVar()
		self.legend_visibility = False
		self.cursor_visibility = [tk.IntVar(value=0), tk.IntVar(value=0)]
		self.fit_bound = [tk.IntVar(value=0), tk.IntVar(value=0)]
		self.cursor_positions = []
		self.graph_indexes = {"cursor1" : 0, "cursor2" : 1}
		self.temperature = tk.StringVar(value = "---")
		self.floating_potential = tk.DoubleVar()
		self.debye_length = tk.DoubleVar()
		self.density = tk.DoubleVar()
		self.probe_radius = tk.DoubleVar()
		self.debye_ratio = tk.DoubleVar()

		# Frames
		self.left_frame = ctk.CTkFrame()
		self.right_frame = ctk.CTkFrame()

		self.graph_frame = ctk.CTkFrame(master = self.left_frame) 	# Holds the graph
		self.adding_frame = ctk.CTkFrame(master = self.left_frame)	# Holds the controls for adding and removing files from the graph.


		self.control_frame = ctk.CTkFrame(master = self.right_frame)# Holds the controls for manipulating the graphs.
		self.middle_frame = ctk.CTkFrame(master = self.right_frame)
		self.selector_frame = ctk.CTkFrame(master = self.middle_frame)
		self.select_all_frame = ctk.CTkFrame(master = self.selector_frame)

		self.options_frame = ctk.CTkFrame(master = self.control_frame)
		self.math_frame = ctk.CTkFrame(master = self.control_frame)
		self.useless_frame  = ctk.CTkFrame(master = self.control_frame)

		self.cursor_frame = ctk.CTkFrame(master = self.options_frame)



		""" RESULTS FRAMES """
		self.results_frame = ctk.CTkFrame(master = self.middle_frame)
		self.temperature_frame = ctk.CTkFrame(master = self.results_frame)
		self.temperature_button = ctk.CTkButton(master = self.temperature_frame,
			command = self.temp_fit,
			text = "kTe:",
			height = 30,
			width = 30)
		self.temperature_label = ctk.CTkLabel(master = self.temperature_frame,
			textvar = self.temperature)
		self.floating_frame = ctk.CTkFrame(master = self.results_frame)
		self.floating_potential_button = ctk.CTkButton(master = self.floating_frame,
			command = self.floating,
			text = "Vf:",
			height = 30,
			width = 30)
		self.floating_label = ctk.CTkLabel(master = self.floating_frame,
			textvar = self.floating_potential)
		self.probe_area_frame = ctk.CTkFrame(master = self.results_frame)
		self.probe_area_input = ctk.CTkEntry(master = self.probe_area_frame,
			width = 120,
			height = 25,
			corner_radius = 10)
		self.probe_area_label = ctk.CTkLabel(master = self.probe_area_frame,
			text = "Ap (cm^2):")
		self.ion_mass_frame = ctk.CTkFrame(master = self.results_frame)
		self.ion_mass_input = ctk.CTkEntry(master = self.ion_mass_frame,
			width = 120,
			height = 25,
			corner_radius = 10)
		self.ion_mass_label = ctk.CTkLabel(master = self.ion_mass_frame,
			text = "M (kg):")
		self.debye_frame = ctk.CTkFrame(master = self.results_frame)
		self.debye_button = ctk.CTkButton(master = self.debye_frame,
			command = self.debye,
			text = "lD (fix):",
			height = 30,
			width = 30)
		self.debye_label = ctk.CTkLabel(master = self.debye_frame,
			textvar = self.debye_length)
		self.debye_ratio_frame = ctk.CTkFrame(master = self.results_frame)
		self.debye_ratio_button = ctk.CTkButton(master = self.debye_ratio_frame,
			command = self.debye_ratio,
			text = "e(fix this_):",
			height = 30,
			width = 30)
		self.debye_ratio_label = ctk.CTkLabel(master = self.debye_ratio_frame,
			textvar = self.debye_ratio_calculate)

		# The figure that will contain the plot and adding the plot
		self.fig = Figure(figsize = (int(self.options[0]),int(self.options[0])), dpi = 100)
		self.plot1 = self.fig.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
		self.canvas.get_tk_widget().pack()

		self.toolbar = NavigationToolbar2Tk(self.canvas, self.useless_frame)
		self.toolbar.update()
		self.cursor1 = self.plot1.axvline(x=self.fit_bound[0].get(),linestyle = "None")
		self.cursor2 = self.plot1.axvline(x=self.fit_bound[1].get(),linestyle = "None")
		self.canvas.draw()

		""" ADDING FRAME """

		self.explorer_button = ctk.CTkButton(master = self.adding_frame,
			command = self.file_browser,
			text = "explorer")
		self.deletion_button = ctk.CTkButton(master = self.adding_frame,
			command = self.delete_file,
	                text = "Delete")
		self.save_button = ctk.CTkButton(master = self.adding_frame,
			command = self.save_data,
			text = "save data")
		self.save_image_button = ctk.CTkButton(master = self.adding_frame,
			command = self.save_image_data,
			text = "save image")
		self.zoom_button = ctk.CTkButton(master = self.adding_frame,
			command = self.fig.canvas.toolbar.zoom,
			text = "zoom")
		self.pan_button = ctk.CTkButton(master = self.adding_frame,
			command = self.fig.canvas.toolbar.pan,
			text = "pan")



		self.plus_button = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(1,1),
			text = ">",
			width = 5)
		self.plus_button_l = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(10,1),
			text = ">>",
			width = 5)
		self.minus_button = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(1,1),
			text = "<",
			width = 5)
		self.minus_button_l = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(10,1),
			text = "<<",
			width = 5)
		self.plus_button_2 = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(1,2),
			text = ">",
			width = 5)
		self.plus_button_l_2 = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.incr(10,2),
			text = ">>",
			width = 5)
		self.minus_button_2 = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(1,2),
			text = "<",
			width = 5)
		self.minus_button_l_2 = ctk.CTkButton(master = self.cursor_frame,
			command = lambda: self.minu(10,2),
			text = "<<",
			width = 5)

		self.rescale_button = ctk.CTkButton(master = self.options_frame,
			command = self.rescale,
			text = "Rescale")
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
		self.select_all_button = ctk.CTkCheckBox(master = self.select_all_frame,
			command = self.all,
			variable = self.select_all,
			text = "")
		self.average_button = ctk.CTkButton(master = self.math_frame,
			command = self.average,
			text = "average")
		self.square_button = ctk.CTkButton(master = self.math_frame,
			command = self.square,
			text = "f^2")
		self.basic_isat_button = ctk.CTkButton(master = self.math_frame,
			command = self.basic_isat,
			text = "basic isat")
		self.basic_isat_button_auto = ctk.CTkButton(master = self.math_frame,
			command = self.basic_isat_auto,
			text = "basic isat auto")
		self.savgol_button = ctk.CTkButton(master = self.math_frame,
			command = self.savgol,
			text = "savgol filter")
		self.eedf_button = ctk.CTkButton(master = self.math_frame,
			command = self.eedf,
			text = "EEDF",
			fg_color="red")
		self.plasma_potential_button = ctk.CTkButton(master= self.math_frame,
			command = self.plasma_potential,
			text = "plasma potential")
		self.absolute_button = ctk.CTkButton(master = self.math_frame,
			command = self.absolute_v,
			text = "|f|")
		self.natural_log_button = ctk.CTkButton(master = self.math_frame,
			command = self.natural,
			text = "ln")
		self.oml_button = ctk.CTkButton(master = self.math_frame,
			command = self.oml,
			text = "oml")

		self.fit_counter = ctk.CTkLabel(master = self.cursor_frame, textvar = self.fit_bound[0])
		self.fit_counter_2 = ctk.CTkLabel(master = self.cursor_frame, textvar = self.fit_bound[1])
		self.cursor_show_button = ctk.CTkCheckBox(master = self.cursor_frame,
			command = lambda: self.hide_cursor(1),
			variable = self.cursor_visibility[0],
			text = "")
		self.cursor_show_button_2 = ctk.CTkCheckBox(master = self.cursor_frame,
			command = lambda: self.hide_cursor(2),
			variable = self.cursor_visibility[1],
			text = "")

		self.select_all_label = ctk.CTkLabel(master = self.select_all_frame, text = "Select All:")

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
		self.adding_frame.grid(row=1, column = 0, sticky = "nsew")

		self.explorer_button.grid(row=0, column=0, sticky = "nsew")
		self.deletion_button.grid(row=0, column=1, sticky = "nsew")
		self.save_button.grid(row=0, column=2, sticky = "nsew")
		self.zoom_button.grid(row=0, column=3, sticky = "nsew")
		self.pan_button.grid(row=0, column=4, sticky = "nsew")
		self.save_image_button.grid(row=0, column=5, sticky = "nsew")

		self.right_frame.grid_columnconfigure(0, weight=1)
		self.right_frame.grid_columnconfigure(1, weight=1)
		self.right_frame.grid_rowconfigure(0, weight=1)
		self.middle_frame.grid(row=0, column=0, sticky = "nswe")
		self.middle_frame.grid_rowconfigure(0, weight = 1)
		self.middle_frame.grid_rowconfigure(1, weight = 1)
		self.selector_frame.grid(row=0, column=0, sticky = "nswe")
		self.results_frame.grid(row=1, column=0, sticky = "nswe")
		self.control_frame.grid(row=0, column=1, sticky = "nswe")

		self.control_frame.grid_columnconfigure(0, weight=1)
		self.control_frame.grid_rowconfigure(0, weight=1)
		self.control_frame.grid_rowconfigure(1, weight=2)

		self.options_frame.grid(row=0, column=0)
		self.math_frame.grid(row=1, column=0)

		self.select_all_frame.pack()
		self.select_all_label.grid(row=0, column=0)
		self.select_all_button.grid(row=0, column=1)

		self.probe_area_frame.pack(fill = tk.X)
		self.probe_area_label.grid(row = 0, column = 0)
		self.probe_area_input.grid(row = 0, column = 1)
		self.ion_mass_frame.pack(fill = tk.X)
		self.ion_mass_label.grid(row = 0, column = 0)
		self.ion_mass_input.grid(row = 0, column = 1)
		self.temperature_frame.pack(fill=tk.X)
		self.temperature_button.grid(row = 0, column = 0)
		self.temperature_label.grid(row = 0, column = 1)
		self.floating_frame.pack(fill=tk.X)
		self.floating_potential_button.grid(row = 0, column = 0)
		self.floating_label.grid(row = 0, column = 1)
		self.debye_frame.pack(fill = tk.X)
		self.debye_button.grid(row = 0, column = 0)
		self.debye_label.grid(row = 0, column = 1)
		self.debye_ratio_frame.pack(fill = tk.X)
		self.debye_ratio_button.grid(row = 0, column = 0)
		self.debye_ratio_label.grid(row = 0, column = 1)

		self.scale_button.pack()
		self.legend_button.pack()
		self.rescale_button.pack()

		self.derivative_button.pack()
		self.box_button.pack()
		self.average_button.pack()
		self.basic_isat_button.pack()
		self.basic_isat_button_auto.pack()
		self.savgol_button.pack()
		self.eedf_button.pack()
		self.plasma_potential_button.pack()
		self.absolute_button.pack()
		self.natural_log_button.pack()
		self.square_button.pack()
		self.oml_button.pack()

		self.cursor_frame.pack()
		self.minus_button_l.grid(row=0,column=0)
		self.minus_button.grid(row=0,column=1)
		self.plus_button.grid(row=0,column=3)
		self.plus_button_l.grid(row=0,column=4)
		self.fit_counter.grid(row=0,column=2)
		self.cursor_show_button.grid(row=0,column=5)
		self.minus_button_l_2.grid(row=1,column=0)
		self.minus_button_2.grid(row=1,column=1)
		self.plus_button_2.grid(row=1,column=3)
		self.plus_button_l_2.grid(row=1,column=4)
		self.fit_counter_2.grid(row=1,column=2)
		self.cursor_show_button_2.grid(row=1,column=5)

	def check_selected_files(self):
		opened_files = self.get_selected()
		if len(opened_files) == 0:
			self.open_popup("NOTICE: no file selected")
			return 0
		elif len(opened_files) > 1:
			self.open_popup("NOTICE: select a single file")
			return 2
		else:
			return 1

	def debye_ratio_calculate(self):
		self.debye_ratio.set(self.probe_radius.get())/(self.debye_length.get())

	def square(self):
		if self.check_selected_files() == 1:
			fname = self.get_selected()[0]
			newfname = self.get_next_name(fname)
			sq = np.square(self.currently_displayed[fname][1])
			self.add_graph(newfname, self.currently_displayed[fname][0], sq)

	def hide_cursor(self, n):
		if n == 1:
			if self.cursor1.get_linestyle() == "None":
				self.cursor1.set_linestyle("solid")
			else:
				self.cursor1.set_linestyle("None")
		elif n == 2:
			if self.cursor2.get_linestyle() == "None":
				self.cursor2.set_linestyle("solid")
			else:
				self.cursor2.set_linestyle("None")

		self.canvas.draw()

	def absolute_v(self):
		fname = self.get_selected()[0]
		a = self.data_analyzer.absolute_val(self.currently_displayed[fname])[1]
		self.add_graph(fname + "_sav", self.currently_displayed[fname][0], a)

	def save_data(self):
		fname = self.get_selected()[0]
		data = self.currently_displayed[fname]
		data_to_write = ""
		for i in range(len(data[0])):
			data_to_write += str(data[0][i])
			data_to_write += self.xy_split
			data_to_write += str(data[1][i])
			data_to_write += "\n"

		data_to_write = data_to_write[:-1]
		name_to_write_to = asksaveasfilename(initialfile = "", defaultextension=".txt", filetypes=[("Text Files","*.txt"),("Csv Files", "*.csv"), ("All Files", "*.*")])
		f = open(name_to_write_to, "w")
		f.write(data_to_write)
		f.close()

	def save_image_data(self):
		fname = asksaveasfilename(initialfile = "", defaultextension=".png", filetypes=[("Png Files","*.png"),("Jpg Files", "*.jpg"), ("All Files", "*.*")])
		if fname is None:
			return 
		self.fig.savefig(fname,dpi = plt.gcf().dpi)
		self.canvas.draw()

	def plasma_potential(self):
		fname = self.get_selected()[0]
		asdfasdf = self.data_analyzer.plasma_potential(self.currently_displayed[fname])
		print(asdfasdf)
		return asdfasdf

	def eedf(self):
		fname = self.get_selected()[0]
		print(self.currently_displayed[fname])
		vp = float(input("V_p?: "))
		ee = self.data_analyzer.druyvesteyn(self.currently_displayed[fname],vp)
		self.add_graph(fname + "_ee", self.currently_displayed[fname][0], ee)

	# Savgol filter on selected files
	def savgol(self):
		if len(self.get_selected()) == 0:
			self.open_popup("NOTICE: no file selected")
		for fname in self.get_selected():
			try:
				smoothed = self.data_analyzer.savgol_smoothing(self.currently_displayed[fname])
				self.add_graph(fname + "_sav", self.currently_displayed[fname][0], smoothed)
			except:
				print(e)

	# Get rid of the try except
	def basic_isat(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		lower_abs = np.absolute(data_t[0] - self.fit_bound[0].get())
		upper_abs = np.absolute(data_t[0] - self.fit_bound[1].get())
		isat,electron_current = self.data_analyzer.ion_saturation_basic(data_t,np.where(lower_abs == np.min(lower_abs))[0][0],np.where(upper_abs == np.min(upper_abs))[0][0])
		self.add_graph(fname + "_isat", self.currently_displayed[fname][0], isat)
		self.add_graph(fname + "_ecurr", self.currently_displayed[fname][0], electron_current)

	def basic_isat_auto(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		isat,electron_current = self.data_analyzer.ion_saturation_basic_auto(data_t)
		self.add_graph(fname + "_isat", self.currently_displayed[fname][0], isat)
		self.add_graph(fname + "_ecurr", self.currently_displayed[fname][0], electron_current)

	def oml(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		lower_abs = np.absolute(data_t[0] - self.fit_bound[0].get())
		upper_abs = np.absolute(data_t[0] - self.fit_bound[1].get())
		#density = self.data_analyzer.oml_theory(data_t,np.where(lower_abs == np.min(lower_abs))[0][0],np.where(upper_abs == np.min(upper_abs))[0][0],self.probe_area_input.get(),self.ion_mass_input.get())
		ddd = self.data_analyzer.oml_theory(data_t,np.where(lower_abs == np.min(lower_abs))[0][0],np.where(upper_abs == np.min(upper_abs))[0][0],0.047,6.62 * 10**(-26))
		self.density.set(ddd)
		print(ddd)

	def debye(self):
		l_squared = 8.8541878128*10**(-12)*float(self.temperature.get().split(' ')[0])/(1.60217663*10**(-19) * float(self.density.get()) * 10**6)
		self.debye_length.set(l_squared ** 0.5)

	def floating(self):
		if self.check_selected_files() == 1:
			fname = self.get_selected()[0]
			fp = self.data_analyzer.floating_potential(self.currently_displayed[fname])
			self.floating_potential.set(fp[0])

	def all(self):
		v = self.select_all.get()
		for key in self.selector_display:
			self.selector_display[key][1].set(v)

	def toggle_legend(self):
		if self.legend_visibility == False:
			self.legend_visibility = True
			self.plot1.legend(self.currently_displayed.keys())
		elif self.legend_visibility == True:
			self.legend_visibility = False
			self.plot1.get_legend().remove()
		self.canvas.draw()

	def toggle_graph_scale(self):
		if self.lin_log == 0:
			self.lin_log = 1
			self.plot1.set_yscale("log")
		elif self.lin_log == 1:
			self.lin_log = 0
			self.plot1.set_yscale("linear")
		self.canvas.draw()

	def rescale(self):
		xs = []
		ys = []
		for v1 in self.get_selected():
			xs.extend(list(self.currently_displayed[v1][0]))
			ys.extend(list(self.currently_displayed[v1][1]))

		xs = [xss for xss in xs if str(xss) != 'nan']
		ys = [yss for yss in ys if str(yss) != 'nan']

		minxs = float(min(xs))
		minys = float(min(ys))
		maxxs = float(max(xs))
		maxys = float(max(ys))

		self.plot1.set_xlim(minxs,maxxs)
		self.plot1.set_ylim(minys,maxys)
		self.canvas.draw()

	def get_selected(self):
		selected = []
		for key in self.selector_display:
			if self.selector_display[key][0].winfo_children()[1].get() == 1:
				selected.append(key)
		return selected

	def box_average(self):
		for fname in self.get_selected():
			try:
				data = self.data_analyzer.box_average(self.currently_displayed[fname])
				prelim_fname = fname.split("/")[-1].split(".")[0] + "_box." + fname.split("/")[-1].split(".")[1]
				if prelim_fname not in list(self.graph_indexes.keys()):
					self.add_graph(prelim_fname, data[0], data[1])

			except KeyError:
				print("\a")

	# BETTER NAMES
	def average(self):
		data_to_average = []
		for fname in self.get_selected():
			data_to_average.append(self.currently_displayed[fname])
		# TODO broken
		data = self.data_analyzer.average(data_to_average)
		self.add_graph("average", data[0], data[1])

	def incr(self,n,cnum):
		self.fit_bound[cnum-1].set(self.fit_bound[cnum-1].get()+n)
		if cnum == 1:
			self.cursor1.set_xdata(self.fit_bound[cnum-1].get())
		if cnum == 2:
			self.cursor2.set_xdata(self.fit_bound[cnum-1].get())
		self.canvas.draw()

	def minu(self,n,cnum):
		self.fit_bound[cnum-1].set(self.fit_bound[cnum-1].get()-n)
		if cnum == 1:
			self.cursor1.set_xdata(self.fit_bound[cnum-1].get())
		if cnum == 2:
			self.cursor2.set_xdata(self.fit_bound[cnum-1].get())
		self.canvas.draw()

	def temp_fit(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		lower_abs = np.absolute(data_t[0] - self.fit_bound[0].get())
		upper_abs = np.absolute(data_t[0] - self.fit_bound[1].get())
		temp_fit_lower = np.where(lower_abs == np.min(lower_abs))[0][0]
		temp_fit_upper = np.where(upper_abs == np.min(upper_abs))[0][0]
		temps = []
		for upper_bound in range(temp_fit_lower, temp_fit_upper+1):
			for lower_bound in range(temp_fit_lower, upper_bound):
				if abs(lower_bound-upper_bound) == 1:
					pass
				else:
					m,b = np.polyfit(data_t[0][lower_bound:upper_bound], data_t[1][lower_bound:upper_bound], 1)
					temps.append(1/m)

		temps = np.array(temps)
		av = np.average(temps)
		std = np.std(temps)

		self.temperature.set(str(av) + " +- " + str(std))

		print("Temp: ", av)
		print("Bounds: %f to %f" % (av - std, av + std) )

	def derivative(self):
		for fname in self.get_selected():
			try:
				data = self.data_analyzer.derivative(self.currently_displayed[fname],1)
				prelim_fname = fname.split("/")[-1].split(".")[0] + "_der." + fname.split("/")[-1].split(".")[1]
				if prelim_fname not in list(self.graph_indexes.keys()):
					self.add_graph(prelim_fname, data[0], data[1])
			except KeyError:
				print("\a")

	def natural(self):
		for fname in self.get_selected():
			try:
				data = [self.currently_displayed[fname][0],np.log(self.currently_displayed[fname][1])]
				#prelim_fname = fname.split("/")[-1].split(".")[0] + "_ln." + fname.split("/")[-1].split(".")[1]
				prelim_fname = fname  + "average_ln"
				if prelim_fname not in list(self.graph_indexes.keys()):
					self.add_graph(prelim_fname, data[0], data[1])
			except KeyError:
				print("\a")

	def open_popup(self,message):
		top = ctk.CTkToplevel(self)
		top.geometry("1000x100")
		top.title("Error!")
		tk.Label(top, textvariable = tk.StringVar(value = message),fg="red",font = ("courier",50),bg = "#2a2d2e").pack()

	def file_browser(self):
		fnames = tk.filedialog.askopenfilenames(initialdir = self.starting_dir, title = "Select a File", filetypes = [("csv files", "*.csv"),("data files", "*.txt"),  ("all files","*.*")])
		for fname in fnames:
			if fname not in self.selector_display.keys():
				[x,y] = self.get_data(fname)
				try:
					if x == None or y == None:
						pass
					else:
						self.add_graph(fname, x, y)
				except:
					self.add_graph(fname, x, y)

			else:
				self.open_popup("NOTICE: file already opened")

	def get_data(self, fname):
		try:
			if self.data_type_old == True:
				f = open(fname, "r")
				vi_data = f.readlines()
				f.close()
				# Fix the data into a format usable by the code
				vi_data = vi_data[0]
				vi_data = vi_data.split(",")
				x = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 0])
				y = np.array([float(vi_data[i]) for i in range(len(vi_data)) if i % 2 == 1])
			else:
				f = open(fname, "r")
				vi_data = f.readlines()
				f.close()
				x = np.array([float(vi_data[i].split(self.xy_split)[0]) for i in range(len(vi_data))])
				y = np.array([float(vi_data[i].split(self.xy_split)[1]) for i in range(len(vi_data))])


			################# EXPERIMENTAL #################

			avv = np.average(y)
			for i in range(1,len(y)-1):
				if abs(y[i]-avv) >= 0.1:
					y[i] = (y[i+1] + y[i-1])/2

			return x,y
		except:
			self.open_popup("ERR: invalid data")
			return None,None

	def add_graph(self, f, x, y):
		self.currently_displayed.update({f: [x,y]})

		file_frame = ctk.CTkFrame(master = self.selector_frame)

		cb_value = tk.IntVar()
		label = ctk.CTkLabel(master = file_frame, text = f.split("/")[-1])
		cb = ctk.CTkCheckBox(master = file_frame, text = "",variable = cb_value)

		self.selector_display.update({f: [file_frame,cb_value]})
		self.update_next_index()
		self.graph_indexes.update({f: self.next_index})

		self.plot(x,y)
		file_frame.pack()
		label.grid(row=0, column=0)
		cb.grid(row=0, column=1)

	def update_next_index(self):
		indexes = list(self.graph_indexes.values())
		indexes.sort()
		i=0
		while i in indexes:
			i += 1

		self.next_index = i

	def delete_file(self):
		for s in self.get_selected():
			self.currently_displayed.pop(s)
			self.selector_display[s][0].pack_forget()
			self.selector_display[s][0].destroy()
			self.selector_display.pop(s)
			self.plot1.get_lines()[self.graph_indexes[s]].remove()
			i = self.graph_indexes[s]
			del self.graph_indexes[s]
			for e in self.graph_indexes:
				if self.graph_indexes[e] > i:
					self.graph_indexes[e] -= 1

		self.canvas.draw()

	def plot(self,x,y):
		self.plot1.plot(x,y,'o')
		self.canvas.draw()

	def get_next_name(self,prelim):
		relevant_numbers = []
		prelim_type = prelim.split(".")[0].split("__")[0]
		for f in self.selector_display.keys():
			if prelim_type == f.split(".")[0].split("__")[0]:
				try:
					relevant_numbers.append(int(f.split(".")[0].split("__")[-1]))
				except:
					pass

		i = 0
		while i in relevant_numbers:
			i+=1

		return prelim.split(".")[0].split("__")[0] + "__" + str(i) + "." + prelim.split(".")[-1]



if __name__ == "__main__":
	app = App()
	app.mainloop()
