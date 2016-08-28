#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import math
from util import log, bCircleIntersectRectangle

class Node(object):
	"""docstring for Node"""
	def __init__(self, split, value, left, right, bounds):
		super(Node, self).__init__()

		self.split = split
		self.value = value
		self.left = left
		self.right = right
		self.bounds = bounds

	def is_leaf(self):
		return self.left == None and self.right == None

class KDTree(object):
	"""docstring for KDTree"""
	def __init__(self, root, K, observer):
		super(KDTree, self).__init__()
		self.root = root
		self.K = K
		self._observer = observer

	@classmethod
	def build(cls, samples, observer = None):
		"""build kd-tree"""
		if samples == Node or len(samples) == 0:
			return None

		dim = len(samples[0])

		kd_tree = cls._build(samples, -1, dim)

		return KDTree(kd_tree, dim, observer)

	@classmethod
	def _build(cls, samples, index, dim, bounds = None):
		index = (index + 1) % dim

		sorted_samples = sorted(samples, key = lambda s: s[index])
		split_point = len(sorted_samples) >> 1
		selected = sorted_samples[split_point]

		if bounds == None:
			bounds = cls._bounds(samples)

		left_samples = sorted_samples[:split_point]
		right_samples = sorted_samples[split_point + 1:]

		left = right = None
		lbounds, rbounds = cls._split_bounds(bounds, index, selected[index])

		if len(left_samples) > 0:
			left = cls._build(left_samples, index, dim, lbounds)

		if len(right_samples) > 0:
			right = cls._build(right_samples, index, dim, rbounds)

		return Node(index, selected, left, right, bounds)

	def find_nearest_neighbor(self, target):
		"""
		查找最近邻
		"""
		search_path = []
		nn = KDTree.find(self.root, target, search_path)
		d = self.distance(target, nn.value)
		self.notify_nn_found(target, d)

		log((nn.value if nn != None else None), 'select as nn', 'with radius', d, 'search path', [t.value for t in search_path])

		cur_node = nn
		while len(search_path) > 0:
			parent = search_path.pop()
			
			td = self.distance(target, parent.value)
			if td < d:
				log(parent.value, 'is near then nn', (nn.value if nn != None else None), 'with radius', td, 'search path', [t.value for t in search_path])
				d = td
				nn = parent
				self.notify_nn_found(target, d)

			if parent.is_leaf():
				continue

			if parent.left == cur_node:
				next_node = parent.right
			else:
				next_node = parent.left

			if next_node != None:
				log('searching in otherside', next_node.value, 'with parent', parent.value, 'current is', cur_node.value)

				tn, td = self._search_nearest_neighbor(next_node, target, d, nn)
				if tn != None:
					nn = tn
					d = td
			else:
				log('NO need to searching otherside', 'with parent', parent.value, 'current is', cur_node.value)

			cur_node = parent

		return nn

	def _search_nearest_neighbor(self, parent, target, d, nn):
		result = None
		td = self.distance(target, parent.value)
		if td < d:
			log(parent.value, 'is near then nn', (nn.value if nn != None else None), 'with radius', td)
			d = td
			nn = result = parent
			self.notify_nn_found(target, d)

		if self.intersect_with((target, d), parent):
			if parent.left != None:
				tn,td = self._search_nearest_neighbor(parent.left, target, d, nn)
				if tn != None:
					nn = result = tn
					d = td
			
			if parent.right != None:
				tn,td = self._search_nearest_neighbor(parent.right, target, d, nn)
				if tn != None:
					nn = result = tn
					d = td
		else:
			log('test intersection with', parent.value, 'is no intersection')

		return (result, d) if result != None else (None, None)


	def notify_nn_found(self, target, radius):
		if self._observer:
			self._observer.did_nn_found(target, radius)

	@classmethod
	def find(cls, node, target, search_path):
		if target[node.split] < node.value[node.split] and node.left != None:
			search_path.append(node)
			return cls.find(node.left, target, search_path)
		elif target[node.split] > node.value[node.split] and node.right != None:
			search_path.append(node)
			return cls.find(node.right, target, search_path)

		return node

	@classmethod
	def _bounds(cls, samples):
		bounds = []
		for i in range(len(samples[0])):
			bounds.append([float('inf'), float('-inf')])

		for sample in samples:
			for i, t in enumerate(sample):
				if t < bounds[i][0]:
					bounds[i][0] = float(t)
				if t > bounds[i][1]:
					bounds[i][1] = float(t)

		for b in bounds:
			b[0] = min(0, b[0])
			b[1] = b[1] + 1

		return bounds

	@classmethod
	def _split_bounds(cls, in_bounds, split, value):
		if split == 0:
			return ([[in_bounds[0][0], value], in_bounds[1]], 
					[[value, in_bounds[0][1]], in_bounds[1]])
		else:
			return ([in_bounds[0], [in_bounds[1][0], value]], 
					[in_bounds[0], [value, in_bounds[1][1]]])

	@classmethod
	def distance(cls, source, target):
		d = 0.0
		for i in range(len(source)):
			d = d + (source[i] - target[i]) * (source[i] - target[i])

		return math.sqrt(d)

	@classmethod
	def intersect_with(clz, hypercicle, node):
		return bCircleIntersectRectangle(node.bounds[0][0], node.bounds[1][1],
			node.bounds[0][1], node.bounds[1][0], hypercicle[0][0], hypercicle[0][1], hypercicle[1])

class SearchObserver(object):
	"""docstring for SearchObserver"""
	def __init__(self):
		super(SearchObserver, self).__init__()

	def did_nn_found(self, target, radius):
		ax = plt.gca()
		cir1 = Circle(xy = target, radius=radius, alpha=0.4)
		ax.add_patch(cir1)

def draw_tree(tree, target_level = None):
	plt.axis([tree.root.bounds[0][0], tree.root.bounds[0][1], tree.root.bounds[1][0], tree.root.bounds[1][1]])

	def draw_tree_node(node, level):
		if len(node.value) == 2:
			if not node.is_leaf():
				if node.split == 0:
					x = [node.value[node.split], node.value[node.split]]
					y = node.bounds[1]
				else:
					x = node.bounds[0]
					y = [node.value[node.split], node.value[node.split]]
				plt.plot(x, y, 'b-')

			plt.plot(node.value[0], node.value[1], 'bo')

			if target_level != None and level >= target_level:
				return

			if node.left != None:
				draw_tree_node(node.left, level+1)
			if node.right != None:
				draw_tree_node(node.right, level+1)

	draw_tree_node(tree.root, 1)

def make_samples():
	return [(2,3),(5,4),(8.5,5),(4,7),(8,1),(7,2)]

if __name__ == '__main__':
	samples = make_samples()
	target = (3, 4.5)
	plt.title('1－NN算法演示')
	plt.plot(target[0], target[1], 'rx')

	tree = KDTree.build(samples, SearchObserver())
	draw_tree(tree)

	nb = tree.find_nearest_neighbor(target)
	plt.plot(nb.value[0], nb.value[1], 'ro')
	plt.show()
		