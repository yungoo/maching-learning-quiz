# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt 
import time

class PerceptronPrimal(object):
	"""docstring for PerceptronPrimal"""
	def __init__(self, samples):
		super(PerceptronPrimal, self).__init__()
		self.samples = samples
		self.w = np.array([0, 0])
		self.b = 0
		self.times = 0
		self.stop = False

	def run(self):
		fp = True

		start = time.clock()
		while fp and time.clock() - start < 10 and not self.stop:
			fp = self.check()
		
		return (self.w, self.b)

	def check(self):
		flag = False
		for i, t in enumerate(self.samples):
			# tp = t[1] * (w * t[0] + b)
			tp = np.multiply(t[1], np.add(np.dot(self.w, t[0]), self.b))
			if tp <= 0:
				# w = w + t[1] * t[0]
				self.w = np.add(self.w, np.multiply(t[1], t[0]))
				# b = b + t[1]
				self.b = self.b + t[1]
				
				flag = True
				self.times = self.times + 1

				print(self.times, i + 1, self.w, self.b)
		return flag

	def stop(self):
		self.stop = True
		pass

def make_samples():
	return np.array([
		[(3, 3), 1], 
		[(4, 3), 1],
		[(1, 1), -1]])
		
def draw(samples, w, b):
	fp_x = []
	fp_y = []
	tp_x = []
	tp_y = []
	for i, t in enumerate(samples):
		if t[1] < 0:
			fp_x.append(t[0][0])
			fp_y.append(t[0][1])
		else:
			tp_x.append(t[0][0])
			tp_y.append(t[0][1])

	plt.axis([0, max(max(fp_x), max(tp_x)) + 1, 0, max(max(fp_y), max(tp_y)) + 1])
	plt.plot(fp_x, fp_y, 'rx')
	plt.plot(tp_x, tp_y, 'ro')
	plt.plot([0, -b/w[0]], [-b / w[1], 0], 'b-')
	plt.show()

if __name__ == '__main__':
	samples = make_samples()
	app = PerceptronPrimal(samples)
	try:
		w, b = app.run()
		draw(samples, w, b)
	except:
		app.stop()

