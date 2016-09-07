

class NaiveBayesian(object):
	"""docstring for NaiveBayesian"""
	def __init__(self, smooth = True):
		super(NaiveBayesian, self).__init__()
		if smooth:
			self.p_functor = lambda nt, nv, n: (nv + 1) / (n + nt)
		else:
			self.p_functor = lambda nt, nv, n: nv / n

	def train(self, samples):
		"""
		计算得到特征概率矩阵
		   n values
		c0
		c1
		"""
		N = len(samples)
		type_props = {}
		condition_props = {}

		types = NaiveBayesian.value_counts(samples, -1)
		N_Types = len(types)
		for type in types:
			type_props[type] = self.p_functor(N_Types, types[type], N)
			type_col_props = {}
			for col in range(len(samples[0]) - 1):
				col_values = NaiveBayesian.value_counts(samples, col, lambda row: row[-1] == type)
				col_values_props = {}
				NV = 0
				N_col_values = len(col_values)
				for v in col_values:
					NV += col_values[v]
				for v in col_values:
					col_values_props[v] = self.p_functor(N_col_values, col_values[v], NV)
				type_col_props[col] = col_values_props
			condition_props[type] = type_col_props

		self.type_props = type_props
		self.condition_props = condition_props

	def classify(self, instance):
		cp = 0
		result_type = None
		for type in self.type_props:
			p = self.type_props[type]
			for col in range(len(instance)):
				v = instance[col]
				if v in self.condition_props[type][col]:
					p *= self.condition_props[type][col][instance[col]]
				else:
					p = 0
			if p > cp:
				cp = p
				result_type = type
		return (result_type, cp)

	def value_counts(rows, cols, filter = None):
	    '''
	    对y的各种可能的取值出现的个数进行计数.。其他函数利用该函数来计算数据集和的混杂程度
	    '''
	    results = {}
	    for row in rows:
	        if filter == None or filter(row):
	        	r = row[cols]
	        	if r not in results: results[r] = 0
	        	results[r]+=1
	    return results # 返回一个字典
		

def make_samples():
	return [
	[1, 'S', -1],
	[1, 'M', -1],
	[1, 'M',  1],
	[1, 'S',  1],
	[1, 'S', -1],
	[2, 'S', -1],
	[2, 'M', -1],
	[2, 'M',  1],
	[2, 'L',  1],
	[2, 'L',  1],
	[3, 'L',  1],
	[3, 'M',  1],
	[3, 'M',  1],
	[3, 'L',  1],
	[3, 'L', -1],
	]

if __name__ == '__main__':
	samples = make_samples()
	nb = NaiveBayesian()
	nb.train(samples)
	instance = [2, 'S']
	type, prop = nb.classify(instance)
	print('class of instance', instance, 'is', type, 'with prop', prop)
