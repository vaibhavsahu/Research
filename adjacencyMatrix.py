import numpy as np
import os
import constants
import dataManage as dm
import generateAllQueries as gq
import matplotlib.pyplot as plt
def adjacencyMatrix(timeNowString, threashold, onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    _, comTopcomQueryName, comTopTopQueryName, comTopQueryName = gq.generateQueries(onlyCommoditiesList)
    adjacencyDic = {}
    nodes = set()

    (rawHour, _) = dm.readAllCount(False, 'google', 'h', timeNowString)
    (rawDay, _) = dm.readAllCount(False, 'google', 'd', timeNowString)
    # each com and its topics
    for queryName, printName in comTopQueryName:
        (futureName, topicName) = tuple(printName.split("_"))
        # firstly we need to unpack tuple, and then iterate over dictionary keys, vaibhav
        edgeWeight = 0.0
        if printName in rawHour:
            if rawDay[printName] != 0 and rawHour[printName] / (1.0*rawDay[printName]) >= threashold:
                edgeWeight = 1.0
        adjacencyDic[(futureName, printName)] = edgeWeight
        adjacencyDic[(printName, futureName)] = edgeWeight
        nodes.add(futureName)
        nodes.add(printName)
    for queryName, printName in comTopTopQueryName:
        # print len(comTopTopQueryName)
        (futureName, topicName0, topicName1) = tuple(printName.split("_"))

        edgeWeight = 0.0
        if printName in rawHour:
            if rawDay[printName] != 0 and rawHour[printName] / (1.0 * rawDay[printName]) >= threashold:
                edgeWeight = 1.0
        node0 = futureName + '_'+ topicName0
        node1 = futureName + '_'+ topicName1
        adjacencyDic[(node0, node1)] = edgeWeight
        adjacencyDic[(node1, node0)] = edgeWeight
        nodes.add(node0)
        nodes.add(node1)

    for queryName, printName in comTopcomQueryName:
        (futureName0, topicName, futureName1) = tuple(printName.split("_"))

        edgeWeight = 0.0
        if printName in rawHour:
            if rawDay[printName] != 0 and rawHour[printName] / (1.0 * rawDay[printName]) >= threashold:
                edgeWeight = 1.0
        node0 = futureName0 + '_'+ topicName
        node1 = futureName1 + '_'+ topicName
        adjacencyDic[(node0, node1)] = edgeWeight
        adjacencyDic[(node1, node0)] = edgeWeight
        nodes.add(node0)
        nodes.add(node1)
    # print adjacency_list
    return (nodes, adjacencyDic)

def adjacencyDicToMatrix(nodes, adjacencyDic):
    nodeList = sorted(list(nodes))
    # make boolean connectivity graph based on threashold
    connectMatrix = np.zeros((len(nodeList), len(nodeList)))
    for n1, i in zip(nodeList, range(len(nodeList))):
        for n2, j in zip(nodeList, range(len(nodeList))):
            if (n1, n2) in adjacencyDic:
                connectMatrix[i, j] = adjacencyDic[(n1, n2)]
    return (nodeList, connectMatrix)


def displayAdjacencyMatrix(timeNowString, threashold, nodeList, connectMatrix, onlyCommoditiesList):
    fig, ax = plt.subplots()
    im = ax.imshow(connectMatrix, cmap='hot')
    ax.set_xticks(np.arange(len(nodeList)))
    ax.set_yticks(np.arange(len(nodeList)))

    ax.set_xticklabels(nodeList, fontsize=7)
    ax.set_yticklabels(nodeList, fontsize=7)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    commodityString = "_".join(onlyCommoditiesList)
    ax.set_title(commodityString + "_" + '{:06.4f}'.format(threashold) +'_'+timeNowString)
    fileName = timeNowString+ '\\' + commodityString + '_' +'{:06.2f}'.format(threashold) + timeNowString +'.png'
    if not os.path.exists(os.path.dirname(fileName)):
       os.makedirs(os.path.dirname(fileName))
    fig.tight_layout()
    plt.savefig(fileName)
    plt.clf()
    #plt.show()
#
