import tkinter as tk

class Widget_Redrawer:
    def redraw_widgets(self, self_of_parent):
        self_of_parent.adding_frame.pack(fill=tk.X)
        self_of_parent.main_frame.pack(fill=tk.BOTH,expand=True)

        self_of_parent.main_frame.grid_columnconfigure(0,weight=4)
        self_of_parent.main_frame.grid_columnconfigure(1,weight=1)
        self_of_parent.main_frame.grid_columnconfigure(2,weight=2)
        self_of_parent.main_frame.grid_rowconfigure(0,weight=1)
        self_of_parent.canvas.get_tk_widget().grid(row=0, column = 0, sticky = "nswe")
        self_of_parent.middle_frame.grid(row=0, column = 1, sticky = "nswe")
        self_of_parent.right_frame.grid(row=0, column = 2, sticky = "nswe")

        # Adding Frame options at the top of the window
        self_of_parent.explorer_button.grid(row=0, column=0)
        self_of_parent.deletion_button.grid(row=0, column=1)
        self_of_parent.save_button.grid(row=0, column=2)
        self_of_parent.save_image_button.grid(row=0, column=3)
        self_of_parent.open_help_and_options_button.grid(row=0, column=4)

        self_of_parent.zoom_button.grid(row=0, column=5, sticky = "nsew",padx=(50,0))
        self_of_parent.pan_button.grid(row=0, column=6, sticky = "nsew")
        self_of_parent.scale_button.grid(row=0, column=7, sticky = "nsew")
        self_of_parent.legend_button.grid(row=0, column=8, sticky = "nsew")
        self_of_parent.rescale_button.grid(row=0, column=9, sticky = "nsew")

        self_of_parent.right_frame.grid_rowconfigure(0,weight=3)
        self_of_parent.right_frame.grid_rowconfigure(1,weight=2)
        self_of_parent.right_frame.grid_columnconfigure(0,weight=1)
        self_of_parent.buttons_frame.grid(row=0,column=0,sticky="nswe") 
        self_of_parent.console_frame.grid(row=1,column=0,sticky="nswe")

        self_of_parent.console.pack(expand = True, fill=tk.BOTH)
        self_of_parent.console_input_frame.grid_rowconfigure(0,weight=1)
        self_of_parent.console_input_frame.grid_columnconfigure(0,weight=5)
        self_of_parent.console_input_frame.grid_columnconfigure(1,weight=1)
        self_of_parent.console_input_frame.pack(expand=True, fill=tk.BOTH)
        self_of_parent.console_input.grid(row=0,column=0,sticky="ew")
        self_of_parent.console_input_button.grid(row=0,column=1,sticky="ew")

        self_of_parent.middle_frame.grid_rowconfigure(0, weight = 4)
        self_of_parent.middle_frame.grid_rowconfigure(1, weight = 1)
        self_of_parent.middle_frame.grid_columnconfigure(0, weight = 1)
        self_of_parent.selector_frame.grid(row=0, column=0, sticky = "nswe")
        self_of_parent.cursor_frame.grid(row=1, column=0, sticky = "nswe")

        self_of_parent.cursor_frame.grid_rowconfigure(0, weight = 1)
        self_of_parent.cursor_frame.grid_rowconfigure(1, weight = 1)
        self_of_parent.cursor_frame.grid_rowconfigure(2, weight = 1)
        self_of_parent.cursor_frame.grid_columnconfigure(0, weight = 2)
        self_of_parent.cursor_frame.grid_columnconfigure(1, weight = 2)
        self_of_parent.cursor_frame.grid_columnconfigure(2, weight = 1)
        self_of_parent.cursor_frame.grid_columnconfigure(3, weight = 2)
        self_of_parent.cursor_frame.grid_columnconfigure(4, weight = 2)
        self_of_parent.cursor_frame.grid_columnconfigure(5, weight = 1)
        self_of_parent.cursor_label.grid(row=0, column=3, sticky = "nswe")
        px = 2
        py = 2
        self_of_parent.minus_button_l.grid(row=1,column=0, sticky = "nswe",padx=px,pady=py)
        self_of_parent.minus_button.grid(row=1,column=1, sticky = "nswe",padx=px,pady=py)
        self_of_parent.plus_button.grid(row=1,column=3, sticky = "nswe",padx=px,pady=py)
        self_of_parent.plus_button_l.grid(row=1,column=4, sticky = "nswe",padx=px,pady=py)
        self_of_parent.fit_counter.grid(row=1,column=2, sticky = "nswe",padx=px,pady=py)
        self_of_parent.cursor_show_button.grid(row=1,column=5, sticky = "nswe",padx=px,pady=py)
        self_of_parent.minus_button_l_2.grid(row=2,column=0, sticky = "nswe",padx=px,pady=py)
        self_of_parent.minus_button_2.grid(row=2,column=1, sticky = "nswe",padx=px,pady=py)
        self_of_parent.plus_button_2.grid(row=2,column=3, sticky = "nswe",padx=px,pady=py)
        self_of_parent.plus_button_l_2.grid(row=2,column=4, sticky = "nswe",padx=px,pady=py)
        self_of_parent.fit_counter_2.grid(row=2,column=2, sticky = "nswe",padx=px,pady=py)
        self_of_parent.cursor_show_button_2.grid(row=2,column=5, sticky = "nswe",padx=px,pady=py)

        self_of_parent.select_all_frame.pack()
        self_of_parent.select_all_label.grid(row=0, column=0)
        self_of_parent.select_all_button.grid(row=0, column=1)
        
        # BUTTONS FRAME
        self_of_parent.b1_frame.grid(row=0, column=0, sticky="nswe")
        self_of_parent.b2_frame.grid(row=0, column=1, sticky="nswe")
        self_of_parent.b3_frame.grid(row=0, column=2, sticky="nswe")
        self_of_parent.b4_frame.grid(row=0, column=3, sticky="nswe")
        self_of_parent.buttons_frame.grid_rowconfigure(0, weight = 1)
        self_of_parent.buttons_frame.grid_columnconfigure(0, weight = 1)
        self_of_parent.buttons_frame.grid_columnconfigure(1, weight = 1)
        self_of_parent.buttons_frame.grid_columnconfigure(2, weight = 1)
        self_of_parent.buttons_frame.grid_columnconfigure(3, weight = 1)

        vpad = 2

        # SMOOTHING
        self_of_parent.sorting_label_1.pack(pady=vpad)
        self_of_parent.savgol_button.pack(pady=vpad)
        self_of_parent.box_button.pack(pady=vpad)
        self_of_parent.spline_button.pack(pady=vpad)
        self_of_parent.average_button.pack(pady=vpad)

        # MATH
        self_of_parent.sorting_label_2.pack(pady=vpad)
        self_of_parent.derivative_button.pack(pady=vpad)
        self_of_parent.square_button.pack(pady=vpad)
        self_of_parent.absolute_button.pack(pady=vpad)
        self_of_parent.natural_log_button.pack(pady=vpad)

        # OPERATIONS
        self_of_parent.sorting_label_3.pack(pady=vpad)
        self_of_parent.basic_isat_button.pack(pady=vpad)
        self_of_parent.temperature_button.pack(pady=vpad)
        self_of_parent.eedf_button.pack(pady=vpad)
        self_of_parent.plasma_potential_button.pack(pady=vpad)
        self_of_parent.oml_button.pack(pady=vpad)
        self_of_parent.d_temp_button.pack(pady=vpad)
        self_of_parent.floating_potential_button.pack(pady=vpad)

        # SMOOTHING
        self_of_parent.sorting_label_4.pack(pady=vpad)
        self_of_parent.trim_button.pack(pady=vpad)
        self_of_parent.hide_button.pack(pady=vpad)
"""
        self_of_parent.temperature_frame.pack(fill=tk.X)
        self_of_parent.temperature_button.grid(row = 0, column = 0)
        self_of_parent.temperature_label.grid(row = 0, column = 1)

        self_of_parent.floating_frame.pack(fill=tk.X)
        self_of_parent.floating_potential_button.grid(row = 0, column = 0)
        self_of_parent.floating_label.grid(row = 0, column = 1)

        self_of_parent.debye_frame.pack(fill = tk.X)
        self_of_parent.debye_button.grid(row = 0, column = 0)
        self_of_parent.debye_label.grid(row = 0, column = 1)
        
        self_of_parent.basic_density_sef.put_on_screen()
        self_of_parent.probe_area_sef.put_on_screen()

        self_of_parent.normal_plasma_potential_method_frame.pack()
        self_of_parent.potential_bounds_1_button.grid(row=0,column=0)
        self_of_parent.potential_bounds_1_label.grid(row=0,column=1)
        self_of_parent.potential_bounds_2_button.grid(row=1,column=0)
        self_of_parent.potential_bounds_2_label.grid(row=1,column=1)
        self_of_parent.normal_potential_button.grid(row=2,column=0)
        self_of_parent.normal_potential_label.grid(row=2,column=1)
        """
