"""Buttons and Widgets for the LEAP"""
import customtkinter as ctk
import SmartEnterField as sef
import Options

class LEAP_Buttons:
    def __init__(self, tkinter_frame=False):
        """ RESULTS FRAMES """

        tkinter_frame.temperature_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("temperature_fit", [], 3),
                text = "temp fit",
                width=10)
        tkinter_frame.temperature_label = ctk.CTkLabel(master = tkinter_frame.temperature_frame,
                textvariable = tkinter_frame.temperature)

        #tkinter_frame.floating_frame = ctk.CTkFrame(master = tkinter_frame.b3_frame)
        tkinter_frame.floating_potential_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("floating_potential", [], 3),
                text = "Vf",
                height = 30,
                width = 30)
        #tkinter_frame.floating_label = ctk.CTkLabel(master = tkinter_frame.floating_frame,
        #       textvariable = tkinter_frame.floating_potential)

        tkinter_frame.basic_density_sef = sef.SmartEnterField(tkinter_frame.results_frame, "bdense", u" m\u207B\u00B3", lambda: tkinter_frame.button_handler("basic_density", [], 1))
        tkinter_frame.probe_area_sef = sef.SmartEnterField(tkinter_frame.results_frame, "probe area", u" cm \u00B2", lambda: print("Not avaialable ATM"))

        tkinter_frame.console = ctk.CTkTextbox(master = tkinter_frame.console_frame,state="disabled")
        tkinter_frame.console_input = ctk.CTkEntry(master = tkinter_frame.console_input_frame, textvariable = tkinter_frame.console_input_var) 
        tkinter_frame.console_input_button = ctk.CTkButton(master = tkinter_frame.console_input_frame,
                command = tkinter_frame.console_input_receive,
                text = "enter")

        """ ADDING FRAME """

        tkinter_frame.explorer_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.FM.file_browser,
                text = "explorer",
                width=10)
        tkinter_frame.deletion_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.FM.delete_file,
                text = "delete",
                width=10)
        tkinter_frame.save_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.FM.save_data,
                text = "save data")
        tkinter_frame.save_image_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.FM.save_image_data,
                text = "save image")
        tkinter_frame.zoom_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = lambda: tkinter_frame.change_scrolling_mode("zoom"),
                text = "zoom")
        tkinter_frame.pan_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = lambda: tkinter_frame.change_scrolling_mode("pan"),
                text = "pan")
        tkinter_frame.trim_button = ctk.CTkButton(master = tkinter_frame.b4_frame,
                command = lambda: tkinter_frame.button_handler("trim", [], 0),
                text = "trim")


        tkinter_frame.cursor_label = ctk.CTkLabel(master = tkinter_frame.cursor_frame, text = "Cursors:")
        tkinter_frame.plus_button = ctk.CTkButton(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.incr(1,1),
                text = ">",
                width = 5)
        tkinter_frame.plus_button_l = ctk.CTkButton(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.incr(10,1),
                text = ">>",
                width = 5)
        tkinter_frame.minus_button = ctk.CTkButton(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.incr(-1,1),
                text = "<",
                width = 5)
        tkinter_frame.minus_button_l = ctk.CTkButton(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.incr(-10,1),
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
                command = lambda: tkinter_frame.incr(-1,2),
                text = "<",
                width = 5)
        tkinter_frame.minus_button_l_2 = ctk.CTkButton(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.incr(-10,2),
                text = "<<",
                width = 5)


        tkinter_frame.sorting_label_1 = ctk.CTkLabel(master = tkinter_frame.b1_frame,text = "Smoothing:")
        tkinter_frame.sorting_label_2 = ctk.CTkLabel(master = tkinter_frame.b2_frame,text = "Math:",width=10)
        tkinter_frame.sorting_label_3 = ctk.CTkLabel(master = tkinter_frame.b3_frame,text = "Operations:")
        tkinter_frame.sorting_label_4 = ctk.CTkLabel(master = tkinter_frame.b4_frame,text = "Miscellaneous:")


        tkinter_frame.rescale_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.rescale,
                text = "rescale")
        tkinter_frame.derivative_button = ctk.CTkButton(master = tkinter_frame.b2_frame,
                command = lambda: tkinter_frame.button_handler("derivative", [1], 0),
                text = "f'",
                width=10)
        tkinter_frame.scale_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.toggle_graph_scale,
                text = "lin/log")
        tkinter_frame.legend_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = tkinter_frame.toggle_legend,
                text = "legend")
        tkinter_frame.box_button = ctk.CTkButton(master = tkinter_frame.b1_frame,
                command = lambda: tkinter_frame.button_handler("box_average", [], 0),
                text = "box average")
        tkinter_frame.select_all_button = ctk.CTkCheckBox(master = tkinter_frame.select_all_frame,
                command = tkinter_frame.FM.select_all_graphs,
                variable = tkinter_frame.FM.select_all,
                text = "")
        tkinter_frame.average_button = ctk.CTkButton(master = tkinter_frame.b1_frame,
                command = tkinter_frame.data_analyzer.average,
                text = "average")
        tkinter_frame.square_button = ctk.CTkButton(master = tkinter_frame.b2_frame,
                command = lambda: tkinter_frame.button_handler("power", [2], 0),
                text = u"f\u00B2",
                width=10)
        tkinter_frame.basic_isat_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("ion_saturation_basic", [], 0),
                text = "basic isat")
        tkinter_frame.savgol_button = ctk.CTkButton(master = tkinter_frame.b1_frame,
                command = lambda: tkinter_frame.button_handler("savgol", [53,3], 0),
                text = "S-G Filter")
        tkinter_frame.spline_button = ctk.CTkButton(master = tkinter_frame.b1_frame,
                command = lambda: tkinter_frame.button_handler("spline_extrapolate", [1000], 0),
                text = "spline")
        tkinter_frame.eedf_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("druyvesteyn_eedf", [], 0),
                text = "EEDF")
        tkinter_frame.plasma_potential_button = ctk.CTkButton(master= tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("plasma_potential_derivative_method", [], 3),
                text = "plasma potential")
        tkinter_frame.absolute_button = ctk.CTkButton(master = tkinter_frame.b2_frame,
                command = lambda: tkinter_frame.button_handler("absolute_value", [], 0),
                text = "|f|",
                width=10)
        tkinter_frame.natural_log_button = ctk.CTkButton(master = tkinter_frame.b2_frame,
                command = lambda: tkinter_frame.button_handler("natural_logarithm", [], 0),
                text = "ln f",
                width=10)
        tkinter_frame.oml_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("oml_theory", [], 1),
                text = "oml")
        tkinter_frame.d_temp_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: print("Not implemented yet"),
                text = "Dtemp")
        tkinter_frame.floating_potential_button = ctk.CTkButton(master = tkinter_frame.b3_frame,
                command = lambda: tkinter_frame.button_handler("floating_potential", [], 3),
                text = "Vf")

        #tkinter_frame.potential_bounds_1_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        command = tkinter_frame.save_bounds_1,
        #        text = "Vp bounds 1:")
        #tkinter_frame.potential_bounds_1_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        textvariable= tkinter_frame.bounds1)
        #tkinter_frame.potential_bounds_2_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        command = tkinter_frame.save_bounds_2,
        #        text = "Vp bounds 2:")
        #tkinter_frame.potential_bounds_2_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        textvariable= tkinter_frame.bounds2)
        #tkinter_frame.normal_potential_button = ctk.CTkButton(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        command = tkinter_frame.normal_potential,
        #        text = "NVp:")
        #tkinter_frame.normal_potential_label = ctk.CTkLabel(master = tkinter_frame.normal_plasma_potential_method_frame,
        #        textvariable= tkinter_frame.normal_vp)

        tkinter_frame.fit_counter = ctk.CTkLabel(master = tkinter_frame.cursor_frame, textvariable= tkinter_frame.fit_bound[0])
        tkinter_frame.fit_counter_2 = ctk.CTkLabel(master = tkinter_frame.cursor_frame, textvariable= tkinter_frame.fit_bound[1])
        tkinter_frame.cursor_show_button = ctk.CTkCheckBox(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.hide_cursor(1),
                variable = tkinter_frame.cursor_visibility[0],
                text = "",
                width = 20,
                height = 20)
        tkinter_frame.cursor_show_button_2 = ctk.CTkCheckBox(master = tkinter_frame.cursor_frame,
                command = lambda: tkinter_frame.hide_cursor(2),
                variable = tkinter_frame.cursor_visibility[1],
                text = "",
                width = 20,
                height = 20)

        tkinter_frame.select_all_label = ctk.CTkLabel(master = tkinter_frame.select_all_frame, text = "Select All:")
        tkinter_frame.open_help_and_options_button = ctk.CTkButton(master = tkinter_frame.adding_frame,
                command = lambda: Options.Options(tkinter_frame),
                text = "settings")
        tkinter_frame.hide_button = ctk.CTkButton(master = tkinter_frame.b4_frame,
                command = tkinter_frame.FM.hide_graphs,
                text = "hide")
