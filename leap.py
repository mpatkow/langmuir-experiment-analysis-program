import tkinter as tk
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
import LEAP_Frames
import LEAP_Buttons
import Options
import Widget_Redrawer
from scipy import interpolate as itp

ctk.set_appearance_mode("Dark")	# Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
plt.style.use("default")

# when doing manipulations improve the name of the new file

class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		option_file = open("options.txt", "r")
		self.options = [l.split("\t")[1][:-1] for l in option_file.readlines()]
		option_file.close()

		# Optional starting directory
		try:
			self.starting_dir = sys.argv[1]
		except:
			self.starting_dir = "~"

		# Set up the basic window things
		self.WIDTH = 5000
		self.HEIGHT = 5000
		self.title("Langmuir Experiment Analyzer Program")
		self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))

		self.data_analyzer = data_manipulator.data_manipulator()
		self.WR = Widget_Redrawer.Widget_Redrawer()

		self.data_type_old			  = False
		self.currently_displayed		= {}
		self.selector_display		   = {}
		self.graph_indexes			  = {"cursor1" : 0, "cursor2" : 1}
		self.lin_log					= 0
		self.next_index				 = 0
		self.select_all				 = tk.IntVar()
		self.legend_visibility		  = False
		self.cursor_visibility		  = [tk.IntVar(value=0), tk.IntVar(value=0)]
		self.fit_bound				  = [tk.IntVar(value=0), tk.IntVar(value=0)]
		self.cursor_positions		   = []
		self.temperature				= tk.StringVar(value = "---")
		self.floating_potential		 = tk.DoubleVar()
		self.debye_length			   = tk.DoubleVar()
		self.density					= tk.DoubleVar()
		self.probe_area				 = 0  
		self.gas_type				   = float(self.options[3])/(10**3 * 6.023 * 10**23) # The atomic mass of the element is entered in options.txt
		self.probe_radius			   = tk.DoubleVar()
		self.debye_ratio				= tk.DoubleVar()
		self.normal_vp				  = tk.DoubleVar()
		self.bounds					 = [tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0)]
		self.bounds1					= tk.StringVar(value = str(self.bounds[0].get()) + " to " + str(self.bounds[1].get()))
		self.bounds2					= tk.StringVar(value = str(self.bounds[2].get()) + " to " + str(self.bounds[3].get()))
		self.elementary_charge          = 1.60217663 * 10 ** (-19)
		self.ecurr_view					= False 

		# The normal format this program reads for langmuir sweeps is	  xvalue xy_split yvalue newlinecharacter		   
		# The old format is a continuous, one line list of x1,y1,x2,y2, ... 
		# Other data formats might be added in the future
		# The separator in the normal data format can be modified by changing the xy_split variable in the options file. This defaults to a tab (\t)
		if self.options[2] == "True":
			self.data_type_old = True
		if self.options[4] == "True":
			self.ecurr_view = True
		if self.options[1] == "\\t":
			self.xy_split = "\t"
		else:
			self.xy_split = self.options[1]
		
		LEAP_Frames.LEAP_Frames(self)
		LEAP_Buttons.LEAP_Buttons(self)
		self.redraw_widgets()
		
	def redraw_widgets(self):
	   	self.WR.redraw_widgets(self)
		
	def check_selected_files(self):
		opened_files = self.get_selected()
		if len(opened_files) == 0:
			self.open_popup("NOTICE: no file selected", True)
			return 0
		elif len(opened_files) > 1:
			self.open_popup("NOTICE: select a single file", True)
			return 2
		else:
			return 1

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

	def get_cursor_values(self,fname, data_t):
		data_t = self.currently_displayed[fname]
		lower_abs = np.absolute(data_t[0] - self.fit_bound[0].get())
		upper_abs = np.absolute(data_t[0] - self.fit_bound[1].get())
		return sorted([np.where(upper_abs == np.min(upper_abs))[0][0],np.where(lower_abs == np.min(lower_abs))[0][0]])

	# broken
	def debye_ratio_calculate(self):
		self.debye_ratio.set(self.probe_radius.get())/(self.debye_length.get())

	def normal_potential(self):
		a1 = self.bounds[0].get()
		a2 = self.bounds[1].get()
		b1 = self.bounds[2].get()
		b2 = self.bounds[3].get()

		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		m1,intercept1 = np.polyfit(data_t[0][a1:a2], data_t[1][a1:a2], 1)
		m2,intercept2 = np.polyfit(data_t[0][b1:b2], data_t[1][b1:b2], 1)
		self.normal_vp.set((intercept2-intercept1)/(m1-m2))

	def square(self):
		if self.check_selected_files() == 1:
			fname = self.get_selected()[0]
			newfname = self.get_next_name(fname)
			sq = np.square(self.currently_displayed[fname][1])
			self.add_graph(newfname, self.currently_displayed[fname][0], sq)

	def save_bounds_1(self):
		fname = self.get_selected()[0]
		cvalues = self.get_cursor_values(fname, self.currently_displayed)
		self.bounds[0].set(cvalues[0])
		self.bounds[1].set(cvalues[1])
		self.bounds1.set(value = str(int(self.currently_displayed[fname][0][self.bounds[0].get()])) + " to " + str(int(self.currently_displayed[fname][0][self.bounds[1].get()])))

	def save_bounds_2(self):
		fname = self.get_selected()[0]
		cvalues = self.get_cursor_values(fname, self.currently_displayed)
		self.bounds[2].set(cvalues[0])
		self.bounds[3].set(cvalues[1])
		self.bounds2.set(value = str(int(self.currently_displayed[fname][0][self.bounds[2].get()])) + " to " + str(int(self.currently_displayed[fname][0][self.bounds[3].get()])))
			
	def basic_density(self):
		fname = self.get_selected()[0]
		isat_value = abs(self.currently_displayed[fname][1][10])
		print(self.elementary_charge)
		print(self.probe_area)
		print(math.e)
		ne = isat_value/(self.elementary_charge * self.probe_area * math.e ** (-0.5)) * (self.gas_type / (float(self.temperature.get().split(' ')[0]) * self.elementary_charge) ) ** 0.5
		print(ne)


	def probe_area_update(self):
		self.probe_area = self.probe_area_sef.get_value()
		print("Set the probe area to: %f square mm." % self.probe_area)

	def absolute_v(self):
		if self.check_selected_files() == 1:
			fname = self.get_selected()[0]
			newfname = self.get_next_name(fname)
			sq = np.square(self.currently_displayed[fname][1])
			a = self.data_analyzer.absolute_val(self.currently_displayed[fname])[1]
			self.add_graph(newfname, self.currently_displayed[fname][0], a)

	def save_data(self):
		if self.check_selected_files() == 1:
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

	# broken
	def save_image_data(self):
		fname = asksaveasfilename(initialfile = "", defaultextension=".png", filetypes=[("Png Files","*.png"),("Jpg Files", "*.jpg"), ("All Files", "*.*")])
		if fname is None:
			return
		self.fig.savefig(fname,dpi = plt.gcf().dpi)
		self.canvas.draw()

	def open_help_and_options(self):
		self.help_and_options = Options.Options(self)

	# incomplete
	def plasma_potential(self):
		fname = self.get_selected()[0]
		asdfasdf = self.data_analyzer.plasma_potential(self.currently_displayed[fname])
		print(asdfasdf)
		return asdfasdf

	# incomplete
	def eedf(self):
		fname = self.get_selected()[0]
		print(self.currently_displayed[fname])
		vp = float(input("V_p?: "))
		ee = self.data_analyzer.druyvesteyn(self.currently_displayed[fname],vp)
		self.add_graph(fname + "_ee", self.currently_displayed[fname][0], ee)

	#TEMPORARILIY DOING SPLREP/SPLEV
	def savgol(self):
		if len(self.get_selected()) == 0:
			self.open_popup("NOTICE: no file selected", True)
		for fname in self.get_selected():
			try:
				smoothed = self.data_analyzer.savgol_smoothing(self.currently_displayed[fname])
				self.add_graph(fname + "_sav", self.currently_displayed[fname][0], smoothed)
			except:
				print(e)

	def spline_extrapolate(self):
		if len(self.get_selected()) == 0:
			self.open_popup("NOTICE: no file selected", True)
		for fname in self.get_selected():
			try:
				mytck,myu=itp.splprep([self.currently_displayed[fname][0],self.currently_displayed[fname][1]],k=5, s=0)
				xnew,ynew= itp.splev(np.linspace(0,1,3000),mytck)
				self.add_graph(fname + "_splrep", xnew, ynew)
			except:
				print(e)

	# Get rid of the try except
	def basic_isat(self):
		fname = self.get_selected()[0]
		[lower_abs, upper_abs] = self.get_cursor_values(fname, self.currently_displayed)
		isat,electron_current = self.data_analyzer.ion_saturation_basic(self.currently_displayed[fname],lower_abs, upper_abs)
		if self.ecurr_view:
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
		[lower_abs, upper_abs] = self.get_cursor_values(fname, self.currently_displayed)
		#density = self.data_analyzer.oml_theory(data_t,np.where(lower_abs == np.min(lower_abs))[0][0],np.where(upper_abs == np.min(upper_abs))[0][0],self.probe_area_input.get(),self.ion_mass_input.get())
		ddd = self.data_analyzer.oml_theory(data_t,lower_abs,upper_abs,0.047,6.62 * 10**(-26))
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

	def trim(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		[xmin, xmax] = self.get_cursor_values(fname, data_t)
		newfname = self.get_next_name(fname)
		self.add_graph(newfname, self.currently_displayed[fname][0][xmin:xmax], self.currently_displayed[fname][1][xmin:xmax])
		
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
		fname = self.get_selected()[0]
		newfname = self.get_next_name(fname)
		data = self.data_analyzer.average(data_to_average)
		self.add_graph(newfname, data[0], data[1])

	def incr(self,n,cnum):
		self.fit_bound[cnum-1].set(self.fit_bound[cnum-1].get()+n)
		if cnum == 1:
			self.cursor1.set_xdata(self.fit_bound[cnum-1].get())
		if cnum == 2:
			self.cursor2.set_xdata(self.fit_bound[cnum-1].get())
		self.canvas.draw()

	def minu(self,n,cnum):
		self.incr(-n, cnum)

	#cursor order not fixed yet
	def temp_fit(self):
		fname = self.get_selected()[0]
		data_t = self.currently_displayed[fname]
		[temp_fit_lower, temp_fit_upper] = self.get_cursor_values(fname, self.currently_displayed)
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
				prelim_fname = fname	+ "average_ln"
				if prelim_fname not in list(self.graph_indexes.keys()):
					self.add_graph(prelim_fname, data[0], data[1])
			except KeyError:
				print("\a")

	def open_popup(self,message,warn):
		top = ctk.CTkToplevel(self)
		if warn:
			top.geometry("1000x100")
			top.title("Warning!")
			tk.Label(top, textvariable = tk.StringVar(value = message),fg="yellow",font = ("courier",50),bg = "#2a2d2e").pack()
		else:
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
				self.open_popup("NOTICE: file already opened", True)

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
			self.open_popup("ERR: invalid data", False)
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
