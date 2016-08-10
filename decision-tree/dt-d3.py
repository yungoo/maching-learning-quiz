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
    baseEntropy = dt.entropy(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        splitInfo = 0.0
        for value in uniqueVals:
            subDataSet, _ = dt.divide_discrete_set(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * dt.entropy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def createTree(dataSet, labels, decisionValue=None):
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
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    
    children = []
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        tb, _ = dt.divide_discrete_set(dataSet, bestFeat, value)
        children.append(createTree(tb, subLabels, decisionValue=value))

    return DecisionNode(col = bestFeat, label = bestFeatLabel, value = decisionValue,
                            children = children)

def main():
    dataSet, labels = createDataSet()

    labels_tmp = labels[:] # 拷贝，createTree会改变labels
    desicionTree = createTree(dataSet, labels_tmp)
    #storeTree(desicionTree, 'classifierStorage.txt')
    #desicionTree = grabTree('classifierStorage.txt')
    dt_plotter.createPlot(desicionTree)
    # testSet = createTestSet()
    # print('classifyResult:\n', classifyAll(desicionTree, labels, testSet))

if __name__ == '__main__':
    main()