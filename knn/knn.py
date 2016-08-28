#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import math
import copy
from queue import PriorityQueue
from util import log, bCircleIntersectRectangle

class Node(object):
	"""docstring for Node"""
	def __init__(self, axis, data, left, right, bounds):
		super(Node, self).__init__()

		self.axis = axis
		self.data = data
		self.left = left
		self.right = right
		self.bounds = bounds

	def is_leaf(self):
		return self.left == None and self.right == None

class kNNResultCollection(object):
	"""docstring for kNNResultCollection"""

	class kNNResult(object):
		"""docstring for kNNResult"""
		def __init__(self, node, distance):
			super(kNNResultCollection.kNNResult, self).__init__()
			self.node = node
			self.distance = distance
		def __cmp__(self, t):
			return cmp(s.distance, t.distance)
		def __lt__(self, t):
			return self.distance > t.distance

	def __init__(self, K):
		super(kNNResultCollection, self).__init__()
		self.K = K
		self.queue = PriorityQueue(K + 1)
		self.distance = float('inf')
		self.last_node = None

	def put(self, node, distance):
		if distance >= self.distance:
			return False

		succ = True
		self.queue.put_nowait(kNNResultCollection.kNNResult(node, distance))
		if self.queue.qsize() > self.K:
			t = self.queue.get_nowait()
			log('discard nn', t.node.data, 'with distance', t.distance)
			succ = t.node != node

		if succ:
			self.last_node = node

		return succ

	def last(self):
		return self.last_node if self.last_node != None else None

	def touch(self):
		ret = []
		while not self.queue.empty():
			ret.append(self.queue.get().node)
		return ret
			
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
		root = cls._build(samples, -1, dim)
		return KDTree(root, dim, observer)

	@classmethod
	def _build(cls, samples, index, dim, bounds = None):
		"""递归构造kd-tree"""
		index = (index + 1) % dim
		sorted_samples = sorted(samples, key = lambda s: s[index])
		axis_point = len(sorted_samples) >> 1
		selected = sorted_samples[axis_point]

		if bounds == None:
			bounds = cls._bounds(samples)

		left_samples = sorted_samples[:axis_point]
		right_samples = sorted_samples[axis_point + 1:]

		left = right = None
		lbounds, rbounds = cls._split_bounds(bounds, index, selected[index])

		if len(left_samples) > 0:
			left = cls._build(left_samples, index, dim, lbounds)

		if len(right_samples) > 0:
			right = cls._build(right_samples, index, dim, rbounds)

		return Node(index, selected, left, right, bounds)

	def find_nearest_neighbor(self, target, k=1):
		"""
		查找最近邻
		"""
		nnc = kNNResultCollection(k)
		search_path = []

		tn = KDTree.find(self.root, target, search_path)
		d = self.distance(target, tn.data)
		if nnc.put(tn, d):
			self.notify_nn_found(target, d)
			log((tn.data if tn != None else None), 'select as nn', 'with radius', d, 'search path', [t.data for t in search_path])

		cur_node = tn
		while len(search_path) > 0:
			parent = search_path.pop()
			
			d = self.distance(target, parent.data)
			if nnc.put(parent, d):
				log(parent.data, 'is near then nn', (tn.data if tn != None else None), 'with radius', d, 'search path', [t.data for t in search_path])
				self.notify_nn_found(target, d)

			if parent.is_leaf():
				continue

			if parent.left == cur_node:
				next_node = parent.right
			else:
				next_node = parent.left

			if next_node != None:
				log('searching in otherside', next_node.data, 'with parent', parent.data, 'current is', cur_node.data)

				self._search_nearest_neighbor(next_node, target, nnc)

			else:
				log('NO need to searching otherside', 'with parent', parent.data, 'current is', cur_node.data)

			cur_node = parent

		return nnc

	def _search_nearest_neighbor(self, parent, target, nnc):
		"""
		在某子树下搜索最近邻
		"""
		d = self.distance(target, parent.data)
		if nnc.put(parent, d):
			log(parent.data, 'is near then nn', nnc.last().data if nnc.last() != None else None, 'with radius', d)
			self.notify_nn_found(target, d)

		if self.intersect_with((target, d), parent):
			if parent.left != None:
				self._search_nearest_neighbor(parent.left, target, nnc)

			if parent.right != None:
				self._search_nearest_neighbor(parent.right, target, nnc)
		else:
			log('test intersection with', parent.data, 'is no intersection')

	def notify_nn_found(self, target, radius):
		if self._observer:
			self._observer.did_nn_found(target, radius)

	@classmethod
	def find(cls, node, target, search_path):
		"""叶子查找"""
		if target[node.axis] < node.data[node.axis] and node.left != None:
			search_path.append(node)
			return cls.find(node.left, target, search_path)
		elif target[node.axis] > node.data[node.axis] and node.right != None:
			search_path.append(node)
			return cls.find(node.right, target, search_path)
		return node

	@classmethod
	def _bounds(cls, samples):
		"""
		获取实例的边界
		"""
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
	def _split_bounds(cls, in_bounds, axis, value):
		"""将超矩形划分为两个子区域"""
		l = copy.deepcopy(in_bounds)
		r = copy.deepcopy(in_bounds)

		l[axis][1] = value
		r[axis][0] = value

		return (l, r)

	@classmethod
	def distance(cls, source, target):
		"""计算欧氏距离"""
		d = 0.0
		for i in range(len(source)):
			d = d + (source[i] - target[i]) * (source[i] - target[i])

		return math.sqrt(d)

	@classmethod
	def intersect_with(clz, hypercicle, node):
		"""判断圆和矩形相交"""
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

def draw_2d_tree(tree, target_level = None):
	plt.axis([tree.root.bounds[0][0], tree.root.bounds[0][1], tree.root.bounds[1][0], tree.root.bounds[1][1]])

	def draw_tree_node(node, level):
		if len(node.data) == 2:
			if not node.is_leaf():
				if node.axis == 0:
					x = [node.data[node.axis], node.data[node.axis]]
					y = node.bounds[1]
				else:
					x = node.bounds[0]
					y = [node.data[node.axis], node.data[node.axis]]
				plt.plot(x, y, 'b-')

			plt.plot(node.data[0], node.data[1], 'bo')

			if target_level != None and level >= target_level:
				return

			if node.left != None:
				draw_tree_node(node.left, level+1)
			if node.right != None:
				draw_tree_node(node.right, level+1)

	draw_tree_node(tree.root, 1)

def make_samples():
	return [(2,3),(5,4),(8.5,5),(4,7),(8,1),(7,2)]
	# return [(6.5,3.6),(5,4),(8.5,5),(4,7),(8,1),(7,2)]
	# return [(3,1.5),(2,4),(9.5,7),(3.9,8),(9,1),(4,0.1)]

if __name__ == '__main__':
	samples = make_samples()
	target = (3, 4.5)
	tree = KDTree.build(samples, SearchObserver())
	ret = tree.find_nearest_neighbor(target, k=1)

	plt.title('k-NN demo')
	plt.plot(target[0], target[1], 'rx')
	draw_2d_tree(tree)

	for nb in ret.touch():
		plt.plot(nb.data[0], nb.data[1], 'ro')
	plt.show()