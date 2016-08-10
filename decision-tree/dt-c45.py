# -*- coding: utf-8 -*-
__author__ = 'Wsine'

from math import log
import dt_base as dt
from dt_base import DecisionNode
import dt_plotter

def chooseBestFeatureToSplit(dataSet):
    """
    输入：数据集
    输出：最好的划分维度
    描述：选择最好的数据集划分维度
    """
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = dt.entropy(dataSet)
    bestInfoGainRatio = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        # splitInfo = 0.0
        for value in uniqueVals:
            subDataSet, _ = dt.divide_discrete_set(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * dt.entropy(subDataSet)
            # splitInfo += -prob * log(prob, 2)
        infoGain = baseEntropy - newEntropy
        # if (splitInfo == 0): # fix the overflow bug
        #     continue
        infoGainRatio = infoGain / baseEntropy
        if (infoGainRatio > bestInfoGainRatio):
            bestInfoGainRatio = infoGainRatio
            bestFeature = i
    return (bestFeature, bestInfoGainRatio)

def createTree(dataSet, labels, epsilon, decisionValue=None):
    """
    输入：数据集，特征标签
    输出：决策树
    描述：递归构建决策树，利用上述的函数
    """
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return DecisionNode(results = dt.unique_counts(dataSet), value=decisionValue)
    if len(dataSet[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return DecisionNode(results = dt.majority_class(classList), value=decisionValue)

    bestFeat, bestInfoGainRatio = chooseBestFeatureToSplit(dataSet)

    # print bestInfoGainRatio
    # if bestInfoGainRatio < epsilon:
    #     # 如果特征的信息增益比小于阈值，返回类别最多的节点
    #     return DecisionNode(results = dt.majority_class(classList), value=decisionValue)

    bestFeatLabel = labels[bestFeat]
    del(labels[bestFeat])

    children = []
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        children.append(createTree(dt.divide_discrete_set(dataSet, bestFeat, value)[0], subLabels, epsilon, decisionValue=value))

    return DecisionNode(col = bestFeat, label = bestFeatLabel, value = decisionValue,
                            children = children)

def createDataSet():
    """
    outlook->  0: sunny | 1: overcast | 2: rain
    temperature-> 0: hot | 1: mild | 2: cool
    humidity-> 0: high | 1: normal
    windy-> 0: false | 1: true 
    """
    dataSet = [[0, 0, 0, 0, 'N'], 
               [0, 0, 0, 1, 'N'], 
               [1, 0, 0, 0, 'Y'], 
               [2, 1, 0, 0, 'Y'], 
               [2, 2, 1, 0, 'Y'], 
               [2, 2, 1, 1, 'N'], 
               [1, 2, 1, 1, 'Y']]
    labels = ['outlook', 'temperature', 'humidity', 'windy']
    return dataSet, labels

def createTestSet():
    """
    outlook->  0: sunny | 1: overcast | 2: rain
    temperature-> 0: hot | 1: mild | 2: cool
    humidity-> 0: high | 1: normal
    windy-> 0: false | 1: true 
    """
    testSet = [[0, 1, 0, 0], 
               [0, 2, 1, 0], 
               [2, 1, 1, 0], 
               [0, 1, 1, 1], 
               [1, 1, 0, 1], 
               [1, 0, 1, 0], 
               [2, 1, 0, 1]]
    return testSet

def createDataSet2():
    my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

    labels = ['source', 'country', 'click', 'age']
    return (my_data, labels)

def trainSamples():
    '''
    训练样本
    Features:
    年龄: (3: 老年, 2: 中年, 1: 青年)
    是否有工作: (1: 是, 2: 否)
    有自己的房子: (1: 是, 2: 否)
    信贷情况: (1: 非常好, 2: 好, 3: 一般)
    是否可贷[类别]: (1: 是, 2: 否)
    '''
    samples = [
        [1, 2, 2, 3, 2],
        [1, 2, 2, 2, 2],
        [1, 1, 2, 2, 1],
        [1, 1, 1, 3, 1],
        [1, 2, 2, 3, 2],
        [2, 2, 2, 3, 2],
        [2, 2, 2, 2, 2],
        [2, 1, 1, 2, 1],
        [2, 2, 1, 1, 1],
        [2, 2, 1, 1, 1],
        [3, 2, 1, 1, 1],
        [3, 2, 1, 2, 1],
        [3, 1, 2, 2, 1],
        [3, 1, 2, 1, 1],
        [3, 2, 2, 3, 2],
    ]

    labels = ['age', 'has a job', 'has house', 'credit status']
    return [samples, labels]

def trainSamples2():
    my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

    labels = ['source', 'country', 'clicked', 'age']
    return (my_data, labels)

def main():
    dataSet, labels = createDataSet()

    labels_tmp = labels[:]
    desicionTree = createTree(dataSet, labels_tmp, 0.1)
    dt.print_tree(desicionTree)
    #storeTree(desicionTree, 'classifierStorage.txt')
    #desicionTree = grabTree('classifierStorage.txt')
    # testSet = createTestSet()
    # print('classifyResult:\n', dt.classify_all(desicionTree, testSet))
    dt_plotter.createPlot(desicionTree)

if __name__ == '__main__':
    main()