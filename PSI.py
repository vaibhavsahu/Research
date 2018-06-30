import constants as con
import numpy as np
import math
import matplotlib.pyplot as plt

cutOff = 0.5

def phiGraph(adjacency, n):
    # takes a dictiony of (queryName, score)
    # computes a adjacency matrix based on a threashold
    # computes PSI and returns it
    #cutOff = 0.5


##        // takes a graph represented as an integer connectivity matrix (symetric) with graph[i,j] == 1 means an edge, == 0 no edge
##        // and returns a double that represents the complexity of the graph (higher the most information contained in the graph)
##        // assumes that the graph has no self connections
    #fill in c_i by looking at connectivity between each i and all the other nodes
    c_i = np.zeros((n,2)) # the count of connections to a single node. the second index is not to i ,0] or connections to i ,1]

    for connect in range(2):
        for i in range(n):
            for j in range(n):
                if i != j and adjacency[i, j] == connect:
                    c_i[i, connect]+=1 #increment
    ## scale to turn in to probabilities
    p_i = (1/(float(n-1)))*np.array(c_i)
    ##fill in c_ij by looking at connectivity between i and j through all other nodes
    c_ij = np.zeros((n, n, 2, 2)) #count of connections between two nodes through another node, last two indexes similar to above
    for connect_i in range(2):
        for connect_j in range(2):
            for i in range(n):
                for j in range(n):
                    for m in range(n): # middle node
                        # (i != j && i != m && j != m && graph[i, m] == connect_i && graph[m, j] == connect_j)
                        if i != j and i != m and j != m and adjacency[i,m] == connect_i and adjacency[m,j] == connect_j:
                            c_ij[i, j, connect_i, connect_j]+=1 #increment
    ## scale to turn into probabilities
    #p_ij[i, j, connect_i, connect_j] = c_ij[i, j, connect_i, connect_j] / (double)(n - 2)
    p_ij = np.zeros((n, n, 2, 2)) #as above but probabilities
    p_ij = (1.0/float(n-1))* np.array(c_ij)
    ##  compute the shannon entropy
    k = np.zeros(n)
    for connect in range(2):
        for i in range(n):
            if p_i[i, connect] != 0:
                k[i]+=-1 * p_i[i, connect] * math.log(p_i[i, connect], 2)
    ## compute the marginalized pi and pj (sum probabilities over other variable)
    p_ijMa = np.zeros((n, n, 2))
    p_ijMb = np.zeros((n, n, 2))
    for i in range(n):
        for j in range(n):
            if not i == j:
                # sum over b (second index) for Ma
                p_ijMa[i, j, 0] += p_ij[i, j, 0, 0] + p_ij[i, j, 0, 1];
                p_ijMa[i, j, 1] += p_ij[i, j, 1, 0] + p_ij[i, j, 1, 1];
                # sum over a (first index) for Mb
                p_ijMb[i, j, 0] += p_ij[i, j, 0, 0] + p_ij[i, j, 1, 0];
                p_ijMb[i, j, 1] += p_ij[i, j, 0, 1] + p_ij[i, j, 1, 1];
    ## compute the mutual information m[]
    mI = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            for connect_i in range(2):
                for connect_j in range(2):
                    if p_ij[i, j, connect_i, connect_j] != 0.0 and p_i[i, connect_i] != 0.0 and  p_i[j, connect_j] != 0.0:
                        edgeInfo = math.log(p_ij[i, j, connect_i, connect_j] / (p_ijMa[i, j, connect_i] * p_ijMb[i, j, connect_j]), 2)
                        mI[i, j] += p_ij[i, j, connect_i, connect_j] * edgeInfo
    ## compute psi
    psi = 0.0
    total = 0.0;
    for i in range(n):
        for j in range(n):
            if i != j:
                total += max(k[i], k[j]) * mI[i, j] * (1 - mI[i, j])
    psi = 4*total/(n* (n-1))
    print psi
    return psi





