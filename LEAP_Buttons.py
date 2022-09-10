import customtkinter as ctk
import SmartEnterField as sef

class LEAP_Buttons:
    def __init__(self, tkinter_frame=False):
        """ RESULTS FRAMES """

        tkinter_frame.temperature_button = ctk.CTkButton(master = tkinter_frame.temperature_frame,
        	command = tkinter_frame.temp_fit,
        	text = u"kT\u2091",
        	height = 30,
        	width = 30)
        tkinter_frame.temperature_label = ctk.CTkLabel(master = tkinter_frame.temperature_frame,
        	textvar = tkinter_frame.temperature)

        tkinter_frame.floating_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)
        tkinter_frame.floating_potential_button = ctk.CTkButton(master = tkinter_frame.floating_frame,
        	command = tkinter_frame.floating,
        	text = "Vf",
        	height = 30,
        	width = 30)
        tkinter_frame.floating_label = ctk.CTkLabel(master = tkinter_frame.floating_frame,
        	textvar = tkinter_frame.floating_potential)
        tkinter_frame.probe_area_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)
        tkinter_frame.probe_area_input = ctk.CTkEntry(master = tkinter_frame.probe_area_frame,
        	width = 120,
        	height = 25,
        	corner_radius = 10)
        tkinter_frame.probe_area_label = ctk.CTkLabel(master = tkinter_frame.probe_area_frame,
        	text = "Ap (cm^2)")
        tkinter_frame.ion_mass_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)
        tkinter_frame.ion_mass_input = ctk.CTkEntry(master = tkinter_frame.ion_mass_frame,
        	width = 120,
        	height = 25,
        	corner_radius = 10)
        tkinter_frame.ion_mass_label = ctk.CTkLabel(master = tkinter_frame.ion_mass_frame,
        	text = "M (kg)")
        tkinter_frame.debye_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)
        tkinter_frame.debye_button = ctk.CTkButton(master = tkinter_frame.debye_frame,
        	command = tkinter_frame.debye,
        	text = u"\u03BB debye",
        	height = 30,
        	width = 30)
        tkinter_frame.debye_label = ctk.CTkLabel(master = tkinter_frame.debye_frame,
        	textvar = tkinter_frame.debye_length)
        tkinter_frame.debye_ratio_frame = ctk.CTkFrame(master = tkinter_frame.results_frame)
        tkinter_frame.debye_ratio_button = ctk.CTkButton(master = tkinter_frame.debye_ratio_frame,
        	command = tkinter_frame.debye_ratio_calculate,
        	text = "e(fix this_):",
        	height = 30,
        	width = 30,
        	fg_color="red")
        tkinter_frame.debye_ratio_label = ctk.CTkLabel(master = tkinter_frame.debye_ratio_frame,
        	textvar = tkinter_frame.debye_ratio_calculate)

        tkinter_frame.basic_density_sef = sef.SmartEnterField(tkinter_frame.results_frame, "bdense", u" m\u207B\u00B3", tkinter_frame.basic_density)
        tkinter_frame.probe_area_sef = sef.SmartEnterField(tkinter_frame.results_frame, "probe area", u" mm \u00B2", tkinter_frame.probe_area_update)


        """ ADDING FRAME """

        tkinter_frame.explorer_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.file_browser,
        	text = "explorer")
        tkinter_frame.deletion_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.delete_file,
                    text = "Delete")
        tkinter_frame.save_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.save_data,
        	text = "save data")
        tkinter_frame.save_image_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.save_image_data,
        	text = "save image")
        tkinter_frame.zoom_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.fig.canvas.toolbar.zoom,
        	text = "zoom")
        tkinter_frame.pan_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.fig.canvas.toolbar.pan,
        	text = "pan")
        tkinter_frame.trim_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
        	command = tkinter_frame.trim,
        	text = "trim")



        tkinter_frame.plus_button = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.incr(1,1),
        	text = ">",
        	width = 5)
        tkinter_frame.plus_button_l = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.incr(10,1),
        	text = ">>",
        	width = 5)
        tkinter_frame.minus_button = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.minu(1,1),
        	text = "<",
        	width = 5)
        tkinter_frame.minus_button_l = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.minu(10,1),
        	text = "<<",
        	width = 5)
        tkinter_frame.plus_button_2 = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.incr(1,2),
        	text = ">",
        	width = 5)
        tkinter_frame.plus_button_l_2 = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.incr(10,2),
        	text = ">>",
        	width = 5)
        tkinter_frame.minus_button_2 = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.minu(1,2),
        	text = "<",
        	width = 5)
        tkinter_frame.minus_button_l_2 = ctk.CTkButton(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.minu(10,2),
        	text = "<<",
        	width = 5)

        tkinter_frame.rescale_button = ctk.CTkButton(master = tkinter_frame.options_frame,
        	command = tkinter_frame.rescale,
        	text = "Rescale")
        tkinter_frame.derivative_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.derivative,
        	text = "f'")
        tkinter_frame.scale_button = ctk.CTkButton(master = tkinter_frame.options_frame,
        	command = tkinter_frame.toggle_graph_scale,
        	text = "lin/log")
        tkinter_frame.legend_button = ctk.CTkButton(master = tkinter_frame.options_frame,
        	command = tkinter_frame.toggle_legend,
        	text = "legend")
        tkinter_frame.box_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.box_average,
        	text = "box average")
        tkinter_frame.select_all_button = ctk.CTkCheckBox(master = tkinter_frame.select_all_frame,
        	command = tkinter_frame.all,
        	variable = tkinter_frame.select_all,
        	text = "")
        tkinter_frame.average_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.average,
        	text = "average")
        tkinter_frame.square_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.square,
        	text = "f^2")
        tkinter_frame.basic_isat_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.basic_isat,
        	text = "basic isat")
        tkinter_frame.basic_isat_button_auto = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.basic_isat_auto,
        	text = "basic isat auto")
        tkinter_frame.savgol_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.savgol,
        	text = "S-G Filter")
        tkinter_frame.spline_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.spline_extrapolate,
        	text = "Spline")
        tkinter_frame.eedf_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.eedf,
        	text = "EEDF",
        	fg_color="red")
        tkinter_frame.plasma_potential_button = ctk.CTkButton(master= tkinter_frame.math_frame,
        	command = tkinter_frame.plasma_potential,
        	text = "plasma potential")
        tkinter_frame.absolute_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.absolute_v,
        	text = "|f|")
        tkinter_frame.natural_log_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.natural,
        	text = "ln")
        tkinter_frame.oml_button = ctk.CTkButton(master = tkinter_frame.math_frame,
        	command = tkinter_frame.oml,
        	text = "oml")

        tkinter_frame.potential_bounds_1_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
            command = tkinter_frame.save_bounds_1,
            text = "Vp bounds 1:")
        tkinter_frame.potential_bounds_1_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
            textvar = tkinter_frame.bounds1)
        tkinter_frame.potential_bounds_2_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
            command = tkinter_frame.save_bounds_2,
            text = "Vp bounds 2:")
        tkinter_frame.potential_bounds_2_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
            textvar = tkinter_frame.bounds2)
        tkinter_frame.normal_potential_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
            command = tkinter_frame.normal_potential,
            text = "NVp:")
        tkinter_frame.normal_potential_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
            textvar = tkinter_frame.normal_vp)


        tkinter_frame.fit_counter = ctk.CTkLabel(master = tkinter_frame.cursor_frame, textvar = tkinter_frame.fit_bound[0])
        tkinter_frame.fit_counter_2 = ctk.CTkLabel(master = tkinter_frame.cursor_frame, textvar = tkinter_frame.fit_bound[1])
        tkinter_frame.cursor_show_button = ctk.CTkCheckBox(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.hide_cursor(1),
        	variable = tkinter_frame.cursor_visibility[0],
        	text = "")
        tkinter_frame.cursor_show_button_2 = ctk.CTkCheckBox(master = tkinter_frame.cursor_frame,
        	command = lambda: tkinter_frame.hide_cursor(2),
        	variable = tkinter_frame.cursor_visibility[1],
        	text = "")

        tkinter_frame.select_all_label = ctk.CTkLabel(master = tkinter_frame.select_all_frame, text = "Select All:")
        tkinter_frame.open_help_and_options_button = ctk.CTkButton(master = tkinter_frame.options_frame,
            command = tkinter_frame.open_help_and_options,
            text = "h&o")
