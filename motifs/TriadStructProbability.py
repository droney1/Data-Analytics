import numpy as np

class TriadStructProbability:
    def __init__(self, Deg):
        self.Deg = Deg
        self.triadInOutDegs = np.matrix([], [], [], {
            {{0,0}, {0,0},{0,0}},
            {{0,1}, {1,0},{0,0}},
            {{1,1}, {1,1},{0,0}},
            {{0,2}, {1,0},{1,0}},
            {{2,0}, {0,1}, {0,1}},
            {{1,1}, {0,1}, {1,0}},
            {{0,1}, {2,1},{1,1}},
            {{1,0}, {1,2},{1,1}},
            {{2,0}, {0,2}, {1,1}},
            {{1,1}, {1,1},{1,1}},
            {{1,1}, {2,2},{1,1}},
            {{0,2}, {2,1},{2,1}},
            {{2,0}, {1,2}, {1,2}},
            {{1,1}, {1,2},{2,1}},
            {{2,1}, {1,2}, {2,2}},
            {{2,2}, {2,2},{2,2}}
        })

        self.triadNodePermutation = np.matrix([], [], {
            {0},
            {0, 1, 2, 3, 4, 5},
            {0, 3, 4},
            {0, 3, 4},
            {0, 3, 4},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1},
            {0, 3, 4},
            {0, 3, 4},
            {0, 3, 4},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0}
        })

        self.triadPermutation = np.matrix([], [], {
            {0, 1, 2},
            {0, 2, 1},
            {1, 0, 2},
            {1, 2, 0},
            {2, 0, 1},
            {2, 1, 0}
        })

        self.numEdgeInTriads = [], {
            0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5 ,6
        }

        self.DyadEdgeIndicator = np.matrix([], [], [], {
            {{False, False}, {False, False}, {False, False}},
            {{True, False}, {False, False}, {False, False}},
            {{True, False}, {True, False}, {False, False}},
            {{True, True}, {False, False}, {False, False}},
            {{False, False}, {True, False}, {True, False}},
            {{False, True}, {True, False}, {False, False}},
            {{True, False}, {False, True}, {False, True}},
            {{False, False}, {True, True}, {False, True}},
            {{False, False}, {True, True}, {True, False}},
            {{True, False}, {False, True}, {True, False}},
            {{True, False}, {True, True}, {False, True}},
            {{True, True}, {False, True}, {False, True}},
            {{False, False}, {True, True}, {True, True}},
            {{False, True}, {True, True}, {False, True}},
            {{False, True}, {True, True}, {True, True}},
            {{True, True}, {True, True}, {True, True}}
        })

        self.DyadNode2Node = np.matrix([], [], {
            {1, 2}, {0, 2}, {0, 1}
        })



    def approxStructProbNoLoopNoMulti(self, deg, numEdge, type):
        res = 0
        for i in range(3):
            for j in range(2):
                if deg[i][j] < self.triadInOutDegs[type][i][j]:
                    return res
        res = 1.0
        probNull = 1
        u, v = 0, 0
        for u in range(3):
            for i in range(2):
                v = self.DyadNode2Node[u][i]
                probNull = 1

                for j in range(deg[u][1]):
                    probNull *= 1 - deg[v][0] / (numEdge - deg[u][0] - j)

                if self.DyadEdgeIndicator[type][u][i]:
                    if deg[v][0] == 0:
                        return 0
                    res *= (1 - probNull)
                    deg[u][1] -= 1
                    deg[v][0] -= 1
                    numEdge -= 1
                else:
                    res *= probNull
                if res == 0:
                    return 0

        return res

    def getApproxProbConfigModel(self, nIds, iin, out, t, num, opt):
        res = 0
        for p in self.triadNodePermutation[t]:
            for n in range(3):
                self.Deg[n][0] = iin[nIds[self.triadPermutation[p][n]]]
                self.Deg[n][1] = out[nIds[self.triadPermutation[p][n]]]
            res += opt.computeProbForStruct(self.Deg, numEdge, t)

        return res

    def approxStructProbConfigModel(self, deg, numEdge, t):
        res = 0
        for i in range(3):
            for j in range(2):
                if deg[i][j] < self.triadInOutDegs[type][i][j]:
                    return res

        v = 0
        res = 1
        for u in range(3):
            for i in range(2):
                v = self.DyadNode2Node[u][i]
                if self.DyadEdgeIndicator[t][u][i]:
                    res *= deg[u][1] / numEdge * deg[v][0]
                    deg[u][1] -= 1
                    deg[v][0] -= 1
                    numEdge -= 1
                else:
                    res *= 1 - deg[u][1] / numEdge * deg[v][0]
                if res == 0:
                    return 0

        return res

    def getApproxProbConfigModel(self, nIds, iin, out, t, numEdge):
        res = 0
        for p in self.triadNodePermutation[t]:
            for n in range(3):
                self.Deg[n][0] = iin[nIds[self.triadPermutation[p][n]]]
                self.Deg[n][1] = out[nIds[self.triadPermutation[p][n]]]
            res += TriadStructProbability.approxStructProbConfigModel(self.Deg, numEdge, t)

        return res

