import numpy as np
import math
from scipy.signal import savgol_filter

class data_manipulator:
    def __init__(self, tkinter_frame):
        self.tkinter_frame = tkinter_frame

    def derivative(self, data, order):
        derivatives = [data[1]]
        dx = np.gradient(data[0])
        for i in range(order):
            dy = np.gradient(derivatives[-1])
            derivatives.append(dy/dx)
        return [data[0],derivatives[-1]]

    # Right now only works on data sets of identical dimensions.
    def average(self, data):
        # data is a list of data files. Each of these data files is stored as a list [x,y], where x and y are numpy arrays.
        new_x = data[0][0]
        new_y = data[0][1]
        new_y = new_y.astype('float64')
        for dataset in data[1:]:
            new_y += dataset[1]
        new_y /= float(len(data))
        return [new_x, new_y]

    # Takes the average of the data point itself and its neighbors
    def box_average(self, data):
        new_y = []
        for i in range(1, len(data[1])-1):
            new_y.append((data[1][i-1] + data[1][i] + data[1][i+1])/3)
        new_y = np.array(new_y)
        new_y = np.insert(new_y, 0, data[1][0], axis=0)
        new_y = np.append(new_y, data[1][-1])
        return [data[0], new_y]

    # Finds the floating potential by finding the largest negative value and smallest positive value and doing a linear fit between them to get the x-intercept.
    def floating_potential(self, data):
        a = data[1]
        aa = np.absolute(a)

        i = np.where(aa == np.amin(aa))[0]

        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0

        if a[i] < 0:
            x1 = data[0][i]
            y1 = a[i]
            x2 = data[0][i+1]
            y2 = a[i+1]
        else:
            x1 = data[0][i-1]
            y1 = a[i-1]
            x2 = data[0][i]
            y2 = a[i]

        v_float = x1 - y1 * (x2-x1)/(y2-y1)
        return v_float

    def ion_saturation_primitive(self, data):
        return data[1][0]

    def ion_saturation_basic(self, fname, options_list):
        [lower_abs, upper_abs] = self.tkinter_frame.get_cursor_values(fname, self.tkinter_frame.currently_displayed)
        data = self.tkinter_frame.currently_displayed[fname]
        m,b = np.polyfit(data[0][lower_abs:upper_abs] , data[1][lower_abs:upper_abs], 1)
        xvalues = self.tkinter_frame.currently_displayed[fname][0]
        to_return = [[xvalues, data[1] - m*data[0] - b]]
        if self.tkinter_frame.ecurr_view:
            to_return.append([xvalues, m*data[0] + b])
        return to_return

    def savgol_smoothing(self, data, o1, o2):
        return savgol_filter(data[1],o1,o2)

    def druyvesteyn(self, data, vp, probe_area):
        # returns eedf
        max_index = np.argmin(np.abs(data[0]-vp))
        trimmed_probe_biases = data[0][0:max_index]
        new_current_data = np.flip(data[1][0:max_index])
        electron_energy = np.flip(vp - trimmed_probe_biases)
        first_der = self.derivative([trimmed_probe_biases, new_current_data],1)
        first_der_smoothed = self.savgol_smoothing(first_der,51,3)
        second_der = self.derivative([trimmed_probe_biases, first_der_smoothed],1)
        return electron_energy, np.multiply(second_der[1], np.sqrt(electron_energy)) * (9.1093837 * 10**(-31)) ** (0.5) * 2 * math.sqrt(2) / ((1.60217663 * 10**(-19)) **2 * probe_area)

    def druyvesteyn_temperature(self, data, lower_bound, upper_bound):
        total_area = 0
        numerator_integral = 0
        for i in range(lower_bound, upper_bound):
            dx = data[0][i+1]-data[0][i]
            f = data[1][i]
            total_area += dx * f
            numerator_integral += data[0][i] * dx * f

        return (2.0/3.0) * 1/total_area * numerator_integral

    def plasma_potential(self, data):
        data_der = self.derivative(data, 1)
        i = np.argmax(data_der[1])
        return data[0][i]


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

    def power(self, fname, options_list):
        """
        Raises the y-values of the data stored in fname to the given power, options_list[0]
        """
        data = self.tkinter_frame.currently_displayed[fname]
        return [[data[0], data[1] ** options_list[0]]]

    def absolute_value(self, fname, options_list):
        """
        Takes the absolute value of the y-values of the data
        """
        data = self.tkinter_frame.currently_displayed[fname]
        return [[data[0], np.absolute(data[1])]]
    
    #FIXME incorrect formula
    def debye_length(self, fname, options_list):
        """
        Calculates the debye length of the plasma
        """
        