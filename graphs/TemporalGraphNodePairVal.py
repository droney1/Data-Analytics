import numpy as np
from TemporalNetwork import *
from GraphNodePairVal import *

class TemporalGraphNodePairVal(TemporalNetwork):
    def __init__(self, graphs, edgeNum, preMissingEdges, size, time):
        self.graphs = graphs
        self.edgeNum = edgeNum
        self.preMissingEdges = preMissingEdges
        self.size = size
        self.time = time

    def TemporalGraphNodePairVal(self, edgeGraphs, dir):
        self.time = len(edgeGraphs)
        self.edgeNum = [None] * self.time

        for t in range(self.time):
            self.graphs[t] = GraphNodePairVal(self.size, dir, edgeGraphs[t])
            self.edgeNum[t] = len(edgeGraphs[t])

        calMissingEdgesInNextTimeStep()

    def calMissingEdgesInNextTimeStep(self):
        tmp = np.matrix([], [], {})
        preEdgeType = {}
        curEdgeType = {}
        hm = {}

        for t in range(self.time - 1):
            self.preMissingEdges[t+1] = GraphNodePairVal(self.size, self.graphs[t+1].directed, tmp)
            for n in self.graphs[t].nodes.keys():
                preEdgeType = self.graphs[t].nodes.get(n)
                curEdgeType = self.graphs[t+1].nodes.get(n)

                if curEdgeType is None:
                    self.preMissingEdges[t+1].nodes.put(n, preEdgeType)
                    continue

                hm = {}
                for u in preEdgeType.keys():
                    if u not in curEdgeType:
                        hm.put(u, preEdgeType.get(u))

                if not hm:
                    self.preMissingEdges[t+1].nodes.put(n, hm)

    def getMotifFreq(self, numNode):
        #TODO: Auto-generated method stub
        return None

    def getMotifTransition(self, numNode):
        #TODO: Auto-generated method stub
        return None

    def getAllMotifFreq(self, subGraphSize):
        res = np.matrix([], [])
        if subGraphSize == 3:
            res = np.matrix([self.time], [16])

        return res

    def getAllTriadFreq(self, allFreqs):
        tmp = self.graphs[0].getMotifFreq(3)
        for i in range(len(tmp)):
            allFreqs[0][i] = tmp[i]

        neig = None
        preNeig = None
        nuVal, preNUVal, nvVal, preNVVal, uvVal, preUVVal = -1, -1, -1, -1, -1, -1
        n, motifType = 0, -1
        hs = []

        for t in range(1, self.time):
            for i in range(1, 16):
                allFreqs[t][i] = allFreqs[t-1][i]

            for n, neig in self.graphs[t].nodes:
                preNeig = self.graphs[t-1].nodes.get(n)
                hs.clear()
                hs.addAll(neig.keys())

                for u in hs:
                    nuVal = self.graphs[t].getPairVal(n, u)
                    preNUVal = self.graphs[t-1].getPairVal(n, u)
                    if nuVal == preNUVal:
                        continue
                    if preNUVal == 0:
                        for v in hs:
                            uvVal = self.graphs[t].getPairVal(u, v)

                            if (u == v) or (n > u and uvVal > 0):
                                continue
                            else:
                                nvVal = self.graphs[t].getPairVal(n, v)
                                preNVVal = self.graphs[t-1].getPairVal(n, v)
                                preUVVal = self.graphs[t-1].getPairVal(u, v)
                                if (v < n and uvVal > 0) and (preNVVal != nvVal or preUVval != uvVal):
                                    continue
                                motifType = getTriadTypeFromStructureVal(nuVal, nvVal, uvVal)
                                allFreqs[t][motifType] += 1

                                if preNVVal > 0 and preUVVal > 0:
                                    motifType = motifType = getTriadTypeFromStructureVal(nuVal, nvVal, uvVal)
                                elif preNVVal == 0 and preUVVal == 0:
                                    continue
                                else:
                                    motifType = (3 if preNVVal + preUVVal == 3 else 2)
                                allFreqs[t][motifType] -= 1

                        if n < u:
                            motifType = (3 if nvVal == 3 else 2)
                            allFreqs[t][motifType] += np.size(self.graphs[t]) - np.size(hs) - np.size(self.graphs[t].nodes.get(u))
                            for v in self.graphs[t].nodes.get(u).keys():
                                if v in hs:
                                    allFreqs[t][motifType] += 1

                else:
                    nuVal = neig.get(u)
                    if nuVal == preNeig.get(u):
                        continue

                #TODO: check missing edges


    def updateTriadFreq(self, allFreqs, t):
        #TODO: fill in this function
        print()

    def getAvgMotifFreq(self, motifSize):
        #TODO: Auto-generated method stub
        return None


