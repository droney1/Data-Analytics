import numpy as np
from TemporalNetwork import *
from GraphOfEdgeArray import *

class TemporalGraphWEdge(TemporalNetwork):
    def __init__(self, edges, numNullSnapShot):
        self.edges = edges
        self.numNullSnapshot = numNullSnapShot

    def TemporalGraphWEdgeArray(self, s, t, e):
        size = s
        time = t
        self.edges = e
        self.numNullSnapshot = 0

    def getSnapshot(self, idx):
        if idx > len(self.edges):
            print("\n The " + idx + "-th snapshot does not exits, return the first snapshot instead!\n")
            idx = 0

        g = GraphOfEdgeArray(self.edges[idx], True, size)
        return g

    def getMotifFreq(self, motifSize):
        res = np.matrix([time], [])

        if motifSize == 3:
            for t in range(time):
                if len(self.edges[t]) == 0:
                    res[t] = [None] * 16
                    res[t][0] = size
                    res[t][0] = res[t][0] * (size - 1) / 2 * (size - 2) / 3
                    continue

                g = GraphOfEdgeArray(self.edges[t], True, size)
                res[t] = g.getMotifFreq(motifSize)

        elif motifSize == 4:
            res = np.matrix([0], [199])

        return res

    def getMotifTransaction(self, numNode):
        #TODO: Auto-generated method stub
        return None

    def getAvgMotifFreq(self, motifSize):
        #TODO: Auto-generated method stub
        return None
