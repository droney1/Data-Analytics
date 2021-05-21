import numpy as np
import math
import collections

class MotifGraph:
    def __init__(self, numNode, edges, directed):
        self.numNode = numNode
        self.edges = edges
        self.directed = directed

        self.EDGEBASE = 1 << 32
        self.TRIADNAME = {
            "003", "012","102","021D", "021U", "021C", "111D", "111U",
            "030T", "030C", "201", "120D", "120U", "120C", "210", "300"
        }

        self.triadCodeIdx = initializeTriadCode()

        self.TRIAD_EDIT_DISTANCE = np.matrix({
            {0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6},
            {1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5},
            {2, 1, 0, 2, 2, 2, 1, 1, 3, 3, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 0, 2, 1, 3, 1, 1, 3, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 2, 0, 1, 1, 3, 1, 2, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4},
            {3, 2, 1, 3, 1, 1, 0, 2, 2, 2, 1, 1, 3, 1, 2, 3},
            {3, 2, 1, 1, 3, 1, 2, 0, 2, 2, 1, 3, 1, 1, 2, 3},
            {3, 2, 3, 1, 1, 1, 2, 2, 0, 2, 3, 1, 1, 1, 2, 3},
            {3, 2, 3, 3, 2, 1, 2, 2, 2, 0, 3, 3, 3, 1, 2, 3},
            {4, 3, 2, 2, 2, 2, 1, 1, 3, 3, 0, 2, 2, 2, 1, 2},
            {4, 3, 2, 2, 2, 2, 1, 3, 1, 3, 2, 0, 2, 1, 1, 2},
            {4, 3, 2, 2, 2, 2, 3, 1, 1, 3, 2, 2, 0, 1, 1, 2},
            {4, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 2},
            {5, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 1},
            {6, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 0}
        })

        self.TRIAD_EDIT_DISTANCE_REPLACE = np.matrix({
            {0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6},
            {1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5},
            {2, 1, 0, 2, 2, 2, 1, 1, 3, 3, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 0, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 2, 0, 1, 1, 2, 1, 2, 2, 2, 2, 2, 3, 4},
            {2, 1, 2, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4},
            {3, 2, 1, 2, 1, 1, 0, 1, 2, 2, 1, 1, 2, 1, 2, 3},
            {3, 2, 1, 1, 2, 1, 1, 0, 2, 2, 1, 2, 1, 1, 2, 3},
            {3, 2, 3, 1, 1, 1, 2, 2, 0, 1, 3, 1, 1, 1, 2, 3},
            {3, 2, 3, 2, 2, 1, 2, 2, 1, 0, 3, 2, 2, 1, 2, 3},
            {4, 3, 2, 2, 2, 2, 1, 1, 3, 3, 0, 2, 2, 2, 1, 2},
            {4, 3, 2, 2, 2, 2, 1, 2, 1, 2, 2, 0, 2, 1, 1, 2},
            {4, 3, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 0, 1, 1, 2},
            {4, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 2},
            {5, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 1},
            {6, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 0}
        })



    def MotifGraph(self, num, es, dir):
        self.numNode = num
        self.edges = []
        tmp = 0
        for i in range(len(es)):
            tmp = es[i][0]
            self.edges.add((tmp<<32) + es[i][1])

        self.directed = dir

    def resetEdges(self, es):
        self.edges.clear()
        tmp = 0
        for i in range(len(es)):
            tmp = es[i][0]
            self.edges.add((tmp<<32) + es[i][1])

    def edgeHashKey(self, s, t):
        key = s
        key = (key<<32) + t
        return key

    def hashKeyToEdge(self, k, res):
        if res is None or len(res) < 2:
            res = [None] * 2
        res[0] = int(k>>32)
        res[1] = int(k%self.EDGEBASE)
        return res

    def getEdges(self):
        res = np.matrix([np.size(self.edges)], [2])
        i = 0
        for e in self.edges:
            res[i][1] = int(e%self.EDGEBASE)
            res[i+1][0] = int(e>>32)
            i += 1
        return res

    def getTriadCountFromRandomGraphWSameAsymDyads(self):
        freq = [None] * 16
        if self.numNode == 0 or np.size(self.edges) == 0:
            return freq
        q = math.log(np.size(self.edges))
        base = self.numNode*(self.numNode - 1) / 2
        l2, l3, lbase = math.log(2), math.log(3), math.log(base)
        l6 = l2 + l3
        q -= lbase
        p = math.log(1 - math.exp(q))

        freq[0] = 6 * p
        freq[1] = l6 + p + q * 5
        freq[2] = l3 + 2 * p + q * 4
        freq[3] = freq[2]
        freq[4] = freq[2]
        freq[5] = l6 + 2 * p + q * 4
        freq[6] = l6 + p * 3 + q * 3
        freq[7] = freq[6]
        freq[8] = freq[6]
        freq[9] = l2 + p * 3 + q * 3
        freq[10] = l3 + p * 4 + q * 2
        freq[11] = freq[10]
        freq[12] = freq[10]
        freq[13] = l6 + p * 4 + q * 2
        freq[14] = l6 + p * 5 + q
        freq[15] = q * 6
        lbase += math.log(self.numNode - 2) - l3

        for i in range(len(freq)):
            freq[i] = math.exp(freq[i] + lbase)

        return freq

    def getLogTraidDistrFromRandomGraphWSameDyads(self):
        dist = [None] * 16
        mutualNum = countMutualDyads()
        asymNum = np.size(self.edges) - 2 * mutualNum
        nullNum = self.numNode * (self.numNode - 1) / 2 - (mutualNum + asymNum)
        l2, l3 = math.log(2), math.log(3)
        mutualNum = math.log(mutualNum) - math.log(self.numNode) - math.log(self.numNode - 1) + l2
        asymNum = math.log(asymNum) - math.log(self.numNode) - math.log(self.numNode - 1) + l2
        nullNum = math.log(nullNum) - math.log(self.numNode) - math.log(self.numNode - 1) + l2
        dist[0] = nullNum * l3
        dist[1] = l3 + asymNum + nullNum + nullNum
        dist[2] = l3 + mutualNum + nullNum + nullNum
        dist[3] = l3 - 4 + asymNum + asymNum + nullNum
        dist[4] = dist[3]
        dist[5] = dist[3] + l2
        dist[6] = l3 + mutualNum + asymNum + nullNum
        dist[7] = dist[6]
        dist[8] = asymNum * 3 + l3 - l2 * 2
        dist[9] = dist[8] - l3
        dist[10] = l3 + mutualNum + mutualNum + nullNum
        dist[11] = l3 + mutualNum + asymNum + asymNum - l2 * 2
        dist[12] = dist[11]
        dist[13] = dist[11] + l2
        dist[14] = l3 + mutualNum + mutualNum + asymNum
        dist[15] = mutualNum * 3
        return dist

    def getTriadCountFromRadnomGraphWSameDyads(self):
        freq = getLogTriadDistrFromRandomGraphWSameDyads()
        lbase = math.log(self.numNode) + math.log(self.numNode - 1) + math.log(self.numNode - 2) - math.log(6)
        for i in range(len(freq)):
            freq[i] = math.exp(freq[i] + lbase)
        return freq

    def getTriadDistrFromRadnomGraphWSameDyads(self):
        dist = getLogTriadDistrFromRandomGraphWSameDyads()
        for i in range(len(dist)):
            dist[i] = math.exp(dist[i])
        return dist

    def countMutualDyads(self):
        res = 0
        for e in self.edges:
            if ((e<<32) + (e>>32)) in self.edges:   #Might be e>>>32
                res += 1
        return res / 2

    def getChangingEdges(self, g1, g2, edgeSet):
        if edgeSet is None:
            edgeSet = []
        else:
            edgeSet.clear()
        s1, s2 = None, None
        removed = []
        if np.size(g1.edges) > np.size(g2.edges):
            s1 = g2.edges
            s2 = g1.edges
        else:
            s1 = g1.edges
            s2 = g2.edges

        for e in s2:
            if e in s1:
                s1.remove(e)
            else:
                edgeSet.add(e)

        edgeSet.extend(s1)
        if s1 == g2.edges:
            s1.extend(removed)

        return edgeSet

    def getTriadHashKey(self, ioDegrees):
        ioDegrees.sort()
        res = ioDegrees[0]
        res = (res << 4) + ioDegrees[1]
        res = (res << 4) + ioDegrees[2]

        return res

    def edgeKeyToSubgraphArray(self, e, sgAr, s, t):
        sgAr[s] = int(e >> 32)
        sgAr[t] = int(e % self.EDGEBASE)

        return sgAr

    def subGraphToTriadHashKey(self, subGraph,  graph, iodegrees):
        e = 0
        if iodegrees is None or len(iodegrees) < 3:
            iodegrees = [None] * 3
        else:
            np.zeros(iodegrees)

        for s in range(len(subGraph) - 1):
            for t in range(len(subGraph)):
                e = edgeHashKey(subGraph[s], subGraph[t])
                if e in graph.edges:
                    iodegrees[s] += 1
                    iodegrees[t] += 4

                e = edgeHashKey(subGraph[t], subGraph[s])
                if e in graph.edges:
                    iodegrees[s] += 4
                    iodegrees[t] += 1

        return getTriadHashKey(iodegrees)

    def getSubgraphkey(self, nodes):
        hs = []
        for n in nodes:
            hs.add(n)

        return collections.unmodifiableSet(hs)

    def initializeTriadCode(self):
        triadhm = {}
        subgraph = np.matrix(
            {0, 0, 0},
            {0, 1, 4},
            {0, 5, 5},
            {2, 4, 4},
            {1, 1, 8},
            {1, 4, 5},
            {1, 5, 9},
            {4, 5, 6},
            {2, 5, 8},
            {5, 5, 5},
            {5, 5, 10},
            {2, 9, 9},
            {6, 6, 8},
            {5, 6, 9},
            {6, 9, 10},
            {10, 10, 10}
        )
        tmp = 0

        for i in range(len(subgraph)):
            tmp = 0
            subgraph[i].sort()
            for n in subgraph[i]:
                tmp = (tmp << 4) + n
            triadhm.put(tmp, i)

        if self.triadCodeIdx is None:
            self.triadCodeIdx = traidhm

        return triadhm
