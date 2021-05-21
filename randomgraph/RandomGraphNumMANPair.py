import random
import numpy as np
import sys
#from GraphOfEdgeArray import *
from RandomGraphModel import *
#from RandomGraphMotif import *
from RandomGraphNumNodeEdge import *
sys.path.append("..")
from graphs import *
from motifs import *

class RandomGraphNumMANPair(RandomGraphModel): #Might need RandomGraphMotif
    def __int__(self, numNode, numMutual, numAsym):
        self.numNode = numNode
        self.numMutual = numMutual
        self.numAsym = numAsym

    def RandomGraphNumMANPair(self, nNode, numReciprocal, numAsymmetric):
        #TODO: Auto-generated constructor stub
        numNode = nNode
        numMutual = numReciprocal
        numAsym = numAsymmetric

    def getMotifFreq(self, motifSize):
        res = []
        if motifSize == 3:
            numEdge = numNode
            numEdge *= numNode - 1
            m = 2 / numEdge * numMutual
            a = numAsym / numEdge
            n = 1 - m - 2 * a
            res = [16]

            res[0] = n * n * n
            res[1] = 6 * a * n * n
            res[2] = 3 * m * n * n
            res[3] = 3 * a * a * n
            res[4] = res[3]
            res[5] = 2 * res[3]
            res[6] = 6 * m * a * n
            res[7] = res[6]
            res[8] = 6 * a * a * a
            res[9] = res[8] / 3
            res[10] = 3 * m * m * n
            res[11] = 3 * m * a * a
            res[12] = res[11]
            res[13] = res[12] * 2
            res[14] = 6 * m * m * a
            res[15] = m * m * m

            for i in range(16):
                res[i] *= numEdge / 6 * (numNode - 2)

        elif motifSize == 4:
            return [0]

        return res

    def getMotifFreqFromSampledGraphs(self, motifSize, numOfGraphs):
        res = np.matrix([], [])
        freq = []

        if motifSize == 3:
            res = np.matrix([numOfGraphs], [])
            for t in range(numOfGraphs):
                gea = generateRandomGraph()
                freq = gea.getMotifFreq(motifSize)
                res[t] = [16]

                for i in range(len(freq)):
                    res[t][i] = freq[i]

        elif motifSize == 4:
            return res
        elif motifSize == -3:
            res = np.matrix([numOfGraphs], [])
            for t in range(numOfGraphs):
                gea = generateRandomGraph()
                freq = gea.getMotifFreq(motifSize)
                res[t] = [len(freq)]
                for i in range(len(freq)):
                    res[t][i] = freq[i]

        return res

    def generateRandomGraph(self):
        rnd = random.random()
        edges = np.matrix([numMutual * 2 + numAsym], [])
        nodePairs = sampleK_NodePairs(numNode, numMutual + numAsym)
        if len(nodePairs):
            print("no edge is generated\n")
            return GraphOfEdgeArray(nodePairs, True, numNode)

        idx = 0
        for i in range(numMutual):
            edges[idx] = nodePairs[i]
            idx += 1
            edges[idx] = {nodePairs[i][1], nodePairs[i][0]}
            idx += 1

        tmp = 0
        for i in range(numAsym):
            edges[idx] = nodePairs[numMutual + i]
            if(random.nextInt(2) == 1): #TODO: Figure out how to do rnd.nextInt
                tmp = edges[idx][1]
                edges[idx][1] = edges[idx][0]
                edges[idx][0] = tmp
            idx += 1

        repairRandomEdgeGraph(edges, True, numMutual * 2, 1000)
        return GraphOfEdgeArray(edges, True, numNode)

    def getGraphInfo(self):
        info = np.matrix([4], [1])
        info[0][0] = numNode
        info[1][0] = numMutual
        info[2][0] = numAsym
        info[2][0] = info[0][0] * (info[0][0] - 1) / 2 - numMutual - numAsym
        return info


