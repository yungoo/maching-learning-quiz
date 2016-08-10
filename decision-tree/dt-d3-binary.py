# -*- coding: utf-8 -*-
__author__ = 'Wsine'

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
    numEntries = len(dataSet)
    baseEntropy = dt.entropy(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    bestSets = None
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        for value in uniqueVals:
            tb, fb = dt.divide_set(dataSet, i, value)
            prob = len(tb)/float(numEntries)
            infoGain = baseEntropy - prob * dt.entropy(tb) - (1 - prob) * dt.entropy(fb)
            if (infoGain > bestInfoGain and len(fb) > 0 and len(fb) > 0):
                bestInfoGain = infoGain
                bestFeature = (i, value)
                bestSets = (tb, fb)

    if bestInfoGain > 0:
        return (bestFeature, bestSets)
    return (None, None)

def createTree(dataSet, labels):
    """
    输入：数据集，特征标签
    输出：决策树
    描述：递归构建决策树，利用上述的函数
    """
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return DecisionNode(results = dt.unique_counts(dataSet))
    if len(dataSet[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return DecisionNode(results = dt.majority_class(classList))

    bestFeatValue, bestSets = chooseBestFeatureToSplit(dataSet)
    if bestFeatValue == None:
        return DecisionNode(results = dt.unique_counts(dataSet))
    else:
        bestFeat = bestFeatValue[0]
        bestValue = bestFeatValue[1]
        bestFeatLabel = labels[bestFeat]

        sub_labels = labels[:bestFeat]
        sub_labels.extend(labels[bestFeat+1:])

        trueBranch = createTree(bestSets[0], sub_labels)  #递归调用
        falseBranch = createTree(bestSets[1], sub_labels)
        return DecisionNode(col = bestFeat, label = bestFeatLabel, value = bestValue,
                            tb = trueBranch, fb = falseBranch)

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

    labels = ['source', 'country', 'clicked', 'age']
    return (my_data, labels)

def main():
    dataSet, labels = createDataSet2()

    desicionTree = createTree(dataSet, labels)
    # dt.storeTree(desicionTree, 'classifierStorage.txt')
    # desicionTree = dt.grabTree('classifierStorage.txt')
    dt_plotter.createPlot(desicionTree)
    testSet = createTestSet()
    print('classifyResult:\n', dt.classify_all(desicionTree, testSet))

if __name__ == '__main__':
    main()