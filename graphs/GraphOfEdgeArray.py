import numpy as np
from BasicGraph import *
from GraphPropertiesToolBox import *
from GraphNodePairVal import *

class GraphOfEdgeArray(BasicGraph):
    def __init__(self, nodeNames, edges, directed, size):
        self.nodeNames = nodeNames
        self.edges = edges
        self.directed = directed
        self.size = size

    def GraphOfEdgeArray(self, e, direct, numNode):
        self.edges = e
        self.directed = direct
        self.size = numNode

    def GraphOfEdgeArray(self, e, direct, numNode, nodeName):
        self.nodeNames = nodeName
        self.edges = e
        self.directed = direct
        self.size = numNode

    def getDegreeSeq(self):
        return getInOutDegreeFromEdges(self.size, self.edges)

    def getDegreeFreq(self):
        return getJoinInOutFreqFromInOutDegree(getInOutDegreeFromEdges(self.size, self.edges))

    def getMotifFreq(self, motifSize):
        gnpv = GraphNodePairVal(self.size, self.directed, self.edges)
        return gnpv.getMotifFreq(motifSize)

    def getNodeMotifFreq(self, motifSize):
        res = np.matrix([], [])
        gnpv = GraphNodePairVal(self.size, self.directed, self.edges)
        return gnpv.getNodeMotifFreq(motifSize)

    def removeNullNodes(self):
        hm = {}
        newEdges = np.matrix([len(self.edges)], [2])
        for i in range(len(self.edges)):
            for j in range(2):
                if self.edges[i][j] not in hm:
                    newEdges[i][j] = np.size(hm)
                    hm.put(self.edges[i][j], newEdges[i][j])
                else:
                    newEdges[i][j] = hm.get(self.edges[i][j])

        return GraphOfEdgeArray(newEdges, self.directed, np.size(hm))

