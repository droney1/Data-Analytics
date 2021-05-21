import numpy as np
#from Motif import *
import sys
from BasicGraph import *
from GraphPropertiesToolBox import *
sys.path.append("..")
from motifs import *

class TemporalGraphEdgeListTimeStamp(BasicGraph):
    def __init__(self, timeStampEdges):
        self.timeStampEdges = timeStampEdges

    def TemporalGraphEdgeListTimeStamp(self, edgesOfTimeStamp):
        self.timeStampEdges = edgesOfTimeStamp

    def getMotifFreq(self, motifSize):
        return None

    def getDegreeSeq(self):
        #TODO: Auto-generated method stub
        return None

    def getDegreeFreq(self):
        #TODO: Auto-generated method stub
        return None

    def trackNodePairThreeEdgeMotif(self, timeWin):
        nodepairMotifMap = {}
        idx = 0
        key, dir = 0, 0
        nodePair = None

        for edge in self.timeStampEdges:
            key = edgeToKey(edge[0], edge[1])
            nodePair = nodepairMotifMap.get(key)
            if nodePair is None:
                nodePair = [None] * 8
                nodePair[6] = - timeWin - 1
                nodePair[7] = nodePair[6]
                nodePair[5] = 1
                nodepairMotifMap.put(key, nodePair)

            dir = (1 if edge[0] < edge[1] else -1)
            idx >>= 1
            if dir*nodePair[5] < 0:
                nodePair[4] += 2
            nodePair[5] = dir
            if edge[2] - nodePair[6] < timeWin:
                idx = nodePair[4]
                nodePair[idx] += 1

            nodePair[6] = nodePair[7]
            nodePair[7] = edge[2]
            if nodePair[6] == nodePair[7]:
                nodePair[6] = -timeWin - 1

            ls = []
            idx = 0
            res = [None] * 6
            for en, nodePair in nodepairMotifMap:
                idx = 2
                key = 0
                for i in range(4):
                    res[i+2] = nodePair[i]
                    key += nodePair[i]
                if key == 0:
                    continue
                nodePair = keyToEdgeLong(en)
                key = 0
                res[0] = nodePair[0]
                res[1] = nodePair[1]
                ls.add(res)
                res = [None] * 6
            return ls

    def getNodeMotifFreq(self, motifSize):
        #TODO Auto-generated method stub
        return None