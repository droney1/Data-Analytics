import numpy as np
import sys
#from MotifGraph import *
from BasicGraph import *
sys.path.append("..")
from motifs import *

class GraphNodePairVal(BasicGraph):
    def __init__(self):
        self.nodes = {}
        self.tmpArray = []
        self.triadIODegIdx = np.matrix([0, 0, 1], [1, 2, 2])
        self.triadIODeg = [3]
        self.triadStructure = [3]

    def GraphNodePairVal(self, s, dir, edges):
        size = s
        directed = dir
        self.nodes = {}
        neig = []

        for edge in edges:
            if edges[0] in self.nodes:
                neig = self.nodes.get(edge[0])
            else:
                neig = {}
                self.nodes.put(edge[0], neig)

            if edge[1] in neig:
                neig.put(edge[1], 3)
            else:
                neig.put(edge[1], 1)

            if edge[1] in self.nodes:
                neig = self.nodes.get(edge[1])
            else:
                neig = {}
                self.nodes.put(edge[1], neig)

            if edge[0] in neig:
                neig.put(edge[0], 3)
            else:
                neig.put(edge[0], 2)

    def getMotifFreq(self, motifSize):
        if self.tmpArray is None or len(self.tmpArray) != motifSize:
            self.tmpArray = []
        if directed: #TODO: Determine how to send directed
            if motifSize == 3:
                return getTriadFreq()
            elif motifSize == 4:
                return getFourNodeMotifFreq(self.tmpArray)
            elif motifSize == -3:
                    return getRogerNodeMotifSeq()

        return None

    def getPairVal(self, u, v):
        if (u not in self.nodes) or (v not in self.nodes.get(u)):
            return 0
        else:
            return self.nodes.get(u).get(v)

    def getTriadFreq(self):
        res = []
        neig = {}
        edgeVal = -2
        motifType = -1
        node, u, v, nu, reCnt = -1, -1, -1, -1, 0
        isTriangle = False
        for node, neig in self.nodes.iteritems:
            for u, nu in neig.iteritems:
                reCnt = 0
                for v in neig:
                    if u == v:
                        continue
                    isTriangle = self.nodes.get(u).containsKey(v)    #TODO: Determine how to write this line in python

                    if isTriangle:
                        reCnt += 1
                    if u < v or (isTriangle > v and node > v):
                        continue
                    else:
                        self.triadIODeg = np.zeros()

                        if (nu and 1) > 0:
                            self.triadIODeg[0] += 1
                            self.triadIODeg[1] += 4

                        if (nu and 2) > 0:
                            self.triadIODeg[0] += 4
                            self.triadIODeg[1] += 1

                        edgeVal = nu

                        if (edgeVal and 1) > 0:
                            self.triadIODeg[0] += 1
                            self.triadIODeg[2] += 4
                        if (edgeVal and 2) > 0:
                            self.triadIODeg[0] += 4
                            self.triadIODeg[2] += 1

                        if isTriangle:
                            edgeVal = self.nodes.get(v).get(u)

                            if (edgeVal and 1) > 0:
                                self.triadIODeg[2] += 1
                                self.triadIODeg[1] += 4
                            if (edgeVal and 2) > 0:
                                self.triadIODeg[2] += 4
                                self.triadIODeg[1] += 1

                            motifType = triadCodeIdx.get(getTriadHashKey(self.triadIODeg))
                            res[motifType] += 1

                if u > node:
                    if neig.get(u) == 3:
                        motifType = 2
                    else:
                        motifType = 1
                    res[motifType] += size - np.size(neig) - np.size(self.nodes.get(u)) + reCnt

        total = int(size)
        total = total * (total - 1)/2 * (total-2)/3
        for i in res:
            total -= i

        res[0] = total
        return res

    def getNodeMotifFreq(self, motifSize):
        if self.tmpArray is None or len(self.tmpArray) != motifSize:
            self.tmpArray = []

        if size == 0:
            res = np.matrix([1], [17])
            res[0][0] = 1
            res[0][1] = 1
            return res

        if directed:
            if motifSize == 3:
                return getNodeTriadFreq()
            elif motifSize == 4:
                return None
            elif motifSize == -3:
                return None

        return None

    def getNodeTriadFreq(self):
        nodeTriadFreqMap ={}
        nodeRoles = None
        for key in self.nodes.keys():
            nodeTriadFreqMap.put(key, [])

        res = []
        neig = None
        edgeVal, motifType = -2, -2
        node, u, v, nu, reCnt = -1, -1, -1, -1, 0
        for node, neig in self.nodes:
            reCnt = 0

            for v in neig:
                if u == v:
                    if isTriangle:
                        reCnt
                    if u < v or (isTriangle and node) > v:
                        continue
                    else:
                        self.triadIODeg = np.zeros()

                        if (nu and 1) > 0:
                            self.triadIODeg[0] += 1
                            self.triadIODeg[1] += 4
                        if (nu and 2) > 0:
                            self.triadIODeg[0] += 4
                            self.triadIODeg[1] += 1

                        edgeVal = v

                        if (edgeVal and 1) > 0:
                            self.triadIODeg[0] += 1
                            self.triadIODeg[2] += 4
                        if (edgeVal and 2) > 0:
                            self.triadIODeg[0] += 4
                            self.triadIODeg[2] += 1

                        if isTriangle:
                            edgeVal = self.nodes.get(v).get(u)
                            if (edgeVal and 1) > 0:
                                self.triadIODeg[2] += 1
                                self.triadIODeg[1] += 4
                            if (edgeVal and 2) > 0:
                                self.triadIODeg[2] += 4
                                self.triadIODeg[1] += 1

                        motifType = triadCodeIdx.get(getTriadHashKey(self.triadIODeg))
                        res[motifType] += 1
                        nodeRoles = nodeTriadFreqMap.get(node)
                        nodeRoles[motifType] += 1
                        nodeRoles = nodeTriadFreqMap.get(u)
                        nodeRoles[motifType] += 1
                        nodeRoles = nodeTriadFreqMap(v)
                        nodeRoles[motifType] += 1

                if u > node:
                    if neig.get(u) == 3:
                        motifType = 2
                    else:
                        motifType = 1
                    reCnt = size - np.size(neig) - np.size(self.nodes.get(u)) + reCnt
                    res[motifType] += reCnt
                    nodeRoles = nodeTriadFreqMap.get(node)
                    nodeRoles[motifType] += reCnt
                    nodeRoles = nodeTriadFreqMap.get(u)
                    nodeRoles[motifType] += reCnt

        total = size
        total = total*(total-1)/2 * (total-2)/3

        for i in res:
            total -= i
        res[0] = total
        finRes = np.matrix([size], [16+1])
        for i in range(16):
            finRes[0][i+1] = res[i]
        node = 0
        for key in self.nodes.keys():
            finRes[node][0] = key
            nodeRoles = nodeTriadFreqMap.get(key)
            if nodeRoles is not None:
                for i in range(16):
                    finRes[node][i+1] = nodeRoles[i]
                node += 1

        return finRes

    def RogerNodeMotifSeq(self):
        degDistr = None
        neig = {}
        degMap = {}
        node, u, v = -1, -1, -1
        isTriangle = False
        for node, neig in self.nodes:
            for u in neig.keys():
                for v in neig.keys():
                    if u == v:
                        continue

                    isTriangle = self.nodes.get(u).containsKey(v) #TODO: Determine how to write this line in Python
                    if isTriangle:
                        print()
                    if u < v or (isTriangle and node) > v:
                        continue
                    else:
                        if node in degMap:
                            degMap.put(node, degMap.get(node)+1)
                        else:
                            degMap.put(node, 1)
                        if u in degMap:
                            degMap.put(u, degMap.get(u)+1)
                        else:
                            degMap.put(u, 1)
                        if v in degMap:
                            degMap.put(v, degMap.get(v)+1)
                        else:
                            degMap.put(v, 1)
        degCount = {}
        for i in degMap.values():
            if i in degCount:
                degCount.put(i, degCount.get(i)+1)
            else:
                degCount.put(i, 1)

        tmpDeg = []
        degDistr = []
        node = 0

        for key in degCount.keys():
            tmpDeg[node+1] = key
            node += 1
        tmpDeg.sort()
        for i in range(np.size(degCount)):
            degDistr[2*i] = tmpDeg[i]
            degDistr[2*i+1] = degCount.get(tmpDeg[i])

        return degDistr

    def updateMotifFreq(self, nextGraph, curFreq):
        nextFreq = []
        neig = None
        preNeig = None
        for node in self.nodes.keys():
            neig = self.nodes.get(node)
            preNeig = nextGraph.self.nodes.get(node)

            for u in neig.keys():
                #TODO if(preNeig.containsKey(u) && preNeig.get(u))
                pass

        return nextFreq

    def getFourNodeMotifFreq(self, motifTypeArray):
        res = [None] * 199
        return res

    def setTriadStructure(self, node, u, v):
        self.triadStructure = np.zeros()
        self.triadStructure[0] = self.nodes.get(node).get(u)
        self.triadStructure[1] = self.nodes.get(self.nodes).get(v)
        if self.nodes.get(u) in self.nodes:
            self.triadStructure[2] = self.nodes.get(u).get(v)

    def setTriadIODegree(self):
        self.triadIODeg = np.zeros()
        for i in range(len(self.triadStructure)):
            if self.triadStructure[i] == 1:
                self.triadIODeg[self.triadIODegIdx[i][0]] += 1
                self.triadIODeg[self.triadIODegIdx[i][1]] += 4
            elif self.triadStructure[i] == 2:
                self.triadIODeg[self.triadIODegIdx[i][0]] += 4
                self.triadIODeg[self.triadIODegIdx[i][1]] += 1
            elif self.triadStructure[i] == 3:
                self.triadIODeg[self.triadIODegIdx[i][0]] += 5
                self.triadIODeg[self.triadIODegIdx[i][1]] += 5

    def getTriadTypeFromStructureVal(self, uv, uw, vw):
        self.triadStructure[0] = uv
        self.triadStructure[1] = uw
        self.triadStructure[2] = vw
        setTriadIODegree()
        return triadCodeIdx.get(getTriadHashKey(self.triadIODeg))
