"""Holds the data and measurements for a single langmuir probe sweep"""
import customtkinter as ctk

class LangmuirSweep:
    """Holds the data and measurements for a single langmuir probe sweep"""
    def __init__(self, name, data, tkinter_frame):
        self.name = name
        self.data = data

        self.file_frame = ctk.CTkFrame(master = tkinter_frame.selector_frame)
        self.checkbox_variable = ctk.IntVar()
        self.checkbox = ctk.CTkCheckBox(master = self.file_frame,
                                        text = "",
                                        variable = self.checkbox_variable)
        self.label = ctk.CTkLabel(master = self.file_frame, text = name.split("/")[-1])

        self.file_frame.pack()
        self.label.grid(row=0, column=0)
        self.checkbox.grid(row=0, column=1)

        self.graph_on_plot = tkinter_frame.plot1.plot(self.data[0], self.data[1], "o", label=name)
