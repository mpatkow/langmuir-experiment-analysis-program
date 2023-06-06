"""Main prgram for the Langmuir Experiment Analysis Program (LEAP)"""
import tkinter as tk
import re
import customtkinter as ctk
import numpy as np
from matplotlib import pyplot as plt
import data_manipulator
import leap_frames
import leap_widgets
import Widget_Redrawer
import file_manager 
class App(ctk.CTk):
    """LEAP APPLICATION"""
    # TODO STANDARDIZE PROBE AREA TO BE STORED IN m3
    # TODO make each sweep be its own instance, with its own parameters such as temp, etc.
    # TODO verify with current versions of dependencies
    # TODO .WIPFILES.txt

    def __init__(self):
        super().__init__()

        # Modes: system (default), light, dark
        ctk.set_appearance_mode("Dark")
        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("blue")
        # Many other themes available, check documentation
        plt.style.use("default")

        try:
            with open("options.txt", "r", encoding="utf-8") as option_file:
                self.options = [l.split("\t")[1][:-1]
                                for l in option_file.readlines()]
            # The atomic mass of the element is entered in options.txt
            self.gas_type = float(self.options[3])/(10**3 * 6.023 * 10**23)
        except IndexError:
            print("options file corrupted, run repair_options in the LEAP console to restore to default")
            self.options = list(range(5))

        self.WIDTH = 1200
        self.HEIGHT = 500
        self.title("Langmuir Experiment Analyzer Program")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.data_analyzer = data_manipulator.data_manipulator(self)
        self.WR = Widget_Redrawer.Widget_Redrawer()

        self.data_type_old = False
        self.currently_displayed = {}
        self.selector_display = {}
        self.graph_indexes = {"cursor1": 0, "cursor2": 1}
        self.lin_log = 0
        self.next_index = 0
        self.legend_visibility = False
        self.cursor_visibility = [tk.IntVar(value=0), tk.IntVar(value=0)]
        self.fit_bound = [tk.IntVar(value=0), tk.IntVar(value=0)]
        self.cursor_positions = []
        self.temperature = tk.StringVar(value="NaN")
        self.floating_potential = tk.DoubleVar()
        self.debye_length = tk.DoubleVar()
        self.density = tk.DoubleVar()
        self.probe_area = 10**(-2) 
        self.probe_radius = tk.DoubleVar()
        self.normal_vp = tk.DoubleVar()
        self.bounds = [tk.IntVar(value=0), tk.IntVar(
            value=0), tk.IntVar(value=0), tk.IntVar(value=0)]
        self.bounds1 = tk.StringVar(
            value=str(self.bounds[0].get()) + " to " + str(self.bounds[1].get()))
        self.bounds2 = tk.StringVar(
            value=str(self.bounds[2].get()) + " to " + str(self.bounds[3].get()))
        self.ecurr_view = False
        self.console_input_var = tk.StringVar()
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

        # TODO remove xy_split as an instance variable of the main LEAP
        self.FM = file_manager.FileManager(self, self.xy_split)

        leap_frames.LEAP_Frames(self)
        leap_widgets.LEAP_Buttons(self)
        self.WR.redraw_widgets(self)

        self.console.tag_config('redtag', background="red", foreground="black")
        self.console.tag_config(
            'yellowtag', background="yellow", foreground="black")

        #self.add_commands()

    def hide_cursor(self, n):
        """Toggle the visibility of the n-th cursor"""
        cursor = getattr(self, f"cursor{n}")
        if cursor.get_linestyle() == "None":
            cursor.set_linestyle("solid")
        else:
            cursor.set_linestyle("None")

        self.canvas.draw()

    def get_cursor_values(self, graph):
        """
        Takes the values of the cursors (which are in volts),
        and returns the INDEX of the closest points
        """
        lower_abs = np.absolute(graph.data[0] - self.fit_bound[0].get())
        upper_abs = np.absolute(graph.data[0] - self.fit_bound[1].get())
        return sorted([np.where(upper_abs == np.min(upper_abs))[0][0],
                       np.where(lower_abs == np.min(lower_abs))[0][0]])

    # TODO make console file/module
    def console_input_receive(self):
        command = self.console_input_var.get()
        self.console_input_var.set("")

    def change_scrolling_mode(self, new_mode):
        """
        Sets the mode of the tkinter canvas to either zoom or pan mode, as specified by new_mode.
        """
        moving_function = getattr(self.fig.canvas.toolbar, new_mode)
        moving_function()
        self.console.configure(state="normal")
        self.console.tag_config('info', background="blue", foreground="black")
        self.console.insert(tk.END, f"Graph set to {new_mode} mode\n", 'info')
        self.console.see("end")
        self.console.configure(state="disabled")

    # TODO fix the standardization and the documentation
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
            print(button_function(fname, options_list))
        if expected_files_type == 3:
            for graph in self.FM.get_selected():
                button_function = getattr(self.data_analyzer, f"{button}")
                print(button_function(graph,options_list))
        else:
            if len(self.FM.get_selected()) == 0:
                self.open_popup("no file selected", "yellow", "NOTICE")
            elif len(self.FM.get_selected()) > 1 and expected_files_type == 1:
                self.open_popup(
                    "this function only accepts one set of data", "yellow", "NOTICE")
            else:
                for graph in self.FM.get_selected():
                    button_function = getattr(self.data_analyzer, f"{button}")
                    returned_functions = button_function(graph, options_list)
                    for function in list(returned_functions):
                        self.FM.add_file(self.get_next_name(
                            graph.name), function)

    def toggle_legend(self):
        """Toggle the visibility of the legend"""
        if self.legend_visibility:
            self.legend_visibility = False
            self.plot1.get_legend().remove()
        else:
            self.legend_visibility = True
            l = [name.split("/")[-1] for name in self.FM.currently_displayed_names]
            l.insert(0,"_cursor1")
            l.insert(0,"_cursor2")
            self.plot1.legend(l)
        self.canvas.draw()

    def toggle_graph_scale(self):
        """Toggles the graph mode between linear and logarithmic (y-axis)"""
        if self.lin_log == 0:
            self.lin_log = 1
            self.plot1.set_yscale("log")
        elif self.lin_log == 1:
            self.lin_log = 0
            self.plot1.set_yscale("linear")
        self.canvas.draw()

    # TODO error test this
    def rescale(self):
        """Rescales the tkinter matplotlib frame to contain the selected graphs"""
        xs = []
        ys = []
        for selected_graph in self.FM.get_selected():
            xs.extend(list(selected_graph.data[0]))
            ys.extend(list(selected_graph.data[1]))

        xs = [xss for xss in xs if str(xss) != 'nan']
        ys = [yss for yss in ys if str(yss) != 'nan']

        try:
            minxs = float(min(xs))
            minys = float(min(ys))
            maxxs = float(max(xs))
            maxys = float(max(ys))

            self.plot1.set_xlim(minxs, maxxs)
            self.plot1.set_ylim(minys, maxys)
            self.canvas.draw()

        except ValueError:
            pass

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

    def open_popup(self, message, color, name):
        self.console.configure(state="normal")
        if color == "red":
            self.console.insert(
                tk.END, "[" + name.upper() + "] " + message + "\n", "redtag")
        if color == "yellow":
            self.console.insert(
                tk.END, "[" + name.upper() + "] " + message + "\n", "yellowtag")
        if color == "":
            self.console.insert(
                tk.END, "[" + name.upper() + "] " + message + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    #FIXME does not always work
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
            i += 1

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
