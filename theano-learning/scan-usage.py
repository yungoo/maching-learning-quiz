import theano
import theano.tensor as T
import numpy as np

X = T.matrix('X')
W = T.matrix('W')
b_sym = T.vector('b_sym')

results, updates = theano.scan(lambda v: T.tanh(T.dot(v, W) + b_sym), sequences=X)
compute_elementwise = theano.function(inputs=[X, W, b_sym], outputs=results)

x = np.eye(2, dtype=theano.config.floatX)
print('x:\n', x)
w = np.ones((2,2), dtype=theano.config.floatX)
print('w:\n', w)
b = np.ones((2), dtype=theano.config.floatX)
b[1] = 2
print('b:\n', b)

print('results:\n', compute_elementwise(x, w, b))

print('equals:\n', np.tanh(x.dot(w) + b))