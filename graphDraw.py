import networkx as nx
import matplotlib.pyplot as plt
import random
import generateAllQueries as gq
import constants as con
import dataManage as dm
import math
import operator
import time

#returns tuples
def pointsInCircle(centerP,r,n=100):
    #print n
    shift = random.uniform(0,math.pi/n)
    return [addPoints(centerP, (math.cos(shift+2*math.pi*x/n)*r, math.sin(shift+2*math.pi*x/n)*r)) for x in xrange(0,n)]

def addPoints(point0, point1):
    return tuple(map(operator.add, point0, point1))

    

##if True:
##    G=nx.Graph()
##    G.add_node(1,pos=(1,1))
##    G.add_node(2,pos=(2,2))
##    G.add_edge(1,2)
##    pos=nx.get_node_attributes(G,'pos')
##    print pos

def generateGraph(isTest, timeNowString):
    comTopcomQueryName, comTopTopQueryName = gq.generateQueries()
    topicGraph = nx.Graph()
    #oneCirclePoints = pointsInCircle((0,0), 600, len(con.futureDefinitions)*(len(con.topicsSpecific)+ len(con.topicsGeneral)))
    #Points in multiple Circles
    center = (round(50+random.uniform(0,100)), round(60+random.uniform(0,100)))
    centerPoints = pointsInCircle(center, 700,len(con.futureDefinitions))
    multipleCirclePoints = []
    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
        topicsSpecific = con.futureTopics[futureName]
        topicsGeneral = gq.dictionaryJoin([con.marketTopics, con.supplyAndDemand])
        centerPoint = centerPoints.pop()
        topicGraph.add_node(futureName, pos=centerPoint, cc='green', label=futureName)
        multipleCirclePoints = pointsInCircle(centerPoint, 200, len(topicsSpecific)+ len(topicsGeneral))+multipleCirclePoints
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
#   edges
    allGoogle = dm.readAllCountFraction(isTest, 'google')
    allGoogleW = dm.readAllCount(isTest, 'google', 'w')
    allGoogleD = dm.readAllCount(isTest, 'google', 'd')
    print "Read %d Results"%(len(allGoogle))
    threashold = 1.1/5.0 #higher than twice the average
    for queryName, printName in comTopTopQueryName:
        (futureName, topicName0, topicName1) = tuple(printName.split("_"))
        if printName in allGoogle and allGoogleW[printName] > 10 and allGoogleD[printName] > 10:
            googleCountRatio = allGoogle[printName]
            #print "%-25s %2.3f"%(printName, googleCountRatio)
            if googleCountRatio > threashold:
                edgeWeight = round((googleCountRatio-threashold)*20)
                topicGraph.add_edge(futureName +'_'+ topicName0, futureName +'_'+ topicName1, color='blue', weight=edgeWeight)
    for queryName, printName in comTopcomQueryName:
        (futureName0, topicName, futureName1) = tuple(printName.split("_"))
        if printName in allGoogle and allGoogleW[printName] > 10 and allGoogleD[printName] > 10:
            googleCountRatio = allGoogle[printName]
            #print "%-25s %2.3f"%(printName, googleCountRatio)
            if googleCountRatio > threashold:
                edgeWeight = round((googleCountRatio-threashold)*20)
                topicGraph.add_edge(futureName0 +'_'+ topicName, futureName1 +'_'+ topicName, color='red', weight=edgeWeight)
    displayGraph(topicGraph, timeNowString)

def displayGraph(topicGraph, timeNowString):
    pos=  nx.get_node_attributes(topicGraph,'pos')
    #extract colors and widths
    edges = topicGraph.edges()
    nodes = topicGraph.nodes()##print nodes
    #nodeColors = [graph[u]['color'] for u in nodes]
    edgeColors = [topicGraph[u][v]['color'] for u,v in edges]
    ##print colors
    edgeWeights = [topicGraph[u][v]['weight'] for u,v in edges]
    colorAttributes = nx.get_node_attributes(topicGraph,'cc')
    nodeColors = [colorAttributes[u] for u in nodes]
    nx.draw(topicGraph, pos, edges=edges, edge_color=edgeColors, width=edgeWeights, node_size=200, alpha=0.3, node_color=nodeColors)
    nodeLabels = nx.get_node_attributes(topicGraph,'label')
    nx.draw_networkx_labels(topicGraph, pos, nodeLabels, font_size=10)
    
    plt.savefig('AAgraph_'+timeNowString+'.png')
    plt.show(block=False)   

generateGraph(False, "tt")

#generateGraph(True, 'test graph')

##G = nx.Graph()
##G.add_edge(1,2,color='r',weight=2)
##G.add_edge(2,3,color='b',weight=4)
##G.add_edge(3,4,color='g',weight=6)
##
##pos = nx.circular_layout(G)
##
##edges = G.edges()
##colors = [G[u][v]['color'] for u,v in edges]
##weights = [G[u][v]['weight'] for u,v in edges]
##
##nx.draw(G, pos, edges=edges, edge_color=colors, width=weights)
##plt.show()

    
#drawGraph(topicGraph, pos)       

##g = nx.random_graphs.erdos_renyi_graph(10,0.5)
##colors = [(random(), random(), random()) for _i in range(10)]
##nx.draw_circular(g, node_color=colors)
##plt.show()
