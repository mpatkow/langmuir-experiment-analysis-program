"""File manipulations for LEAP"""
import math
import warnings
import numpy as np
from scipy.signal import savgol_filter
from scipy import interpolate as itp

class data_manipulator:
    """File manipulations for LEAP"""
    def __init__(self, tkinter_frame):
        self.tkinter_frame = tkinter_frame
        self.ELEM_CHARGE = 1.60217663 * 10 ** (-19)
        warnings.simplefilter(action='ignore', category=RuntimeWarning)

    def derivative(self, graph, options):
        """Takes the derivative of the data with the specified order"""
        order = options[0]
        derivatives = [graph.data[1]]
        dx = np.gradient(graph.data[0])
        for _ in range(order):
            dy = np.gradient(derivatives[-1])
            derivatives.append(dy/dx)
        return [[graph.data[0],derivatives[-1]]]

    # TODO Right now only works on data sets of identical dimensions.
    def average(self):
        """
        takes the average of the given data files
        data is a list of data files. Each of these data files
        is stored as a list [x,y], where x and y are numpy arrays.
        """
        data = []
        for graph in self.tkinter_frame.FM.currently_displayed:
            data.append(graph.data)

        new_x = data[0][0]
        new_y = data[0][1]
        new_y = new_y.astype('float64')
        for dataset in data[1:]:
            new_y += dataset[1]
        new_y /= float(len(data))
        self.tkinter_frame.FM.add_file(self.tkinter_frame.get_next_name("average.data"), [new_x, new_y])

    def savgol(self, graph, options):
        """Takes the savgol filter of the given graph"""
        o1 = options[0]
        o2 = options[1]
        if o1 % 2 == 0:
            o1 += 1

        return [[graph.data[0],savgol_filter(graph.data[1],o1,o2)]]

    def box_average(self, graph, options):
        """Box average; takes the average of the datapoint itself and its neighbors"""
        data = graph.data
        new_y = []
        for i in range(1, len(data[1])-1):
            new_y.append((data[1][i-1] + data[1][i] + data[1][i+1])/3)
        new_y = np.array(new_y)
        new_y = np.insert(new_y, 0, data[1][0], axis=0)
        new_y = np.append(new_y, data[1][-1])
        return [[data[0], new_y]]

    def floating_potential(self, graph, options):
        """
        Finds the floating potential by finding the largest negative value
        and smallest positive value and doing a linear fit between them to get
        the x-intercept.
        """
        a = graph.data[1]
        aa = np.absolute(a)

        i = np.where(aa == np.amin(aa))[0]

        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0

        if a[i] < 0:
            x1 = graph.data[0][i]
            y1 = a[i]
            x2 = graph.data[0][i+1]
            y2 = a[i+1]
        else:
            x1 = graph.data[0][i-1]
            y1 = a[i-1]
            x2 = graph.data[0][i]
            y2 = a[i]

        v_float = x1 - y1 * (x2-x1)/(y2-y1)
        return v_float

    def natural_logarithm(self, graph, options):
        """Takes the natural logarithm of the y values"""
        return [[graph.data[0], np.log(graph.data[1])]]

    def ion_saturation_basic(self, graph, options):
        """
        Linear fit between the cursors.
        Subtracts this fitted isat current from I-V sweep.
        """
        [lower_abs, upper_abs] = self.tkinter_frame.get_cursor_values(graph)
        m,b = np.polyfit(graph.data[0][lower_abs:upper_abs],
                         graph.data[1][lower_abs:upper_abs],
                         1)
        to_return = [[graph.data[0], graph.data[1] - m*graph.data[0] - b]]
        if self.tkinter_frame.ecurr_view:
            to_return.append([graph.data[0], m*graph.data[0] + b])
        return to_return

    # TODO not working
    def druyvesteyn_eedf(self):
        """
        Returns the EEDF as found by the druyesteyn method
        """
        max_index = np.argmin(np.abs(data[0]-vp))
        trimmed_probe_biases = data[0][0:max_index]
        new_current_data = np.flip(data[1][0:max_index])
        electron_energy = np.flip(vp - trimmed_probe_biases)
        first_der = self.derivative([trimmed_probe_biases, new_current_data],1)
        first_der_smoothed = self.savgol_smoothing(first_der,51,3)
        second_der = self.derivative([trimmed_probe_biases, first_der_smoothed],1)
        return electron_energy, np.multiply(second_der[1], np.sqrt(electron_energy)) * (9.1093837 * 10**(-31)) ** (0.5) * 2 * math.sqrt(2) / ((1.60217663 * 10**(-19)) **2 * probe_area)

    # TODO not working
    def druyvesteyn_temperature(self, data, lower_bound, upper_bound):
        total_area = 0
        numerator_integral = 0
        for i in range(lower_bound, upper_bound):
            dx = data[0][i+1]-data[0][i]
            f = data[1][i]
            total_area += dx * f
            numerator_integral += data[0][i] * dx * f

        return (2.0/3.0) * 1/total_area * numerator_integral

    def plasma_potential_derivative_method(self, graph, options):
        """
        Returns the plasma potential as found by the maximum of dV
        """
        data_der = self.derivative(graph, [1])
        i = np.argmax(data_der[0][1])
        return graph.data[0][i]

    # TODO not fixed yet
    def oml_theory(self, fname, options_list):
        data = self.tkinter_frame.currently_displayed[fname]
        [lower_abs, upper_abs] = self.tkinter_frame.get_cursor_values(fname, self.tkinter_frame.currently_displayed)

        probe_area_m2 = 0.0001 * self.tkinter_frame.probe_area
        m,b = np.polyfit(data[0][lower_abs:upper_abs], data[1][lower_abs:upper_abs], 1)
        vs1 = -b/m
        Vp = data[0][lower_abs]
        Ii = data[1][lower_abs] ** 0.5
        ion_mass = 6.62*10**(-26)
        density = np.pi / (2**0.5) * Ii / (probe_area_m2 * 1.60217663 * 10**(-19)) * (ion_mass) ** 0.5 / (1.60217663 * 10**(-19)*(vs1-Vp))**0.5
        density = density/(10**6)
    
        #density = self.data_analyzer.oml_theory(data_t,np.where(lower_abs == np.min(lower_abs))[0][0],np.where(upper_abs == np.min(upper_abs))[0][0],self.probe_area_input.get(),self.ion_mass_input.get())

        self.tkinter_frame.density.set(density)
        print(density)

    def power(self, graph, options_list):
        """
        Raises the y-values of the data stored in fname to the given power, options_list[0]
        """
        return [[graph.data[0], graph.data[1] ** options_list[0]]]

    def absolute_value(self, graph, options_list):
        """
        Takes the absolute value of the y-values of the data
        """
        return [[graph.data[0], np.absolute(graph.data[1])]]

    def trim(self, graph, options_list):
        """
        Returns the data, trimmed between the cursors
        """
        [xmin, xmax] = self.tkinter_frame.get_cursor_values(graph)
        return [[graph.data[0][xmin:xmax], graph.data[1][xmin:xmax]]]

    def basic_density(self, graph, options_list):
        """
        Calculates the electron density based on the following formula:

        n_e = (isat_value)/(elementary_charge * probe_area * exp(-1/2)) * sqrt(M/(elementary_charge * temperature (in ev)))
        
        
        old formula was implemented as, incorrectly:
        ne = isat_value/(self.elementary_charge * self.probe_area * 10**(-3)) * (self.gas_type * 2 * math.pi / (float(input("Temperature: ")) * self.elementary_charge) ) ** 0.5

        M is the ion mass, in kg
        isat_value is the tenth current value in the data

        based on https://davidpace.com/example-of-langmuir-probe-analysis/
        """
        isat_value = abs(graph.data[1][10])

        electron_density = isat_value/(self.ELEM_CHARGE * self.tkinter_frame.probe_area * 0.60653066) * math.sqrt(self.tkinter_frame.gas_type / (float(input("Temperature: ")) * self.ELEM_CHARGE))
        return electron_density

    def spline_extrapolate(self, graph, options):
        """
        Petforms a spline filter on the given graph
        options[0] specifie the number of points in the spline
        """
        points = options[0]
        mytck, myu = itp.splprep(graph.data, k=5, s=0)
        xnew, ynew = itp.splev(np.linspace(0,1,points), mytck)
        return [[xnew,ynew]]

    def temperature_fit(self, graph, options):
        """Calculates the temperature as given by the slope between the cursors"""
        [temp_fit_lower, temp_fit_upper] = self.tkinter_frame.get_cursor_values(graph)
        temps = []
        for upper_bound in range(temp_fit_lower, temp_fit_upper+1):
            for lower_bound in range(temp_fit_lower, upper_bound):
                if abs(lower_bound-upper_bound) == 1:
                    pass
                else:
                    if (temp_fit_lower - temp_fit_upper) > 10:
                        if upper_bound % 5 == 0 and lower_bound % 5 == 0:
                            m, b = np.polyfit(graph.data[0][lower_bound:upper_bound],
                                              graph.data[1][lower_bound:upper_bound],
                                              1)
                            temps.append(1/m)
                    else:
                        m, b = np.polyfit(graph.data[0][lower_bound:upper_bound],
                                          graph.data[1][lower_bound:upper_bound],
                                          1)
                        temps.append(1/m)

        temps = np.array(temps)
        av = np.average(temps)
        std = np.std(temps)

        final_temp_statement = f"Temperature: {av} \u00b1 {std} eV"

        self.tkinter_frame.open_popup(final_temp_statement, "", "RESULT")

        return [av, std]