import networkx as nx
import matplotlib.pyplot as plt
import random
import generateAllQueries as gq
import constants as con
import dataManage as dm
import math
import operator
import time
import constants
import os
import csv

adjacency_list = []
#printNameCounts = {}

#returns tuples
def pointsInCircle(centerP,r,n=100, startIndex = 0):
    #print n
    startAngle = math.floor(2*math.pi*startIndex/n)
    return [addPoints(centerP, (math.cos(startAngle + 2*math.pi*x/n)*r, math.sin(startAngle + 2*math.pi*x/n)*r)) for x in xrange(0,n)]

def addPoints(point0, point1):
    return tuple(map(operator.add, point0, point1))

##if True:
##    G=nx.Graph()
##    G.add_node(1,pos=(1,1))
##    G.add_node(2,pos=(2,2))
##    G.add_edge(1,2)
##    pos=nx.get_node_attributes(G,'pos')
##    print pos

def generateGraph(isTest, dataType, timeNowString):
    _, comTopcomQueryName, comTopTopQueryName, comTopQueryName = gq.generateQueries()
    topicGraph = nx.Graph()
    #oneCirclePoints = pointsInCircle((0,0), 600, len(con.futureDefinitions)*(len(con.topicsSpecific)+ len(con.topicsGeneral)))
    #Points in multiple Circles
    center = (350, 350)
    centerPoints = pointsInCircle(center, 1400,len(con.futureDefinitions),1)
    multipleCirclePoints = []
    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
        topicsSpecific = con.futureTopics[futureName]
        topicsGeneral = gq.dictionaryJoin([con.marketTopics, con.supplyAndDemand])
        centerPoint = centerPoints.pop()
        topicGraph.add_node(futureName, pos=centerPoint, cc='green', label=futureName)
        multipleCirclePoints = pointsInCircle(centerPoint, 550, len(topicsSpecific)+ len(topicsGeneral))+multipleCirclePoints
    points = multipleCirclePoints
    #print points
    #Build Nodes
                
    #commodity + specific topic
    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
        topicsSpecific = con.futureTopics[futureName]
        topicsGeneral = gq.dictionaryJoin([con.marketTopics, con.supplyAndDemand])
        for futureTopicName, futureTopicPhrase in topicsSpecific.iteritems(): #returns a dictionary
            nodeName = futureName +'_'+ futureTopicName
            position=points.pop()
            #print position
            #print nodeName
            topicGraph.add_node(nodeName, pos=position, cc='blue', label=futureTopicName)
        #commodity + general topics
        for generalTopicName, generalTopicPhrase in topicsGeneral.iteritems():
            nodeName = futureName +'_'+ generalTopicName
            position=points.pop()
            #print position
            #print nodeName
            topicGraph.add_node(nodeName, pos=position, cc='red', label=generalTopicName)
#   edges #dont use the time stamps
    timeNowString = 'phraseTopics' #hardcoded for testing graph drawing vaibhav
    if dataType is not 'twitter':
         allGoogle  = dm.readAllCountFraction(isTest, dataType, timeNowString)
    # print 'allGogle:\n'
    # print allGoogle
    if dataType is not 'twitter':
        (allGoogleW, _) = dm.readAllCount(isTest, dataType, 'd', timeNowString) #(data, timeStamps)
    # print 'allGogleW:\n '
    # print allGoogleW
    (allGoogleD, _) = dm.readAllCount(isTest, dataType, 'h', timeNowString) #(data, timeStamps)
    # print 'allGogleD:\n '
    # print allGoogleD
    #print "%-20sRead %d Results"%(timeNowString, len(allGoogle))
    createOneGraph(topicGraph, timeNowString, isTest, allGoogleD, 'h') #draw obly
    if dataType is not 'twitter':
        createOneGraph(topicGraph, timeNowString, isTest, allGoogleW, 'd') #draw only
        nodes, edges, edgeWeightsDict = createOneGraph(topicGraph, timeNowString, isTest, allGoogle, 'r')
    return (nodes, edges, allGoogle)


