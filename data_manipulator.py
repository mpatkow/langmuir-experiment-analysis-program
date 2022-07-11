import numpy as np

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


"""	
dm = data_manipulator()

a = np.array([1,2,3,4,5,6,7,8])
b = np.array([3,3,3,3,3,3,3,3])
c = np.array([1,2,3,4,5,6,7,8])
d = np.array([1,1,1,1,1,1,1,1])

data1 = [a,b]
data2 = [c,d]

print(dm.average([data1, data2]))
"""
