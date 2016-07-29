#!/usr/bin/env python
# -*- coding: utf8 -*-

# 作者：黄耀鹏
# 链接：https://zhuanlan.zhihu.com/p/20794583
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from math import log

class decisionnode:
    def __init__(self,col = -1,value = None, results = None, tb = None,fb = None):
        self.col = col   # col是待检验的判断条件所对应的列索引值
        self.value = value # value对应于为了使结果为True，当前列必须匹配的值
        self.results = results #保存的是针对当前分支的结果，它是一个字典
        self.tb = tb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点
        self.fb = fb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点

# 对y的各种可能的取值出现的个数进行计数.。其他函数利用该函数来计算数据集和的混杂程度
def uniquecounts(rows):
    results = {}
    for row in rows:
        #计数结果在最后一列
        r = row[-1]
        if r not in results: results[r] = 0
        results[r]+=1
    return results # 返回一个字典

def entropy(rows):
    results = uniquecounts(rows)
    #开始计算熵的值
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log(p, 2)
    return ent

# 随机放置的数据项出现于错误分类中的概率
def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp =0
    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts: # 这个循环是否可以用（1-p1）替换？
            if k1 == k2: continue
            p2 = float(counts[k2])/total
            imp+=p1*p2
    return imp

# 改进giniimpurity
def giniimpurity_2(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for k1 in counts.keys():
        p1 = float(counts[k1])/total
        imp+= p1*(1-p1)
    return imp

#在某一列上对数据集进行拆分。可应用于数值型或因子型变量
def divideset(rows, column, value):
    #定义一个函数，判断当前数据行属于第一组还是第二组
    split_function = None
    if isinstance(value,int) or isinstance(value,float):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column] == value
    # 将数据集拆分成两个集合，并返回
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return(set1,set2)

# 以递归方式构造树
def buildtree(rows, scoref = entropy):
    if len(rows)==0 : return decisionnode()

    # 经验熵
    empiricial_entropy = scoref(rows)
    
    # 定义一些变量以记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    
    # 选择最合适的特征列
    column_count = len(rows[0]) - 1
    for col in range(column_count):
        # 在当前列中生成一个由不同值构成的序列
        column_values = set([example[col] for example in rows])
        
        # 根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_values:
            (set1, set2) = divideset(rows, col, value)
            
            # 信息增益
            p = float(len(set1)) / len(rows)
            # 某一个值划分信息增益
            gain = empiricial_entropy - p*scoref(set1) - (1-p)*scoref(set2)

            # 根据信息增益值选择最合适的值
            if gain > best_gain and len(set1)>0 and len(set2)>0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
                
        # if best_criteria != None:                
        #     print 'The best gain ration is:', best_gain, 'by:', best_criteria, '\n->tb:', best_sets[0],'\n->fb:', best_sets[1]

    #创建子分支
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0], scoref)  #递归调用
        falseBranch = buildtree(best_sets[1], scoref)
        return decisionnode(col = best_criteria[0], value = best_criteria[1],
                            tb = trueBranch, fb = falseBranch)
    else:
        return decisionnode(results = uniquecounts(rows))

# 决策树的显示
def printtree(tree, indent = '\t', left=''):
    # 是否是叶节点
    if tree.results != None:
        print str(tree.results)
    else:
        # 打印判断条件
        print str(tree.col) + ":" + str(tree.value) + "? "
        #打印分支
        print left + "T->",
        printtree(tree.tb, indent, left = left + indent)
        print left + "F->",
        printtree(tree.fb, indent, left = left + indent)


# 对新的观测数据进行分类
def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value: branch = tree.tb
            else: branch = tree.fb
        else:
            if v == tree.value : branch = tree.tb
            else: branch = tree.fb
        return classify(observation, branch)

# 决策树的剪枝
def prune(tree, mingain, scoref = entropy):
    # 如果分支不是叶节点，则对其进行剪枝
    if tree.tb.results == None:
        prune(tree.tb, mingain)

    if tree.fb.results == None:
        prune(tree.fb, mingain)

    # 如果两个子分支都是叶节点，判断是否能够合并
    if tree.tb.results != None and tree.fb.results != None:
        #构造合并后的数据集
        tb,fb = [],[]
        for v,c in tree.tb.results.items():
            tb += [[v]]*c
        for v,c in tree.fb.results.items():
            fb += [[v]]*c
        #检查熵的减少量
        delta = scoref(tb + fb) - (scoref(tb) + scoref(fb) / 2)
        print "(" + str(tree.col) + ":" + str(tree.value) + ") -> delta: ", delta
        if delta <= mingain:
            print "merging ->" + str(tree.col) + ":" + str(tree.value) + "? "

            # 合并分支
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts(tb+fb)

# test
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

# divideset(my_data, 2, 'yes')
# giniimpurity(my_data)
# giniimpurity_2(my_data)
# tree = buildtree(my_data)
# printtree(tree = tree, indent='\t')

# print classify(['(direct)','USA','yes', 5], tree)

# test
tree = buildtree(my_data, scoref = entropy)
printtree(tree)
prune(tree, 0.1, scoref = entropy)
printtree(tree)