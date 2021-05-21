import numpy as np
import math
import sys
'''
from GraphOfEdgeArray import *
from MathFun import *
'''
from RandomGraphModel import *
sys.path.append("..")
from graphs import *
from mathFunctions import *

class RandomGraphNumNodeEdge(RandomGraphModel): #Might need RandomGraphMotif
    def __init__(self, numNode, numEdge):
        self.coordinator = [1, 6, 3, 3, 3, 6, 6, 6, 6, 2, 3, 3, 3, 6, 6, 1]
        self.multiplyP = [False, True, True, False, False, False, True, False, False,False, True, False, False, False, True, True]
        self.numNode = numNode
        self.numEdge = numEdge

    def RandomGraphNumNodeEdge(self, nnode, nedge):
        self.numNode = nnode
        self.numEdge = nedge

    def getMotifFreq(self, motifSize):
        res = []
        if motifSize == 3:
            res = [16]
            if self.numNode < 3:
                return res
            N = self.numNode
            N = N * (N - 1)
            p = self.numEdge / N
            q = 1 - p
            res[0] = math.pow(q, 6)

            for i in range(1, 16):
                if self.multiplyP[i]:
                    res[i] = res[i - 1] / q * p
                else:
                    res[i] = res[i - 1]
                for i in range(16):
                    res[i] *= self.coordinator[i] * N / 6 * (self.numNode - 2)
        else:
            res = [0]
        return res

    def getMotifFreqFromSampledGraphs(self, motifSize, numOfGraphs):
        res = np.matrix([], [])
        freq = []

        if motifSize == 3 or motifSize == -3:
            res = np.matrix([numOfGraphs], [])

            for t in range(numOfGraphs):
                gea = generateRandomGraph()
                freq = gea.getMotifFreq(motifSize)
                res[t] = [len(freq)]

                for i in range(len(freq)):
                    res[t][i] = freq[i]

        elif motifSize == 4:
            return res
        return res

    def generateRandomGraph(self):
        mapping = MathFun.resorviorSampling(self.numNode * (self.numNode - 1), self.numEdge)
        edges = np.matrix([self.numEdge], [2])
        r, c, n = 0, 0, self.numNode - 1

        for i in range(self.numEdge):
            r = mapping[i] / n
            c = mapping[i] % n
            if c >= r:
                c += 1
            edges[i][0] = r
            edges[i][1] = c

        return GraphOfEdgeArray(edges, True, self.numNode)

    def getGraphInfo(self):
        res = [[self.numNode], [self.numEdge]]
        return res
