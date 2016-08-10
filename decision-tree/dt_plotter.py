import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', \
                            xytext=centerPt, textcoords='axes fraction', \
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def getNumLeafs(myTree):
    numLeafs = 0

    if myTree.results != None:
        return 1

    if myTree.children != None:
        for child in myTree.children:
            numLeafs += getNumLeafs(child)
    else:
        if myTree.tb.results == None:
            numLeafs += getNumLeafs(myTree.tb)
        else:
            numLeafs += 1

        if myTree.fb.results == None:
            numLeafs += getNumLeafs(myTree.fb)
        else:
            numLeafs += 1

    return numLeafs

def getTreeDepth(myTree):
    if myTree.results != None:
        return 1

    if myTree.children != None:
        maxDepth = 1
        for child in myTree.children:
            maxDepth = max(maxDepth, getNumLeafs(child) + 1)
        return maxDepth
    else:
        maxDepthLeft = 0
        if myTree.tb.results == None:
            maxDepthLeft = getTreeDepth(myTree.tb) + 1
        else:
            maxDepthLeft = 1

        maxDepthRight = 0
        if myTree.fb.results == None:
            maxDepthRight = getTreeDepth(myTree.fb) + 1
        else:
            maxDepthRight = 1

        return max(maxDepthLeft, maxDepthRight)

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    
    # leaf
    if myTree.results != None:
        plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalw
        plotNode(myTree.results.keys()[0], (plotTree.xOff, plotTree.yOff), parentPt, leafNode)
        plotMidText((plotTree.xOff, plotTree.yOff), parentPt, nodeTxt)
    else:
        firstStr = myTree.label
        cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalw, plotTree.yOff)
        plotMidText(cntrPt, parentPt, nodeTxt)
        plotNode(firstStr, cntrPt, parentPt, decisionNode)

        plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
        if myTree.children != None:
            for node in myTree.children:
                plotTree(node, cntrPt, str(node.value))
        else:
            if isinstance(myTree.value, int) or isinstance(myTree.value, float):
                falseLabel = ""
                trueLabel = (">= " + str(myTree.value))
            else:
                falseLabel = ""
                trueLabel = myTree.value
            plotTree(myTree.tb, cntrPt, trueLabel)
            plotTree(myTree.fb, cntrPt, falseLabel)
        plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalw = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalw
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()
