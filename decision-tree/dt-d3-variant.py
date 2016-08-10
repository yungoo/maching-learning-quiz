#!/usr/bin/env python
# -*- coding: utf8 -*-

# 作者：黄耀鹏
# 链接：https://zhuanlan.zhihu.com/p/20794583
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from math import log
import dt_base as dt
from dt_base import DecisionNode
import dt_plotter

# 以递归方式构造树
def build_tree(rows, labels, scoref = dt.entropy):
    if len(rows)==0 : return DecisionNode()

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
            (set1, set2) = dt.divide_set(rows, col, value)
            
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
        sub_labels = labels[:best_criteria[0]]
        sub_labels.extend(labels[best_criteria[0]+1:])
        trueBranch = build_tree(best_sets[0], sub_labels, scoref)  #递归调用
        falseBranch = build_tree(best_sets[1], sub_labels, scoref)
        return DecisionNode(col = best_criteria[0], label = labels[best_criteria[0]], value = best_criteria[1],
                            tb = trueBranch, fb = falseBranch)
    else:
        return DecisionNode(results = dt.unique_counts(rows))

# 决策树的剪枝
def prune(tree, mingain, scoref = dt.entropy):
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
            tree.results = unique_counts(tb+fb)

def main():
    #'source', 'country', 'clicked faq or not', 'age', 'buy service type after trial'
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

    my_labels = ['source', 'country', 'clicked faq or not', 'age']
    tree = build_tree(my_data, my_labels)
    dt.print_tree(tree = tree, indent='\t')
    dt_plotter.createPlot(tree)
    # print classify(['(direct)','USA','yes', 5], tree)

if __name__ == '__main__':
    main()