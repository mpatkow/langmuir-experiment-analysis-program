import tkinter as tk
mode = True
try:
	import customtkinter as ctk
except:
	mode = False

class SmartEnterField:
	def __init__(self, parent_frame, button_label, unit, command_for_button, label_width = 20):
		if mode == True:
			self.variable = tk.DoubleVar(value = 0)
			self.enter_field_frame = ctk.CTkFrame(master = parent_frame)

			self.enter_button = ctk.CTkButton(master = self.enter_field_frame,
			    command = command_for_button,
			    text = button_label,
			    width = 30)
			self.first_entry = ctk.CTkEntry(master = self.enter_field_frame,
				width = 80,
				height = 25,
				corner_radius = 10)
			self.E_label = ctk.CTkLabel(master = self.enter_field_frame,
			    text = " E ",
			    width = 10)
			self.second_entry = ctk.CTkEntry(master = self.enter_field_frame,
				width = 50,
				height = 25,
				corner_radius = 10)
			self.unit_label = ctk.CTkLabel(master = self.enter_field_frame,
			    textvar = tk.StringVar(value = unit),
			    width = label_width)
		else:
			self.variable = tk.DoubleVar(value = 0)
			self.enter_field_frame = tk.Frame(master = parent_frame)

			self.enter_button = tk.Button(master = self.enter_field_frame,
			    command = command_for_button,
			    text = button_label,
			    width = 30)
			self.first_entry = tk.Entry(master = self.enter_field_frame,
				width = 80)
			self.E_label = tk.Label(master = self.enter_field_frame,
			    text = " E ",
			    width = 10)
			self.second_entry = tk.Entry(master = self.enter_field_frame,
				width = 50)
			self.unit_label = tk.Label(master = self.enter_field_frame,
			    textvar = tk.StringVar(value = unit),
			    width = label_width)

	def put_on_screen(self):
		self.enter_field_frame.pack(fill=tk.X)
		self.enter_button.grid(row = 0, column = 0)
		self.first_entry.grid(row = 0, column = 1)
		self.E_label.grid(row = 0, column = 2)
		self.second_entry.grid(row = 0, column = 3)
		self.unit_label.grid(row = 0, column = 4)

	def get_value(self):
		return float(self.first_entry.get()) * 10 ** float(self.second_entry.get())
