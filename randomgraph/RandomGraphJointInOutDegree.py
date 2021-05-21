import numpy as np
import sys
from RandomGraphModel import *
from RandomGraphToolBox import *
sys.path.append("..")
from motifs import *
from graphs import *
'''
from MotifAlg import *
from RandomGraphMotif import *
from GraphPropertiesToolBox import *
from GraphOfEdgeArray import *
from GraphFactory import *
'''

class RandomGraphJointInOutDegree(RandomGraphModel): #Might need RandomGraphMotif
    def __int__(self, jointIODegreeSequence, degFreq, numEdge, numNode):
        self.jointIODegreeSequence = jointIODegreeSequence
        self.degFreq = degFreq
        self.numEdge = numEdge
        self.numNode = numNode

    def RandomGraphJointInOutDegree(self, degreeSeq):
        self.numEdge = 0
        tmp = 0

        for i in range(len(degreeSeq[0])):
            self.numEdge += degreeSeq[0][i]
            tmp += degreeSeq[1][i]

        if self.numEdge != tmp:
            print("\n In/Out Degree not matched during random graph construction. Null Graph Created Instead")
            self.numEdge = 0
            self.jointIODegreeSequence = np.matrix([0], [2])
            self.numNode = 0

        self.jointIODegreeSequence = degreeSeq
        self.numNode = len(degreeSeq[0])
        self.degFreq = getJointInOutFreqFromInOutDegree(self.jointIODegreeSequence)
        print("RandomGraph Created:\n\tnum nodes: ", self.numNode, "\n\t num Edge: ", self.numEdge, "\n\t")
        getExpectedConnectProbWJointInOutDegSeq(self.jointIODegreeSequence[0], self.jointIODegreeSequence[1])

    def getNumNode(self):
        return self.numNode

    def getNumEdge(self):
        return self.numEdge

    def getGraphInfo(self):
        res = np.matrix([1], [])
        res[0] = getExpectationOfProperties(self.degFreq[0], self.degFreq[1], self.degFreq[2])

        return res

    def generateRandomGraph(self):
        edges = generateEdgesFromInOutDegreeSeq(self.jointIODegreeSequence[0], self.jointIODegreeSequence[1], self.numEdge, False)
        return GraphOfEdgeArray(edges, True, self.numNode)

    def getMotifFreq(self, motifSize):
        if motifSize == 3:
            return getTriadFreqFromConfigurationModel(self.degFreq[0], self.degFreq[1], self.degFreq[2], 0)
        elif motifSize == 4:
            return [0]
        else:
            return [0]
    def getMotifFreq(self, motifSize, opt):
        if motifSize == 3:
            return getTriadFreqFromConfigurationModel(self.degFreq[0], self.degFreq[1], self.degFreq[2], self.numNode, opt)
        elif motifSize == 4:
            return [0]
        else:
            return [0]

    def getMotifFreqFromSampledGraphs(self, motifSize, numOfGraphs):
        res = np.matrix([], [])
        freq = []
        edges = np.matrix([], [])

        if motifSize == 3 or motifSize == 3:
            res = np.matrix([numOfGraphs], [])
            for t in range(numOfGraphs):
                edges = generateEdgesFromInOutDegreeSeq(self.jointIODegreeSequence[0], self.jointIODegreeSequence[1], self.numEdge, False)
                edges = removeLoopAndMultiEdges(edges)
                gea = GraphOfEdgeArray(edges, True, self.numNode)
                freq = gea.getMotifFreq(motifSize)
                res[t] = [len(freq)]

                for i in range(len(freq)):
                    res[t][i] = freq[i]

        elif motifSize == 4:
            return res

        return res


