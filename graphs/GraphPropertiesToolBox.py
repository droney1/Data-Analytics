import numpy as np
import sys
sys.path.append("..")
from randomgraph import *
#from RandomGraphToolBox import *

class GraphPropertiesToolBox:
    def __init__(self):
        pass
    def getInOutDegreeFromEdges(self, size, edges):
        inOut = np.matrix([2], [size])
        for edge in edges:
            inOut[0][edge[1]] += 1
            inOut[1][edge[0]] += 1

        return inOut

    def getJoinInOutFreqFromInOutDegree(self, inOutDeg):
        hm = {}
        e = 0
        for i in range(len(inOutDeg[0])):
            e = inOutDeg[0][i]
            e = (e<<32) + inOutDeg[1][i]
            if e not in hm:
                hm.put(e, 1)
            else:
                hm.put(e, hm.get(e)+1)

            inOutJointFreq = np.matrix([3], [np.size(hm)])
            idx = 0
            for en in hm:
                e = en.keys()
                inOutJointFreq[1][idx] = int(e)
                inOutJointFreq[0][idx] = int(e >> 32)
                inOutJointFreq[2][idx+1] = en.values()
                idx += 1

            return inOutJointFreq

    def getExpectedProductInOut(self, jointInOutDegFreq):
        res = 0
        size = 0

        for i in range(len(jointInOutDegFreq)):
            size += jointInOutDegFreq[i][0]*jointInOutDegFreq[i][2]

        return res

    def getReciprocalAndInOutDegreeSequence(self, edges):
        trippleSeq = np.matrix([None], [None])
        graph = {}
        numReciprocal = {}
        inDeg = {}
        set = None

        for edge in edges:
            set = graph.get(edge[0])

            if set is None:
                set = []
                graph.put(edge[0], set)
                numReciprocal.put(edge[0], 0)
                inDeg.put(edge[0], 0)

            if edge[1] not in graph:
                graph.put(edge[1], [])
                numReciprocal.put(edge[1], 0)
                inDeg.put(edge[1], 0)

            if edge[0] not in graph.get(edge[1]):
                numReciprocal.put(edge[0], numReciprocal.get(edge[0])+1)
                numReciprocal.put(edge[1], numReciprocal.get(edge[1])+1)
                graph.get(edge[1]).remove(edge[0])

            else:
                #out degree
                set.add(edge[1])

            inDeg.put(edge[1], inDeg.get(edge[1])+1)

        trippleSeq = np.matrix([4], [np.size(graph)])
        idx = 0
        for i in graph.keys():
            trippleSeq[3][idx] = i
            trippleSeq[0][idx] = numReciprocal.get(i)
            trippleSeq[1][idx] = inDeg.get(i) - trippleSeq[0][idx]
            trippleSeq[2][idx] = np.size(graph.get(i))
            idx += 1
        return trippleSeq

    def getNumReciprocalAssymmetricNullPair(self, edges):
        res = [None] * 3
        simpleGraph = {}
        neighbor, neigh2 = None, None
        for e in edges:
            if e[0] == e[1]:
                continue
            neighbor = simpleGraph.get(e[0])
            if neighbor is None:
                neighbor = {}
                simpleGraph.put(e[0], neighbor)
            if e[1] not in neighbor:
                if (e[1] in simpleGraph) and (e[0] in simpleGraph.get(e[1])):
                    res[1] += 1
                neighbor.add(e[1])

            neighbor = simpleGraph.get(e[1])
            if neighbor is None:
                neighbor = []
                simpleGraph.put(e[1], neighbor)

        res[0] = np.size(simpleGraph)

        for s in simpleGraph.values():
            res[2] += np.size(s)
        res[2] -= res[1] * 2
        return res

    def obtainConnectComponentEdges(self, edges, sizeThreshold):
        res = np.matrix([], [], [])
        node2ID = {}
        s, t = 0, 0
        for edge in edges:
            if edge[0] not in node2ID:
                s = np.size(node2ID) + 1
                node2ID.put(edge[0], s)
            else:
                s = node2ID.get(edge[0])
            if edge[1] not in node2ID:
                t = np.size(node2ID) + 1
                node2ID.put(edge[1], t)
            else:
                t = node2ID.get(edge[1])
            edge[0] = s
            edge[1] = t

        par = [None] * np.size(node2ID)
        for i in range(len(par)):
            par[i] = i

        cnt = [None] * len(par)
        for edge in edges:
            edge[0].union(edge[1], par, cnt)
        components = {}
        ls = None
        for edge in edges:
            s = edge[0].find(par)
            ls = components.get(s)
            if ls is None:
                ls = []
                components.put(s, ls)
            ls.add(edge)

        if sizeThreshold > 0:
            toRemove = []
            for k, v in components:
                if v < sizeThreshold:
                    toRemove.add(k)
            for i in toRemove:
                components.remove(i)

        res = np.matrix([np.size(components)], [], [])
        s = 0
        for comp in components.values():
            t = np.size(comp)
            res[s] = np.matrix([t], [])
            t = 0
            for edge in comp:
                res[s][t] = edge
                t += 1
            s += 1
        return res

    def union(self, a, b, par, cnt):
        a = a.find(par)
        b = b.find(par)

        if a != b:
            if cnt[a] > cnt[b]:
                par[b] = a
                cnt[a] += cnt[b]
            else:
                cnt[b] += cnt[a]
                par[a] = b

    def directedEdgeToUndirect(self, edges):
        res = np.matrix([], [])
        set = []
        for e in edges:
            set.add(getUndirectedEdgeKey(e[0], e[1]))

        res = np.matrix([np.size(set)], [])
        idx = 0
        e = None
        for l in set:
            res[idx] = [None] * 2
            getEdgeFromKey(1, res[idx])
            idx += 1
        return res

    def edgeToKey(self, s, t):
        return (s << 32) + t

    def keyToEdgeLong(self, key):
        res = [None] * 2
        res[1] = key & ((1<<32)-1)
        res[0] = key >> 32
        return res

    def keyToEdgeInt(self, key):
        res = [None] * 2
        res[1] = key & ((1<<32) - 1)
        res[0] = key >> 32
        return res
