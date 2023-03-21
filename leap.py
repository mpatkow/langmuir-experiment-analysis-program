import tkinter as tk
import re
import math
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
from scipy import interpolate as itp
import numpy as np
from matplotlib import pyplot as plt
import data_manipulator
import LEAP_Frames
import LEAP_Buttons
import Widget_Redrawer

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")	     # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        plt.style.use("default")             # Many other themes available, check matplotlib documentation

        try:
            option_file = open("options.txt", "r")
            self.options = [l.split("\t")[1][:-1] for l in option_file.readlines()]
            option_file.close()
        except:
            print("options file corrupted, run repair_options in the LEAP console to restore to default")
            self.options = [5]

        self.WIDTH = 1200 
        self.HEIGHT = 500 
        self.title("Langmuir Experiment Analyzer Program")
        self.geometry("%ix%i" % (self.WIDTH, self.HEIGHT))

        self.data_analyzer = data_manipulator.data_manipulator(self)
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
        self.temperature				= tk.StringVar(value = "NaN")
        self.floating_potential		 = tk.DoubleVar()
        self.debye_length			   = tk.DoubleVar()
        self.density					= tk.DoubleVar()
        self.probe_area				 = 0 
        try:
            self.gas_type				   = float(self.options[3])/(10**3 * 6.023 * 10**23) # The atomic mass of the element is entered in options.txt
        except:
            print("options file corrupted, run repair_options in the program console to restore to default")
        self.probe_radius			   = tk.DoubleVar()
        self.normal_vp				  = tk.DoubleVar()
        self.bounds					 = [tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0)]
        self.bounds1					= tk.StringVar(value = str(self.bounds[0].get()) + " to " + str(self.bounds[1].get()))
        self.bounds2					= tk.StringVar(value = str(self.bounds[2].get()) + " to " + str(self.bounds[3].get()))
        self.elementary_charge          = 1.60217663 * 10 ** (-19)
        self.ecurr_view					= False
        self.console_input_var              = tk.StringVar()
        self.valid_commands = {}
        

        # The normal format this program reads for langmuir sweeps is	  xvalue xy_split yvalue newlinecharacter		   
        # The old format is a continuous, one line list of x1,y1,x2,y2, ...
        # Other data formats might be added in the future
        # The separator in the normal data format can be modified by changing the xy_split variable in the options file. This defaults to a tab (\t)
        try:
            if self.options[2] == "True":
                self.data_type_old = True
            if self.options[4] == "True":
                self.ecurr_view = True
            if self.options[1] == "\\t":
                self.xy_split = "\t"
            else:
                self.xy_split = self.options[1]
        except:
            print("options file corrupted, run repair_options to restore to default")


        LEAP_Frames.LEAP_Frames(self)
        LEAP_Buttons.LEAP_Buttons(self)
        self.WR.redraw_widgets(self)

        self.console.tag_config('redtag', background="red", foreground="black")
        self.console.tag_config('yellowtag', background="yellow", foreground="black")

        self.add_commands()

    def hide_cursor(self, n):
        """Toggle the visibility of the n-th cursor"""
        cursor = getattr(self, f"cursor{n}")
        if cursor.get_linestyle() == "None":
            cursor.set_linestyle("solid")
        else:
            cursor.set_linestyle("None")

        self.canvas.draw()

    #TODO make more sensible
    def get_cursor_values(self,fname, data_t):
        """
        Returns the current values of the cursors.
        """
        data_t = self.currently_displayed[fname]
        lower_abs = np.absolute(data_t[0] - self.fit_bound[0].get())
        upper_abs = np.absolute(data_t[0] - self.fit_bound[1].get())
        return sorted([np.where(upper_abs == np.min(upper_abs))[0][0],np.where(lower_abs == np.min(lower_abs))[0][0]])

    def hide_graph(self):
        for a in self.get_selected():
            fname = a 
            if self.plot1.get_lines()[self.graph_indexes[fname]].get_marker() != None:
                self.plot1.get_lines()[self.graph_indexes[fname]].set_marker(None)
                self.canvas.draw()
            else:
                self.plot1.get_lines()[self.graph_indexes[fname]].set_marker("o")
                self.canvas.draw()

    # TODO: move this file to the Options.py file
    def fix_options(self):
        f = open("options.txt", "w")
        f.write("windowsize:\t1\n")
        f.write("xyseparator:\t\\t\n")
        f.write("datatype:\tFalse\n")
        f.write("gastype:\t40.0\n")
        f.write("ecurr_view:\tFalse\n")
        f.close()
        print("Options file fixed, restart the program to complete the process") 

    def console_input_receive(self):
        self.console.configure(state="normal")
        self.console_command(self.console_input_var.get())
        self.console.insert(tk.END, "> " + self.console_input_var.get() + "\n")
        self.console_input_var.set("")
        self.console.see("end")
        self.console.configure(state="disabled")

    # TODO: Add the commands to a file
    # FIXME: commands broken with the new button handling method
    def add_commands(self):
        self.valid_commands["explorer"] = ["file_browser",[],[]]
        self.valid_commands["savgol"] = ["savgol",["winlen", "polyorder"],[53,3]]
        self.valid_commands["boxav"] = ["box_average",[],[]]
        self.valid_commands["spline"] = ["spline_extrapolate",["p"],[1000]]
        self.valid_commands["average"] = ["average",[],[]]
        self.valid_commands["repair_options"] = ["fix_options",[],[]]
        self.valid_commands["delete"] = ["delete_file",[],[]]
        self.valid_commands["zoom"] = ["zoomfunc",[],[]]
        self.valid_commands["pan"] = ["panfunc",[],[]]
        self.valid_commands["save"] = ["save_data",[],[]]
        self.valid_commands["saveimage"] = ["save_image_data",[],[]]
        self.valid_commands["settings"] = ["open_help_and_options",[],[]]
        self.valid_commands["derivative"] = ["derivative",["o"],[1]]
        self.valid_commands["power"] = ["raiseto",["o"],[2]]
        self.valid_commands["abs"] = ["absolute_v",[],[]]
        self.valid_commands["rescale"] = ["rescale",[],[]]
        self.valid_commands["isat"] = ["basic_isat",[],[]]
        self.valid_commands["ln"] = ["natural",[],[]]
        self.valid_commands["trim"] = ["trim",[],[]]
        self.valid_commands["hide"] = ["hide_graph",[],[]]
        self.valid_commands["gettemp"] = ["temperature_value",[],[]]
        self.valid_commands["settemp"] = ["set_temp",["t"],[0]]

    def get_option_values(self, command): 
        # needs ERROR messages
        command_name = command.split(" ")[0]
        command_options_and_values = {}
        for command_chunk in command.split("-")[1:]:
            command_options_and_values[command_chunk.split()[0]] = command_chunk.split()[1:] 
        return command_name,command_options_and_values

    def console_command(self, ctxt):
        cn, co = self.get_option_values(ctxt)
        if cn in self.valid_commands:
            fixed_options = self.valid_commands[cn][2][:]
            for o in co.keys():
                try:
                    ii = self.valid_commands[cn][1].index(o)
                    fixed_options[ii] = co[o][0]
                except:
                    print("not a valid optoin")

            cmd = "self."
            cmd += self.valid_commands[cn][0]
            cmd += "("
            for o in fixed_options:
                cmd += str(o)
                cmd += ","
            if cmd[-1] == ",":
                cmd = cmd[:-1]
            cmd += ")"

            eval(cmd)


    def basic_density(self):
        fname = self.get_selected()[0]
        isat_value = abs(self.currently_displayed[fname][1][10])
        #ne = isat_value/(self.elementary_charge * self.probe_area * 10**(-3)) * (self.gas_type * 2 * math.pi / (float(self.temperature.get().split(' ')[0]) * self.elementary_charge) ) ** 0.5
        ne = isat_value/(self.elementary_charge * self.probe_area * 10**(-3)) * (self.gas_type * 2 * math.pi / (float(input("Temperature: ")) * self.elementary_charge) ) ** 0.5
        print(ne)

        #fname = self.get_selected()[0]
        #newfname = self.get_next_name(fname)
        #data = self.data_analyzer.average(data_to_average)
        #self.add_graph(newfname, data[0], data[1])


    #FIXED
    def probe_area_update(self):
        try:
            self.probe_area = self.probe_area_sef.get_value()
            print("Set the probe area to: %f square cm." % self.probe_area)
        except:
            self.open_popup("No value entered for probe area", "yellow", "NOTICE")

    #PRELIM FIX, NOT CHECKED
    def save_data(self):
        if self.check_selected_files() == 1:
            fname = self.get_selected()[0]
            data = self.currently_displayed[fname]
            data_to_write = ""
            for i in range(len(data[0])):
                if self.data_type_old == False:
                    data_to_write += str(data[0][i])
                    data_to_write += self.xy_split
                    data_to_write += str(data[1][i])
                    data_to_write += "\n"
                else:
                    data_to_write += str(data[0][i])
                    data_to_write += "," 
                    data_to_write += str(data[1][i])
                    data_to_write += ","

            data_to_write = data_to_write[:-1]
            name_to_write_to = asksaveasfilename(initialfile = "", defaultextension=".txt", filetypes=[("Text Files","*.txt"),("Csv Files", "*.csv"), ("All Files", "*.*")])
            try:
                f = open(name_to_write_to, "w")
                f.write(data_to_write)
                f.close()
            except FileNotFoundError:
                pass

    #PRELIM FIX, NOT CHECKED
    def save_image_data(self):
        fname = asksaveasfilename(initialfile = "", defaultextension=".png", filetypes=[("Png Files","*.png"),("Jpg Files", "*.jpg"), ("All Files", "*.*")])
        if fname is None:
            return
        self.fig.savefig(fname,dpi = plt.gcf().dpi)
        self.canvas.draw()

    # incomplete
    def plasma_potential(self):
        fname = self.get_selected()[0]
        asdfasdf = self.data_analyzer.plasma_potential(self.currently_displayed[fname])
        print(asdfasdf)
        return asdfasdf

    # incomplete
    def eedf(self):
        fname = self.get_selected()[0]
        vp = float(input("V_p?: "))
        eexvals, ee = self.data_analyzer.druyvesteyn(self.currently_displayed[fname],vp, 4.17 * 10**(-6))
        self.add_graph(fname + "_ee", eexvals, ee)

    def druyvesteyn_temperature(self):
        fname = self.get_selected()[0]
        data = self.currently_displayed[fname]
        [temp_fit_lower, temp_fit_upper] = self.get_cursor_values(fname, self.currently_displayed)
        print(self.data_analyzer.druyvesteyn_temperature(data, temp_fit_lower, temp_fit_upper))

    def spline_extrapolate(self,points=1000):
        points = int(points)
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE") 
        for fname in self.get_selected():
            mytck,myu=itp.splprep([self.currently_displayed[fname][0],self.currently_displayed[fname][1]],k=5, s=0)
            xnew,ynew= itp.splev(np.linspace(0,1,points),mytck)
            newfname = self.get_next_name(fname)
            if newfname not in list(self.graph_indexes.keys()):
                self.add_graph(newfname, xnew, ynew)

    def change_scrolling_mode(self, new_mode):
        """
        Sets the mode of the tkinter canvas to either zoom or pan mode, as specified by new_mode.
        """
        moving_function = getattr(self.fig.canvas.toolbar, new_mode)
        moving_function()
        self.console.configure(state="normal")
        self.console.tag_config('info', background="blue", foreground="black")
        self.console.insert(tk.END, f"Graph set to {new_mode} mode\n",'info')
        self.console.see("end")
        self.console.configure(state="disabled")

    def button_handler(self, button, options_list, expected_files_type):
        """ 
        Handle the click of a button by calling the corresponding method. 
        If no file is selected, display a popup message and return.
        Otherwise, call the method corresponding to `button`,
        passing in each selected file and adding the returned functions to the graph.

        If expected_files is 0, this indicates a function that may take multiple sets of data,
        but the command is executed for each function seperately
        If expected_files is 1, this indicates a function that only takes one set of data.
        If expected_files is 2, this indicates a function that does not take any data. 
        It only returns/modifies a value or variable.
        
        Parameters:
            button (str): The name of the button that was clicked.
            expected_files_type (int): The type of files the button's function expects
           
        Returns:
            None.
        """
        if expected_files_type == 2:
            button_function = getattr(self.data_analyzer, f"{button}")
            button_function(fname, options_list)
        else:
            if len(self.get_selected()) == 0:
                self.open_popup("no file selected", "yellow", "NOTICE")
            elif len(self.get_selected()) > 1 and expected_files_type == 1:
                self.open_popup("this function only accepts one set of data", "yellow", "NOTICE")
            else:
                for fname in self.get_selected():
                    button_function = getattr(self.data_analyzer, f"{button}")
                    returned_functions = button_function(fname, options_list)
                    for function in list(returned_functions):
                        self.add_graph(self.get_next_name(fname), function[0], function[1])


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
        
        try:
            minxs = float(min(xs))
            minys = float(min(ys))
            maxxs = float(max(xs))
            maxys = float(max(ys))

            self.plot1.set_xlim(minxs,maxxs)
            self.plot1.set_ylim(minys,maxys)
            self.canvas.draw()
        except:
            pass

    def get_selected(self):
        selected = []
        for key in self.selector_display:
            if self.selector_display[key][0].winfo_children()[1].get() == 1:
                selected.append(key)
        return selected

    def trim(self):
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE")
        else:
            fname = self.get_selected()[0]
            data_t = self.currently_displayed[fname]
            [xmin, xmax] = self.get_cursor_values(fname, data_t)
            newfname = self.get_next_name(fname)
            self.add_graph(newfname, self.currently_displayed[fname][0][xmin:xmax], self.currently_displayed[fname][1][xmin:xmax])

    def box_average(self):
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE")
        for fname in self.get_selected():
            try:
                data = self.data_analyzer.box_average(self.currently_displayed[fname])
                newfname = self.get_next_name(fname)
                self.add_graph(newfname, data[0], data[1])
            except KeyError:
                print("\a")

    def savgol(self, o1=53, o2=3):
        o1 = int(o1)
        o2 = int(o2)
        if o1 % 2 == 0:
            o1 += 1
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE")
        for fname in self.get_selected():
            smoothed = self.data_analyzer.savgol_smoothing(self.currently_displayed[fname],o1,o2)
            newfname = self.get_next_name(fname)
            if newfname not in list(self.graph_indexes.keys()):
                self.add_graph(newfname, self.currently_displayed[fname][0], smoothed)

    # make different sized files be comaptible with average
    def average(self):
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE")
        else:
            data_to_average = []
            for fname in self.get_selected():
                data_to_average.append(self.currently_displayed[fname])

            fname = self.get_selected()[0]
            newfname = self.get_next_name(fname)
            try:
                data = self.data_analyzer.average(data_to_average)
                if newfname not in list(self.graph_indexes.keys()):
                    self.add_graph(newfname, data[0], data[1])
            except:
                self.open_popup("files not same size", "yellow", "NOTICE")

    def incr(self, n, cnum):
        """
        Increments the value of the specified cursor by the given amount.

        Parameters:
        n (int): The amount by which to increment the cursor.
        cnum (int): The number of the cursor to increment (either 1 or 2).

        Returns:
        None
        """
        self.fit_bound[cnum-1].set(self.fit_bound[cnum-1].get()+n)
        if cnum == 1:
            self.cursor1.set_xdata(self.fit_bound[cnum-1].get())
        if cnum == 2:
            self.cursor2.set_xdata(self.fit_bound[cnum-1].get())
        self.canvas.draw()

    def temp_fit(self):
        if len(self.get_selected()) == 0:
            self.open_popup("no file selected", "yellow", "NOTICE")
        else:
            fname = self.get_selected()[0]
            data_t = self.currently_displayed[fname]
            [temp_fit_lower, temp_fit_upper] = self.get_cursor_values(fname, self.currently_displayed)
            temps = []
            for upper_bound in range(temp_fit_lower, temp_fit_upper+1):
                for lower_bound in range(temp_fit_lower, upper_bound):
                    if abs(lower_bound-upper_bound) == 1:
                        pass
                    else:
                        if (temp_fit_lower - temp_fit_upper) > 10:
                            if upper_bound % 5 == 0 and lower_bound % 5 == 0:
                                m,b = np.polyfit(data_t[0][lower_bound:upper_bound], data_t[1][lower_bound:upper_bound], 1)
                                temps.append(1/m)
                        else:
                            m,b = np.polyfit(data_t[0][lower_bound:upper_bound], data_t[1][lower_bound:upper_bound], 1)
                            temps.append(1/m)

            temps = np.array(temps)
            av = np.average(temps)
            std = np.std(temps)

            self.temperature.set(str(av) + " +- " + str(std))

            final_temp_statement = u"Temperature: %f \u00b1 %f eV" % (av, std)

            self.open_popup(final_temp_statement, "", "RESULT")

    def temperature_value(self):
        statement = "The temperature register is currently set to " + self.temperature.get() + " eV"
        self.open_popup(statement, "", "INFO")

    def set_temp(self, temp_to_set):
        self.temperature.set(str(temp_to_set) + " +- " + "0")

    def derivative(self,order=1):
        order = int(order)
        for fname in self.get_selected():
            try:
                data = self.data_analyzer.derivative(self.currently_displayed[fname],order)
                fname = self.get_selected()[0]
                newfname = self.get_next_name(fname)
                sq = np.square(self.currently_displayed[fname][1])
                self.add_graph(newfname, data[0], data[1])
            except KeyError:
                print("\a")

    def natural(self):
        for fname in self.get_selected():
            try:
                data = [self.currently_displayed[fname][0],np.log(self.currently_displayed[fname][1])]
                newfname = self.get_next_name(fname)
                sq = np.square(self.currently_displayed[fname][1])
                self.add_graph(newfname, data[0], data[1])
            except KeyError:
                print("\a")














    def open_popup(self,message,color,name):
        self.console.configure(state="normal")
        if color == "red":
            self.console.insert(tk.END, "[" + name.upper() + "] " + message + "\n", "redtag")
        if color == "yellow":
            self.console.insert(tk.END, "[" + name.upper() + "] " + message + "\n", "yellowtag")
        if color == "":
            self.console.insert(tk.END, "[" + name.upper() + "] " + message + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def file_browser(self):
        fnames = tk.filedialog.askopenfilenames(initialdir = ".", title = "Select a File", filetypes = [("csv files", "*.csv"),("data files", "*.txt"),  ("all files","*.*")])
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
                self.open_popup("file already opened", "yellow", "NOTICE")

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

            #avv = np.average(y)
            #for i in range(1,len(y)-1):
            #    if abs(y[i]-avv) >= 0.1:
            #        y[i] = (y[i+1] + y[i-1])/2

            return x,y
            
        except:
            self.open_popup("invalid data", "red", "ERROR")
            return None,None

    def add_graph(self, f, x, y):
        self.currently_displayed.update({f: [x,y]})

        file_frame = ctk.CTkFrame(master = self.selector_frame)

        cb_value = tk.IntVar()

        splittedfname = f.split("/")[-1]
        if self.next_index == 0:
            label = ctk.CTkLabel(master = file_frame, text = splittedfname)
        else: 
            label = ctk.CTkLabel(master = file_frame, text = splittedfname)
        cb = ctk.CTkCheckBox(master = file_frame, text = "", variable = cb_value)

        self.selector_display.update({f: [file_frame,cb_value]})
        self.update_next_index()
        self.graph_indexes.update({f: self.next_index})

        self.plot1.plot(x,y,'o')
        self.canvas.draw()

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

    def get_next_name(self, prelim):
        """
        Returns the next avaialable filename, found as follows
        - consider "filename12.txt"
        - the extension is ignored (in this case .txt)
        - the final number (consecutive string of numerical elements) is taken from the name (in this case 12)
        - the rest of the string can be called the name (in this case filename)
        
        Now the other existing files are compared to the NAME only.
        Final number takes next lowest existing value.
        Returns name + number + . + extension
        
        WARNING! Alters the final number, may cause unintended bugs. 
        For example, if the filename is "sweep1/13/2005.txt", the next filename will probably return "sweep1/13/2006.txt".
        """
        existing_extensions = []

        ntp = prelim.split(".")
        ntp_primary = ntp[0]
        ntp_extension = ntp[1]
        ntp_number = self.get_trailing_nums(ntp_primary)
        ntp_nonumber = self.get_beginning_string(ntp_primary)

        if ntp_number != None:
            existing_extensions.append(int(ntp_number))

        for f in self.selector_display.keys():
            f_primary = f.split(".")[0]
            f_number = self.get_trailing_nums(f_primary)
            f_nonumber = self.get_beginning_string(f_primary)

            if ntp_nonumber == f_nonumber:
                    existing_extensions.append(f_number)

        i = 0
        while i in existing_extensions:
            i+=1

        return ntp_nonumber + str(i) + "." + ntp_extension   

    def get_trailing_nums(self, numtosearch):
        """
        Helper function for get_next_name

        Function returns the last set of numerical digits in a given string
        """
        a = re.search(r'\d+$', numtosearch)
        return int(a.group()) if a else None

    def get_beginning_string(self, stringtosearch):
        """
        Helper function for get_next_name

        Given a string, return the substring that starts at the beginning of the string
        and ends at the last non-numeric character in the string.
        """
        numericals = "0123456789"
        for i in range(len(stringtosearch)-1, -1, -1):
            if stringtosearch[i] not in numericals:
                return stringtosearch[0:i+1]     

if __name__ == "__main__":
    app = App()
    app.mainloop()
