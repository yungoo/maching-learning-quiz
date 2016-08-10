#!/usr/bin/env python
# -*- coding: utf8 -*-

# 作者：黄耀鹏
# 链接：https://zhuanlan.zhihu.com/p/20794583
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from math import log
import operator

class DecisionNode:
    def __init__(self, col = -1, label=None, value = None, results = None, tb = None,fb = None,children = None):
        self.col = col   # col是待检验的判断条件所对应的列索引值
        self.label = label
        self.value = value # value对应于为了使结果为True，当前列必须匹配的值
        self.results = results #保存的是针对当前分支的结果，它是一个字典
        self.tb = tb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点
        self.fb = fb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点
        self.children = children

def unique_counts(rows):
    '''
    对y的各种可能的取值出现的个数进行计数.。其他函数利用该函数来计算数据集和的混杂程度
    '''
    results = {}
    for row in rows:
        #计数结果在最后一列
        r = row[-1]
        if r not in results: results[r] = 0
        results[r]+=1
    return results # 返回一个字典

def majority_class(classList):
    """
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return {sortedClassCount[0][0]: sortedClassCount[0][1]}

def entropy(rows):
    '''
    计算熵的值
    '''
    results = unique_counts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log(p, 2)
    return ent

def gini_impurity(rows):
    '''
    随机放置的数据项出现于错误分类中的概率
    '''
    total = len(rows)
    counts = unique_counts(rows)
    imp =0
    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts: # 这个循环是否可以用（1-p1）替换？
            if k1 == k2: continue
            p2 = float(counts[k2])/total
            imp+=p1*p2
    return imp

def gini_impurity_2(rows):
    '''
    改进giniimpurity
    '''
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0
    for k1 in counts.keys():
        p1 = float(counts[k1])/total
        imp+= p1*(1-p1)
    return imp

def divide_set(rows, column, value):
    """
    输入：数据集，选择维度，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；去除选择维度中等于选择值的项
    """
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda record: record[column] >= value
    else:
        split_function = lambda record: record[column] == value

    tb = []
    fb = []
    for row in rows:
        features = row[:column]
        features.extend(row[column+1:])
        if split_function(row):
            tb.append(features)
        else:
            fb.append(features)

    return (tb, fb)

def divide_discrete_set(rows, column, value):
    """
    输入：数据集，选择维度，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；去除选择维度中等于选择值的项
    """
    tb = []
    fb = []
    for row in rows:
        features = row[:column]
        features.extend(row[column+1:])
        if row[column] == value:
            tb.append(features)
        else:
            fb.append(features)

    return (tb, fb)

def print_tree(tree, indent = '\t', left=''):
    '''
    决策树的显示
    '''
    # 是否是叶节点
    if tree.results != None:
        print str(tree.results)
    else:
        if tree.children != None:
            # 打印判断条件
            print str(tree.col) + ":" + str(tree.value) + "? "
            #打印分支
            for node in tree.children:
                print left + str(node.value) + "->",
                print_tree(node, indent, left = left + indent)
        else:
            # 打印判断条件
            print str(tree.col) + ":" + str(tree.value) + "? "
            #打印分支
            print left + "T->",
            print_tree(tree.tb, indent, left = left + indent)
            print left + "F->",
            print_tree(tree.fb, indent, left = left + indent)

def classify(observation, tree):
    '''
    对新的观测数据进行分类
    '''
    if tree.results != None:
        return tree.results
    else:
        branch = None
        v = observation[tree.col]

        if tree.children == None:
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value: 
                    branch = tree.tb
                else: branch = tree.fb
            else:
                if v == tree.value : branch = tree.tb
                else: branch = tree.fb
        else:
            for node in tree.children:
                if v == node.value:
                    branch = node
        print branch
        return classify(observation, branch)
        
def classify_all(tree, testDataSet):
    """
    输入：决策树，分类标签，测试数据集
    输出：决策结果
    描述：跑决策树
    """
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(classify(testVec, tree))
    return classLabelAll

def storeTree(inputTree, filename):
    """
    输入：决策树，保存文件路径
    输出：
    描述：保存决策树到文件
    """
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    """
    输入：文件路径名
    输出：决策树
    描述：从文件读取决策树
    """
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)