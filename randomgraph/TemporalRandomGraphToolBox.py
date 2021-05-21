import numpy as np
import sys
sys.path.append("..")
from mathFunctions import *
#from MathFun import *

class TemporalRandomGraphToolBox:
    def __init__(self):
        pass

    def shuffleTripletEdgeTimeStamp(self, tripletEdges):
        durstenfeldShuffleMatrixMultiColumn(tripletEdges, {0, 1}, len(tripletEdges))

    def sortTripletEdges(edges):
        edges.sort(ArrayLongComparator({2}, false))

    def removeSelfLoopMultiEdges(self, tripletEdges):
        length = len(tripletEdges)
        curTime, edgeKey = -sys.maxint - 1, 0
        sets = []
        validIdx = []
        for i in range(length):
            if tripletEdges[i][0] == tripletEdges[i][1]:
                continue
            if curTime < tripletEdges[i][2]:
                curTime = tripletEdges[i][2]
                sets.clear()
            edgeKey = (tripletEdges[i][0] << 32) + tripletEdges[i][1]

            if edgeKey not in sets:
                validIdx.add(i)
                sets.add(edgeKey)

        if np.size(validIdx) == len(tripletEdges):
            return tripletEdges
        else:
            res = np.matrix([np.size(validIdx)], [])
            idx = 0
            for i in range(validIdx):
                res[idx] = tripletEdges[i]
                ++idx
        return res
