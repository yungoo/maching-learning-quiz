from numpy import *
from LogisticRegression import LogisticRegression as LR

def load_train_data():
	x = []
	y = []
	with open('./data.csv') as f:
		for line in f.readlines():
			fields = line.strip().split(',')
			x.append([1.0, float(fields[0]), float(fields[1])])
			y.append(float(fields[2]))
	return mat(x), mat(y).transpose()


if __name__ == '__main__':
	x, y = load_train_data()
	tx, ty = x, y

	lr = LR()
	lr.train(x, y, {'alpha': 1, 'max_iteration': 25, 'optimize_type': 'smooth_stock_grad_descent'})
	accuracy = lr.test(tx, ty)
	print('accuracy is ', accuracy)

	lr.inspect()