def createOneGraph(topicGraph, timeNowString, isTest, allGoogleDataItems, dataName):
    _, comTopcomQueryName, comTopTopQueryName, comTopQueryName = gq.generateQueries()
    printNameCounts = {}
    # comTopcomQueryName, two commodities, one Topic
    # comTopTopQueryName, one commidity and two topics
    # comTopQueryName, just one commodity and one topic

    # #create a file containing edge details: futureName_topicName -> futureName, edgeWeight. Dir: E:\Research\data\graphs\heatmaps\graphMatrix.txt
    # fileName = constants.ROOTdata + 'graphs' + '\\heatmaps\\' + 'graphMatrix' + '.txt'
    #
    # #check if file already exists
    # if not os.path.exists(os.path.dirname(fileName)):
    #     os.makedirs(os.path.dirname(fileName))
    #
    # with open(fileName, 'a') as stream:
    #     writer = csv.writer(stream, delimiter='\t')



    #print comTopQueryName
    # each com and its topics
    for queryName, printName in comTopQueryName:
        (futureName, topicName) = tuple(printName.split("_"))
        #firstly we need to unpack tuple, and then iterate over dictionary keys, vaibhav

        #for allGoogleDataItems in allGoogleData:
        if printName in allGoogleDataItems: # and allGoogleW[printName] > 5 and allGoogleD[printName] > 5: #problem is with unpacking dictionary inside a tuple
            googleCount = allGoogleDataItems[printName]
            #print "****************%-25s %6d "%(printName, googleCount)
            #edgeWeight = round(googleCount)
            if googleCount <= -1:
                googleCount = 1
            edgeWeight = round(math.log(googleCount + 1, 2) * 1)
            #writer.writerow((futureName +'_'+ topicName, futureName, edgeWeight))
            if printName not in printNameCounts:
                printNameCounts[printName] = googleCount
            if printName not in adjacency_list:
                adjacency_list.append(printName)
            topicGraph.add_edge(futureName +'_'+ topicName, futureName, color='green', weight=edgeWeight)
    for queryName, printName in comTopTopQueryName:
        # print len(comTopTopQueryName)
        (futureName, topicName0, topicName1) = tuple(printName.split("_"))

        # print '*************'
        # print len(allGoogleDataItems)
        # print '*************'
        #for allGoogleDataItems in allGoogleData:
        if printName in allGoogleDataItems: # and allGoogleW[printName] > 5 and allGoogleD[printName] > 5:
            googleCount = allGoogleDataItems[printName]
            #print "%-25s %6d "%(printName, googleCount)
            #edgeWeight = round(googleCount)
            if googleCount <= -1:
                googleCount = 1
            edgeWeight = round(math.log(googleCount+1, 2)*1)
            if printName not in printNameCounts:
                printNameCounts[printName] = googleCount
            if printName not in adjacency_list:
                adjacency_list.append(printName)
            #writer.writerow((futureName +'_'+ topicName0, futureName +'_'+ topicName1, edgeWeight))
            #adjacency_list.append((futureName +'_'+ topicName0, futureName +'_'+ topicName1, edgeWeight))
            topicGraph.add_edge(futureName +'_'+ topicName0, futureName +'_'+ topicName1, color='blue', weight=edgeWeight)
    for queryName, printName in comTopcomQueryName:
        (futureName0, topicName, futureName1) = tuple(printName.split("_"))

        #print allGoogleDataItems
        #for allGoogleDataItems in allGoogleData:
        if printName in allGoogleDataItems:
            googleCount = allGoogleDataItems[printName]
            #print "%-25s %2.3f"%(printName, googleCountRatio)
            #edgeWeight = round(googleCountRatio)
            if googleCount <= -1:
                googleCount = 1
            edgeWeight = round(math.log(googleCount+1, 2)*1)
            if printName not in printNameCounts:
                printNameCounts[printName] = googleCount
            if printName not in adjacency_list:
                adjacency_list.append(printName)
            #writer.writerow((futureName0 + '_' + topicName, futureName1 + '_' + topicName, edgeWeight))
            #adjacency_list.append((futureName0 + '_' + topicName, futureName1 + '_' + topicName, edgeWeight))
            topicGraph.add_edge(futureName0 +'_'+ topicName, futureName1 +'_'+ topicName, color='red', weight=edgeWeight)
    #print adjacency_list
    nodes, edges, edgeWeightsDict = displayGraph(topicGraph, timeNowString, isTest, dataName)
    return (nodes, edges, edgeWeightsDict)

