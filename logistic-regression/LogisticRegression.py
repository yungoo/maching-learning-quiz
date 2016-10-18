from numpy import *
import matplotlib.pyplot as plt

def sigmoid(x):
	return 1.0 / (1 + exp(-x))

class LogisticRegression(object):
	"""docstring for LogisticRegression"""
	def __init__(self):
		super(LogisticRegression, self).__init__()
		
	def train(self, x, y, opts):
		'''
		@see: http://blog.csdn.net/zouxy09/article/details/20319673
		'''
		num_samples, num_features = shape(x)
		alpha = opts['alpha']
		max_iteration = opts['max_iteration']
		optimize_type = opts['optimize_type']
		weights = ones([num_features, 1])
		
		for k in range(max_iteration):
			if optimize_type == 'grad_descent':
				output = sigmoid(x * weights)
				error = y - output
				weights = weights + alpha * x.transpose() * error
			elif optimize_type == 'stoc_grad_descent':
				for i in range(num_samples):
					output = sigmoid(x[i, :] * weights)
					error = y[i, 0] - output
					weights = weights + alpha * x[i, :].transpose() * error
			elif optimize_type == 'smooth_stock_grad_descent':
				data_index = list(range(num_samples))
				for i in range(num_samples):
					alpha = 4.0 / (1.0 + k + i) + 0.01
					rand_index = int(random.uniform(0, len(data_index)))
					output = sigmoid(x[rand_index, :] * weights)
					error = y[rand_index, :] - output
					weights = weights + alpha * x[rand_index, :].transpose() * error
					del data_index[rand_index]
			else:
				raise NameError('Not support optimize_type');

		self.weights = weights
		self.x = x
		self.y = y

		return self

	def test(self, x, y):
		num_samples, num_features = shape(x)
		match_count = 0
		for i in range(num_samples):
			predict = sigmoid(x[i, :] * self.weights)[0, 0] > 0.5
			if predict == bool(y[i, 0]):
				match_count += 1
		accuracy = float(match_count) / num_samples
		return accuracy

	def inspect(self):
		x, y = self.x, self.y
		num_samples, num_features = shape(x)
		if num_features != 3:
			print("Sorry! I can not draw because the dimension of your data is not 2!")
			return 1

		for i in range(num_samples):
			if int(y[i, 0]) == 0:
				plt.plot(x[i, 1], x[i, 2], 'or')
			elif int(y[i, 0] == 1):
				plt.plot(x[i, 1], x[i, 2], 'ob')

		min_x = min(x[:, 1])[0, 0]
		max_x = max(x[:, 1])[0, 0]
		weights = self.weights.getA()
		y_min_x = float(-weights[0] - weights[1] * min_x) / weights[2]
		y_max_x = float(-weights[0] - weights[1] * max_x) / weights[2]
		plt.plot([min_x, max_x], [y_min_x, y_max_x], '-g')
		plt.xlabel('X1')
		plt.ylabel('X2')
		plt.show()
