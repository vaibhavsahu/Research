#import generateAllQueries as gq
import constants as con
import numpy as np
import graphRelations as gr
from PSI import phiGraph
import matplotlib.pyplot as plt
import os
import csv
import constants



def adjacencyMatric(nodes, edges, edgesWeigthsDict, threashold = 0.5):
    #takes a list of querie names and their score
    #returns connectivity matrix
    # name counts {name, count} name = stockMarket_change3-_eBola goes to edge change3- <-> eBola
    # or stockMarket_change3 goes to stockMarket  <-> change3
    # counts are normalized to between 0 and 1

    #first build the directory
    # weights = {}
    # nodes = set()
    # for name, count in nameCounts.iteritems():
    #     sumWeights =+ count
    #     queryTerms = tuple(name.split("_"))
    #     if len(queryTerms) == 2:
    #         (futureName, topicName) = queryTerms
    #         weights[(futureName, topicName)] = count
    #         weights[(topicName, futureName)] = count
    #         nodes.add(topicName)
    #         nodes.add(futureName)
    #     elif len(queryTerms) == 3:
    #         (futureName, topicName1, topicName2) = queryTerms
    #         weights[(topicName1, topicName2)] = count
    #         weights[(topicName2, topicName1)] = count
    #         nodes.add(topicName1)
    #         nodes.add(topicName2)
    #nodes must be a list so we guarentee ordering
    #print nodes
    #print weights
    nodeList = sorted(list(nodes))
    # make boolean connectivity graph based on threashold
    connectMatrix = np.zeros((len(nodeList), len(nodeList)))
    for n1, i in zip(nodeList, range(len(nodeList))):
        for n2, j in zip(nodeList, range(len(nodeList))):
            # if edges.get((n1,n2)):
            #     thisWeight = edges[(n1,n2)]
            #     if (thisWeight > threashold):
            #         connectMatrix[i,j] = 1
            if (n1, n2) in edgesWeigthsDict:
                weight = edgesWeigthsDict[(n1, n2)]
                if weight >= 1.0:
                    #print (n1, n2)
                    connectMatrix[i, j] = 1
    return nodeList, connectMatrix

# testNameCounts =    {'f1_t1':  0.8,
#                     'f1_t2': 0.8,
#                     'f1_t3': 0.8,
#                     'f1_t1_t2' : 0.8
#                     }
#
# testGraphNamesB= ['0_1', '0_2', '0_3',
#                   '1_2', '1_3', '1_4', '1_5', '1_9',
#                   '2_3', '2_4', '2_9',
#                   '3_4', '3_9',
#                   '5_6', '5_7', '5_8', '5_9',
#                   '6_7', '6_8', '6_9',
#                   '7_8', '7_9',
#                   '8_9'
#                   ]
# testGraphB = {}
# for name in testGraphNamesB:
#     testGraphB[name] = 0.8
#
# testGraphNamesA =['0_1','0_2','0_3','0_4',
#                   '1_2','1_3','1_4',
#                   '2_3','2_4',
#                   '3_4',
#                   '5_6','5_7','5_8','5_9',
#                   '6_7','6_8','6_9',
#                   '7_8','7_9',
#                   '8_9']
#
# testGraphA = {}
# for name in testGraphNamesA:
#     testGraphA[name] = 0.8

# testNameCountsC = gr.queryToGrpahHelperPrintNameCounts()
# testGraphNamesC = gr.queryToGrpahHelperAdjacencyList()

# testGraphC = {}
#
# for name in testGraphNamesC:
#     testGraphC[name] = testNameCounts[name]

# print 'printing testGraph C'
# print testGraphC

#list of paths
#pass timenowString as arg in place of 'test graph'
nodes_google, edges_google, edgesWeigthsDict_google = gr.generateGraph(False, 'google','test graph') #False
# # print nodes_google
# # print edges_google
nodes_twitter, edges_twitter, edgesWeigthsDict_twitter = gr.generateGraph(False, 'twitter','test graph') #False
# print nodes_twitter
# print edges_twitter


