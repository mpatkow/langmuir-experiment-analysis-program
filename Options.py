import tkinter as tk
import customtkinter as ctk

#Add a way to adjust options.txt with GUI
class Options:
    def __init__(self, top_level):
        op = ctk.CTkToplevel(top_level)
        op.title("Help & Options")
        op.geometry("%ix%i" % (50,60))

        #option_file = open("options.txt", "r")
        #self.options = [l.split("\t")[1][:-1] for l in option_file.readlines()]
        #option_file.close()


        op.buttons_frame = ctk.CTkFrame()
