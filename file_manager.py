"""File Manager for LEAP"""
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import numpy as np
from matplotlib import pyplot as plt
import langmuir_sweep
class FileManager:
    """Handles harvesting data from files, as well as adding and removing files from the LEAP"""
    def __init__(self, tkinter_frame, xy_split):
        self.tkinter_frame = tkinter_frame
        self.currently_displayed = []
        self.currently_displayed_names = []
        self.xy_split = xy_split
        self.select_all = tk.IntVar()

    def file_browser(self):
        """Allows the user to select file(s) from their computer to upload to LEAP"""
        file_names = tk.filedialog.askopenfilenames(initialdir = ".",
                                                    title = "Select a File",
                                                    filetypes = [("csv files", "*.csv"),
                                                                 ("data files", "*.txt"),
                                                                 ("all files","*.*")])
        for file_name in file_names:
            if file_name not in self.currently_displayed_names:
                self.add_file(file_name)
            else:
                self.tkinter_frame.open_popup("file already opened", "yellow", "NOTICE")

    def add_file(self, file_name, data=None):
        """Adds a new graph to the LEAP"""

        if data is None:
            data = self.get_data(file_name)

        if data[0] is not None and data[1] is not None:
            self.currently_displayed.append(langmuir_sweep.LangmuirSweep(file_name,
                                                                        data,
                                                                        self.tkinter_frame))

            self.currently_displayed_names.append(file_name)

        self.tkinter_frame.canvas.draw()

    def get_data(self, file_name):
        """
        Gets the voltage-current sweep data from the given file
        """
        try:
            data_file = open(file_name, "r", encoding="utf-8")
            raw_data = data_file.readlines()
            data_file.close()

            voltage_values = np.array([float(raw_data[i].split(self.xy_split)[0])
                                       for i in range(len(raw_data))])
            current_values = np.array([float(raw_data[i].split(self.xy_split)[1])
                                       for i in range(len(raw_data))])

            return [voltage_values, current_values]

        except ValueError:
            self.tkinter_frame.open_popup("invalid data", "red", "ERROR")
            return [None, None]

    def delete_file(self):
        """
        Delete the LangmuirSweep instance, the selector instance, and all other 
        things associated with the selected graphs
        """
        for graph in self.get_selected():
            self.currently_displayed.remove(graph)
            self.currently_displayed_names.remove(graph.name)

            graph.graph_on_plot.pop(0).remove()

            graph.file_frame.pack_forget()
            graph.file_frame.destroy()

            del graph

        self.tkinter_frame.canvas.draw()

    def get_selected(self):
        """ Returns a list of every langmuir_sweep that is selected."""
        selected = []
        for graph in self.currently_displayed:
            if graph.checkbox_variable.get() == 1:
                selected.append(graph)
        return selected

    def hide_graphs(self):
        """Hide the selected graph(s)"""
        for graph in self.get_selected():
            for line in graph.graph_on_plot:
                if line.get_marker() is None:
                    line.set_marker("o")
                else:
                    line.set_marker(None)
                self.tkinter_frame.canvas.draw()

    def save_image_data(self):
        """Save an image of the canvas (includes all visibile graphs)"""
        fname = asksaveasfilename(initialfile="", defaultextension=".png", filetypes=[
                                  ("Png Files", "*.png"),
                                  ("Jpg Files", "*.jpg"),
                                  ("All Files", "*.*")])
        if fname is None:
            return
        self.tkinter_frame.fig.savefig(fname, dpi=plt.gcf().dpi)
        self.tkinter_frame.canvas.draw()

    def save_data(self):
        """Save the selected data"""
        for graph in self.get_selected():
            data_to_write = ""
            for i in range(len(graph.data[0])):
                data_to_write += str(graph.data[0][i])
                data_to_write += self.xy_split
                data_to_write += str(graph.data[1][i])
                data_to_write += "\n"

            data_to_write = data_to_write[:-1]
            name_to_write_to = asksaveasfilename(initialfile="",
                                                 defaultextension=".txt",
                                                 filetypes=[
                                                    ("Text Files", "*.txt"),
                                                    ("Csv Files", "*.csv"),
                                                    ("All Files", "*.*")])

            try:
                f = open(name_to_write_to, "w", encoding="utf-8")
                f.write(data_to_write)
                f.close()
            except FileNotFoundError:
                pass

    def select_all_graphs(self):
        """Selects all graphs in the LEAP"""
        v = self.select_all.get()
        for graph in self.currently_displayed:
            graph.checkbox_variable.set(v)