#
nodes_google, adjacency_google = adjacencyMatric(nodes_google, edges_google, edgesWeigthsDict_google)
# np.savetxt('test1.txt', adjacency_google, fmt="%.0f")
nodes_twitter, adjacency_twitter = adjacencyMatric(nodes_twitter, edges_twitter, edgesWeigthsDict_twitter)
# np.savetxt('test2.txt', adjacency_twitter, fmt="%.0f")
# #
#
#
fig, ax = plt.subplots()
im = ax.imshow(adjacency_google, cmap='hot')
ax.set_xticks(np.arange(len(nodes_google)))
ax.set_yticks(np.arange(len(nodes_google)))

ax.set_xticklabels(nodes_google, fontsize=7)
ax.set_yticklabels(nodes_google, fontsize=7)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
os.chdir('E:\\Research\\data\\google')
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-3]
newest = newest[7:-4]
newest = newest.replace("@", "_")
ax.set_title("heatmap_google" + newest)
fileName = constants.ROOTdata + 'graphs' + '\\' + 'heatmap' +'\\'+'google'+newest+'01.png'
if not os.path.exists(os.path.dirname(fileName)):
   os.makedirs(os.path.dirname(fileName))
plt.savefig(fileName, dpi=200, bbox_inches='tight')

fig.tight_layout()
plt.show()
#
#
fig, ax = plt.subplots()
im = ax.imshow(adjacency_twitter, cmap='hot')
ax.set_xticks(np.arange(len(nodes_twitter)))
ax.set_yticks(np.arange(len(nodes_twitter)))

ax.set_xticklabels(nodes_twitter, fontsize=7)
ax.set_yticklabels(nodes_twitter, fontsize=7)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
os.chdir('E:\\Research\\data\\google')
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-3]
newest = newest[7:-4]
newest = newest.replace("@", "_")
ax.set_title("heatmap_twitter" + newest)
fileName = constants.ROOTdata + 'graphs' + '\\' + 'heatmap' +'\\'+'twitter'+newest+'01.png'
if not os.path.exists(os.path.dirname(fileName)):
   os.makedirs(os.path.dirname(fileName))
plt.savefig(fileName, dpi=200, bbox_inches='tight')
fig.tight_layout()
plt.show()

psiGoogle =  phiGraph(adjacency_google, len(nodes_google))
psiTwitter = phiGraph(adjacency_twitter, len(nodes_twitter))
# #
#

# #
# diag = np.identity(len(nodes_google), dtype=float)
# adjacency_google = np.append(adjacency_google, diag, axis=1)
# adjacency_twitter = np.append(diag, adjacency_twitter, axis=1)
# final_adjacency = np.append(adjacency_google, adjacency_twitter, axis=0)
# #
# psiAll =  phiGraph(final_adjacency, final_adjacency.shape[0])
#
# psiValuesFile = constants.ROOTdata + "price" + "\\" + "psi" + ".txt"
# if not os.path.exists(os.path.dirname(psiValuesFile)):
#     os.makedirs(os.path.dirname(psiValuesFile))
# with open(psiValuesFile, 'w') as stream:
#    writer = csv.writer(stream, delimiter = '\t')
#    writer.writerow((psiGoogle, psiTwitter, psiAll))
#
# #write summary file here
# #extract timestamp from google files
# os.chdir('E:\\Research\\data\\google')
# files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
# newest = files[-2]
# newest = newest[7:-4]
# newest = newest.replace("@", "_")
#
# #read psi.txt
# spx = 0
# gold = 0
# oil = 0
# priceTimestamp = ""
# with open("E:\\Research\\data\\price.txt", 'r') as stream:
#     lines = [elem for elem in stream.read().split('\n') if elem]
#     dataLine = lines[-1].replace('\r', '').split('\t')
#     spx = float(dataLine[0])
#     gold = float(dataLine[1])
#     oil = float(dataLine[2])
#     priceTimestamp = dataLine[3]
#
summaryFile = constants.ROOTdata + "summary" + ".txt"
#
if not os.path.exists(os.path.dirname(summaryFile)):
     os.makedirs(os.path.dirname(summaryFile))
with open(summaryFile, 'a') as stream:
#     #read psi.txt, and price.txt,
    writer = csv.writer(stream, delimiter = '\t')
    writer.writerow((newest, psiGoogle, psiTwitter))
#
#

