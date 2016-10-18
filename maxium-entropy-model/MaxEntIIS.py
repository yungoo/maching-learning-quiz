from numpy import *
from math import *

class FeatureFunction:
    def __init__(self, index, value, label):
        self.index = index
        self.value = value
        self.label = label

    def apply(self, features, label):
        if features[self.index] == self.value and label == self.label:
            return 1
        return 0

class MaxEntIIS(object):
    """docstring for MaxEntIIS"""
    def __init__(self):
        super(MaxEntIIS, self).__init__()
        self.ITERATIONS = 100
        self.EPSION = 0.001
        self.N = 0
        self.minY = 0
        self.maxY = 0
        self.empirical_expects = []
        self.w = []
        self.samples = []
        self.functions = []
        self.features = []
        self.f_sharp_cache = {}

    def load_data(self, filename):
        with open(filename) as f:
            for line in f:
                sample = line.strip().split(' ')
                sample = tuple([int(s[-1]) for s in sample])
                y = sample[0]
                X = sample[1:]
                self.samples.append((X, y))

    def _init_params(self):
        self.N = len(self.samples)
        self._create_feature_functions(self.samples)
        self.w = [0.0] * len(self.functions)
        self.empirical_expects = [0.0] * len(self.functions)
        self._calc_empirical_expects()

    def _create_feature_functions(self, instances):
        maxLabel = 0
        maxFeatures = [0] * (len(instances[0][0]))
        featureSet = set([])

        self.minY = 1
        for i, instance in enumerate(instances):
            if instance[1] > maxLabel:
                maxLabel = instance[1]
            for j in range(len(instance[0])):
                if instance[0][j] > maxFeatures[j]:
                    maxFeatures[j] = instance[0][j]
            featureSet.add(instance[0])

        self.features = list(featureSet)
        self.maxY = maxLabel

        for i, feature in enumerate(maxFeatures):
            for x in range(feature + 1):
                for y in range(self.minY, maxLabel + 1):
                    self.functions.append(FeatureFunction(i, x, y))

        print("# features = ", len(self.features))
        print("# functions = ", len(self.functions))

    def _calc_empirical_expects(self):
        for instance in self.samples:
            y = instance[1]
            for i, function in enumerate(self.functions):
                self.empirical_expects[i] += function.apply(instance[0], y)
        for i, ep in enumerate(self.empirical_expects):
            self.empirical_expects[i] /= 1.0 * self.N
            
        print('empirical_expects', self.empirical_expects)

    def _calc_prob_y_given_x(self):
        cond_prob = [[0.0 for col in range(self.maxY + 1)] for rows in range(len(self.features))]
        for y in range(self.minY, self.maxY + 1):
            for i, feature in enumerate(self.features):
                z = 0.0
                for j, function in enumerate(self.functions):
                    z += self.w[j] * function.apply(feature, y)
                cond_prob[i][y] = exp(z)
        for i in range(len(self.features)):
            normalize = 0.0
            for y in range(self.minY, self.maxY+1):
                normalize += cond_prob[i][y]
            for y in range(self.minY, self.maxY+1):
                cond_prob[i][y] /= normalize
        return cond_prob

    def _apply_f_sharp(self, feature, y):
        key = (feature, y)
        if key in self.f_sharp_cache:
            return self.f_sharp_cache[key]
        sum = 0
        for i, function in enumerate(self.functions):
            sum += function.apply(feature, y)

        self.f_sharp_cache[key] = sum

        return sum

    def _iis_solve_delta(self, empirical_e, fi):
        delta = 0.0
        f_newton = 0.0
        df_newton = 0.0
        p_yx = self._calc_prob_y_given_x()

        for iters in range(0,50):
            f_newton = df_newton = 0.0
            for i, instance in enumerate(self.samples):
                feature = instance[0]
                index = self.features.index(feature)
                for y in range(self.minY, self.maxY+1):
                    f_sharp = self._apply_f_sharp(feature, y)
                    prod = p_yx[index][y] * self.functions[fi].apply(feature, y) * exp(delta * f_sharp)
                    f_newton += prod
                    df_newton += prod * f_sharp
            f_newton = empirical_e - f_newton / self.N
            df_newton = -df_newton / self.N

            if abs(f_newton) < 0.0000001:
                return delta

            ratio = f_newton / df_newton
            delta -= ratio
            if abs(ratio) < self.EPSION:
                return delta

        raise Exception('IIS did not converge')

    def train(self):
        self._init_params()
        for k in range(self.ITERATIONS):
            for i in range(len(self.functions)):
                delta = self._iis_solve_delta(self.empirical_expects[i], i)
                self.w[i] += delta
            print('iterations', k, ':', self.w)

    def classify(self, instance):
        max = 0.0
        label = 0

        for y in range(self.minY, self.maxY+1):
            sum = 0.0
            for i,function in enumerate(self.functions):
                sum += exp(self.w[i] * function.apply(instance, y))
            if sum > max:
                max = sum
                label = y
        return label

if __name__ == '__main__':
    maxent = MaxEntIIS()
    maxent.load_data('zoo.train')
    maxent.train()

    verified = 0
    total = 0
    with open('zoo.test') as f:
        for line in f:
            instance = line.strip().split(' ')
            instance = tuple([int(s[-1]) for s in instance])
            total += 1
            predict = maxent.classify(instance[1:])
            if predict == instance[0]:
                verified += 1

    print('accuracy:', 1.0 * verified / total)
