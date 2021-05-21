import numpy as np
from TriadStructProbability import *

class CalculatorTriadStructProbConfigModel(TriadStructProbability):
    def __init__(self):
        pass

    def computeProbForStruct(self, deg, numEdge, t):
        res, tmp = 1, 1
        for i in range(3):
            for j in range(2):
                if deg[i][j] < triadInOutDegs[t][i][j]:
                    return 0

        for u in range(3):
            for i in range(2):
                v = DyadNode2Node[u][i]
                tmp = deg[u][1] / numEdge * deg[v][0]

                if DyadEdgeIndicator[t][u][i]:
                    if tmp < 1:
                        res *= tmp
                    deg[u][1] -= 1
                    deg[v][0] -= 1
                    numEdge -= 1

                else:
                    if tmp < 1:
                        res *= 1 - tmp
                    else:
                        return 0

                if res <= 0:
                    return 0

        return res