def displayGraph(topicGraph, timeNowString, isTest, dataName):
    edgeWeightsDict = {}
    plt.clf()
    plt.cla()   # Clear axis
    fig=plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_aspect(1)
    #ax.autoscale(False)
    #print timeNowString
    pos=  nx.get_node_attributes(topicGraph,'pos')
    #extract colors and widths
    edges = topicGraph.edges()
    # print 'edges'
    print edges
    nodes = topicGraph.nodes()##print nodes
    #print 'nodes'
    #print nodes
    #nodeColors = [graph[u]['color'] for u in nodes]
    edgeColors = [topicGraph[u][v]['color'] for u,v in edges]
    ##print colors
    #this could be our feature vector matrix or list representing the edge weights
    edgeWeights = [topicGraph[u][v]['weight'] for u,v in edges]
    print edgeWeights
    idx = 0
    for u, v in edges:
        edgeWeightsDict[(u, v)] = edgeWeights[idx]
        idx = idx + 1
    #print edgeWeightsDict

    #build a dict with edge pair as keys and connecting weight as value

    colorAttributes = nx.get_node_attributes(topicGraph,'cc')
    nodeColors = [colorAttributes[u] for u in nodes]
    nx.draw(topicGraph, pos, edges=edges, edge_color=edgeColors, width=edgeWeights, node_size=150, alpha=0.25, node_color=nodeColors)
    nodeLabels = nx.get_node_attributes(topicGraph,'label')
    nx.draw_networkx_labels(topicGraph, pos, nodeLabels, font_size=5, font_weight= 'bold')
    # titles
    if isTest:
        dataType = 'test_'
    else: dataType = ''

    # #extract timestamp from google files
    os.chdir('E:\\Research\\data\\google')
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-3]
    newest = newest[7:-4]
    newest = newest.replace("@", "_")
    plt.title(dataName + '_' + newest)
    fileName = constants.ROOTdata + 'graphs' + '\\' + dataName +'\\'+newest+'.png'
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    #print fileName
    plt.savefig(fileName, dpi=200, bbox_inches='tight')
    #if True:
    plt.show()
    plt.close(fig)
    return (nodes, edges, edgeWeightsDict)
    

#generateGraph(False, 'google','test graph') #False
# generateGraph(False, 'twitter','test graph') #False


# #
# G = nx.Graph()
# G.add_edge(1,2,color='r',weight=2)
# G.add_edge(2,3,color='b',weight=4)
# G.add_edge(3,4,color='g',weight=6)
# ##
# pos = nx.circular_layout(G)
# ##
# edges = G.edges()
# colors = [G[u][v]['color'] for u,v in edges]
# weights = [G[u][v]['weight'] for u,v in edges]
# ##
# nx.draw(G, pos, edges=edges, edge_color=colors, width=weights)
# plt.show()

    
#drawGraph(topicGraph, pos) # Need to ask about its usage or possible implementation

#g = nx.random_graphs.erdos_renyi_graph(10,0.5)
#colors = [(random.random(), random.random(), random.random()) for _i in range(10)]
#nx.draw_circular(g, node_color=colors)
#plt.show()
