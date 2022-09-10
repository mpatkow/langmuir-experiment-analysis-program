import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class LEAP_Frames:
        def __init__(self, tkinter_frame):
            tkinter_frame.left_frame = ctk.CTkFrame()
            tkinter_frame.right_frame = ctk.CTkFrame()

            tkinter_frame.graph_frame = ctk.CTkFrame(master = tkinter_frame.left_frame) 	# Holds the graph
            tkinter_frame.adding_frame = ctk.CTkFrame(master = tkinter_frame.left_frame)	# Holds the controls for adding and removing files from the graph.


            tkinter_frame.control_frame = ctk.CTkFrame(master = tkinter_frame.right_frame, border_width = 2)# Holds the controls for manipulating the graphs
            tkinter_frame.middle_frame = ctk.CTkFrame(master = tkinter_frame.right_frame)
            tkinter_frame.selector_frame = ctk.CTkFrame(master = tkinter_frame.middle_frame)
            tkinter_frame.select_all_frame = ctk.CTkFrame(master = tkinter_frame.selector_frame)

            tkinter_frame.options_frame = ctk.CTkFrame(master = tkinter_frame.control_frame)
            tkinter_frame.math_frame = ctk.CTkFrame(master = tkinter_frame.control_frame)
            tkinter_frame.useless_frame  = ctk.CTkFrame(master = tkinter_frame.control_frame)

            tkinter_frame.cursor_frame = ctk.CTkFrame(master = tkinter_frame.options_frame)

		    # The figure that will contain the plot and adding the plot

            tkinter_frame.fig = Figure(figsize = (int(tkinter_frame.options[0]),int(tkinter_frame.options[0])), dpi = 100)
            tkinter_frame.plot1 = tkinter_frame.fig.add_subplot(111)
            tkinter_frame.canvas = FigureCanvasTkAgg(tkinter_frame.fig, master = tkinter_frame.graph_frame)
            tkinter_frame.canvas.get_tk_widget().pack()

            tkinter_frame.toolbar = NavigationToolbar2Tk(tkinter_frame.canvas, tkinter_frame.useless_frame)
            tkinter_frame.toolbar.update()
            tkinter_frame.cursor1 = tkinter_frame.plot1.axvline(x=tkinter_frame.fit_bound[0].get(),linestyle = "None")
            tkinter_frame.cursor2 = tkinter_frame.plot1.axvline(x=tkinter_frame.fit_bound[1].get(),linestyle = "None")
            tkinter_frame.canvas.draw()
            tkinter_frame.results_frame = ctk.CTkFrame(master = tkinter_frame.middle_frame)
            tkinter_frame.temperature_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)

            tkinter_frame.normal_plasma_potential_method_frame = ctk.CTkFrame(master = tkinter_frame.math_frame)
