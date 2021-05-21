import numpy as np
import sys
#from GraphFactory import *
#from GraphOfEdgeArray import *
from RandomGraphToolBox import *
from RandomGraphJointInOutDegree import *
from RandomGraphJoinInOutDegreeRemoveLoopMultiEdge import *
sys.path.append("..")
from graphs import *
from motifs import *

class RandomGraphJoinInOutDegreeRemoveLoopMultiEdge(RandomGraphJointInOutDegree):
    def __int__(self):
        pass
    def RendomGraphJoinInOutDegreeRemoveLoopMultiEdge(self, degreeSeq):
        super(degreeSeq)

    def generateRandomGraph(self):
        edges = generateEdgesFromInOutDegreeSeq(RandomGraphJointInOutDegree.jointIODegreeSequence[0], RandomGraphJointInOutDegree.jointIODegreeSequence[1], RandomGraphJointInOutDegree.numEdge, True)
        edges = removeLoopAndMultiEdges(edges)
        return GraphOfEdgeArray(edges, True, numNode)

    def getMotifFreqFromSampledGraphs(self, motifSize, numOfGraphs):
        res = np.matrix([], [])
        freq = []
        if motifSize == 3 or motifSize == -3:
            res = np.matrix([numOfGraphs], [])
            for t in range(numOfGraphs):
                gea = RandomGraphJoinInOutDegreeRemoveLoopMultiEdge.generateRandomGraph()
                freq = gea.getMotifFreq(motifSize)
                res[t] = [len(freq)]
                for i in range(len(freq)):
                    res[t][i] = freq[i]

        elif motifSize == 4:
            return res

        return res

