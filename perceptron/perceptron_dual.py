import numpy as np
import matplotlib.pyplot as plt 
import time

class PerceptronDual(object):
	"""docstring for PerceptronDual"""
	def __init__(self, samples):
		super(PerceptronDual, self).__init__()
		self.samples = samples
		self.gram = PerceptronDual.calc_gram(samples)
		self.a = np.array([0] * len(samples))
		self.b = 0
		self.times = 0
		self.stop = False

	@classmethod
	def calc_gram(cls, samples):
		n = len(samples)
		gram = np.arange(n*n).reshape((n, n))
		for i in range(n):
			for j in range(n):
				gram[i][j] = np.dot(samples[i][0], samples[j][0])
		return gram

	def run(self):
		fp = True

		start = time.clock()
		while fp and time.clock() - start < 10 and not self.stop:
			fp = self.check()
		
		if not fp:
			x = []
			y = []
			for i, t in enumerate(self.samples):
				x.append(t[0])
				y.append(t[1])
			x = np.array(x)
			y = np.array(y)
			t = self.a * y
			w = np.dot(t, x)
			print(w, self.b)
			return (w, self.b)

		raise Exception('timeout')

	def check(self):
		flag = False
		for i, t in enumerate(self.samples):
			d = self.distance(i)
			if d <= 0:
				self.a[i] = self.a[i] + 1
				self.b = self.b + t[1]

				flag = True
				self.times = self.times + 1

				print(self.times, self.a, self.b)
		return flag

	def distance(self, i):
		d = 0
		sample = self.samples[i]
		for j, t in enumerate(self.samples):
			d = d + self.a[j] * t[1] * self.gram[j][i]
		d = d + self.b
		d = d * sample[1]
		return d


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
	app = PerceptronDual(samples)
	try:
		w, b = app.run()
		draw(samples, w, b)
	except:
		app.stop()

