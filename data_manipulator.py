import numpy as np
from scipy.signal import savgol_filter

class data_manipulator:
	def __init__(self):
		pass

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
		return [data[0][1:-1], new_y]
	
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
	
	def ion_saturation_basic(self, data, isat_guess):
		m,b = np.polyfit(data[0][:isat_guess], data[1][:isat_guess], 1)
		return m*data[0] + b, data[1] - m*data[0] -b
	
	def savgol_smoothing(self, data):
		return savgol_filter(data[1],51,3)
	
	def druyvesteyn(self, data, vp):
		d = self.derivative(data, 2)[1]
		return d * (vp-data[0])**0.5

	def plasma_potential(self, data):
		data_der = self.derivative(data, 1)
		i = np.argmax(data_der[1])
		return data[0][i]
	
	def absolute_val(self, data):
		return [data[0], np.absolute(data[1])]
