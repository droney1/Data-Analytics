import numpy as np
from TriadStructProbability import *

def computeProbForStruct(deg, numEdge, t):
    res = 0
    for i in range(3):
        for j in range(2):
            if deg[i][j] < triadInOutDeg[t][i][j]:
                return 0

    res = 1.0
    #node u
    probNull = 1
    u, v = 0, 0
    for u in range(3):
        for i in range(2):
            v = DyadNode2Node[u][i]
            #compute probNull
            probNull = 1
            if deg[u][1] > deg[v][0]:
                for j in range(deg[v][0]):
                    probNull *= 1 - deg[u][1] / (numEdge - deg[v][0] - j)

            else:
                for j in range(deg[u][1]):
                    probNull *= 1 - deg[v][0] / (numEdge - deg[u][0] - j)

            if DyadEdgeIndicator[t][u][i]:
                res *= (1 - probNull)
                deg[u][1] -= 1
                deg[v][0] -= 1
                numEdge -= 1

            else:
                res *= probNull

            if res == 0:
                return 0

    return res
