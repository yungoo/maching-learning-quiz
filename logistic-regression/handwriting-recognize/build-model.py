import pickle as cPickle
import gzip

import numpy
from PIL import Image

import theano.tensor as T

with gzip.open('mnist.pkl.gz', 'rb') as f:
	train_set, valid_set, test_set = cPickle.load(f, encoding='iso-8859-1')

# print('The 0\'th label:', train_set[1][0])
# lst = numpy.asarray(train_set[0][0], dtype=numpy.float32)
# img = Image.frombytes(mode='F', size=(28,28), data=lst*255)
# img.show()

index = T.lscalar()
x = T.matrix('x')
y = T.ivector('y')

