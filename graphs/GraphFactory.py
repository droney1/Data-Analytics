import sys
import numpy as np
from GraphOfEdgeArray import *
from TemporalGraphWEdgeArray import *
from TemporalTripletEdgeGraph import *
from GraphPropertiesToolBox import *
sys.path.append("..")
from randomgraph import *
'''
from randomgraph import RandomGraphJointInOutDegree
from randomgraph import RandomGraphJoinInOutDegreeRemoveLoopMultiEdge
from randomgraph import RandomGraphNumNodeEdge
from RandomGraphNumMANPair import *
from TemporalTimeStampRandomGraph import *
'''

class GraphFactory:
    def __init__(self):
        pass

    def makeEdgeGraphFromFileOfEdgeList(self, file):
        graph = None

        try:
            br = open(file, "r")
            size = -1
            minID = sys.maxsize
            line = None
            edgeStr = None
            edge = None
            edgeList = []

            for line in br:
                if line.startswith("//") or line.startswith("#") or len(line) == 0:
                    continue
                edgeStr = line.split()
                if edgeStr == "size":
                    size = int(edgeStr[1])
                else:
                    edge = []
                    edge[0] = int(edgeStr[0])
                    edge[1] = int(edgeStr[1])
                    if edge[0] != edge[1]:
                        edgeList.append(edge)

            edges = np.matrix([size(edgeList)], [])
            idx = 0
            for e in edgeList:
                edges[idx+1] = e

            nameInt = resetNodeIDsInEdges(edges) #TODO: Find this function
            size = len(nameInt)

            edges = removeLoopAndMultiEdges(edges)
            graph = GraphOfEdgeArray(edges, True, size)
            br.close()

        except:
            print("Error when creating graph")
            graph = GraphOfEdgeArray(np.matrix([0][2]), True, 0)

        return graph

    def getTemporalGraphWEdgeArrayFromFile(self, file):
        g = None

        try:
            br = open(file, "r")
            line = br.readline()

            while line != None and (line.startswith("//") or line.startswith("#") or len(line) == 0):
                line = br.readline()

            data = line.split()
            size = int(data[0])
            time = int(data[1])
            t = 0
            numOfEdge = 0
            numSelfLoop = 0
            tEdges = np.matrix([time], [], [])
            edges = np.matrix([], [])
            tmpEdges = np.matrix([], [])

            while t < time and br.readline() != None:
                if line.startswith("//") or len(line) == 0:
                    continue
                data = line.split()
                numOfEdge = len(data) / 2
                numSelfLoop = 0
                edges = np.matrix([numOfEdge], [2])

                for i in range(0, numOfEdge):
                    edges[numSelfLoop][0] = int(data[2*i])
                    edges[numSelfLoop][1] = int(data[2*i + 1])
                    if edges[numSelfLoop][0] == edges[numSelfLoop][1]:
                        numSelfLoop -= 1

                    numSelfLoop += 1

                if numSelfLoop < numOfEdge:
                    tmpEdges = np.matrix([numSelfLoop], [2])
                    for i in range(len(tmpEdges)):
                        tmpEdges[i][0] = edges[i][0]
                        tmpEdges[i][1] = edges[i][1]
                else:
                    tmpEdges = edges
                tEdges[t] = tmpEdges
                t += 1

            numOfEdge = 0
            while t < time:
                tEdges[t+1] = np.matrix([0][2])
                numOfEdge += 1

            g = TemporalGraphWEdgeArray(size, time, tEdges)
            g.numNullSnapshot = numOfEdge
            br.close()
        except:
            print("Create an empty temporal network")
            g = TemporalGraphWEdgeArray(0, 0, np.matrix([0], [0], [2]))

        return g

    def getTemporalGraphWithTimeStampFromFile(self, filename):
        #TODO: Fill in this function
        pass

    def makeTemporalTripletGraphFromFile(self, file):
        #TODO: Make csv file for edges
        res = TemporalTripletEdgeGraph(edges)
        return res

    def getRandomGraphWSameJointIODegree(self, graph):
        g = None
        ioDegSeq = graph.getDegreeSeq()
        g = RandomGraphJointInOutDegree(ioDegSeq)
        return g

    def getRandomGraphLoopAndMultiEdgeWSameJointIODegree(self, graph):
        g = None
        ioDegSeq = graph.getDegreeSeq();
        g = RandomGraphJoinInOutDegreeRemoveLoopMultiEdge(ioDegSeq)
        return g
    def getRandomGraphReciprocalAndInOutDegreeFromGraphOfEdgeArray(self, graph):
        tripplet = getReciprocalAndInOutDegreeSequence(graph.edges)
        g = RandomGraphReciprocaalAndInOutDegree(tripplet)
        return g

    def removeLoopAndMultiEdges(self, edges):
        hs = set()
        edgeHash = 0
        for edge in edges:
            if edge[0] == edge[1]:
                continue
            edgeHash = edge[0]
            edgeHash = (edgeHash << 32) | edge[1]
            hs.add(edgeHash)

        if np.size(hs) == len(edges):
            return edges

        edges = np.matrix([np.size(hs)], [2])
        idx = 0
        edgeHash = (1 << 32)
        for e in hs:
            edges[idx][1] = int(e % edgeHash)
            edges[idx][0] = int(e >> 32)
            idx += 1

        return edges

    def getRandomGraphWNumNodeEdge(self, graph):
        return RandomGraphNumNodeEdge(np.size(graph), len(graph.edges))

    def getRandomGraphW_MAN_Pair(self, graph):
        numNodeMutAsy = getNumReciprocalAssymetricNullPair(graph.edges)
        return RandomGraphNumMANPair(numNodeMutAsy[0], numNodeMutAsy[1], numNodeMutAsy[2])\

    def resetNodeIDsInEdges(self, edges):
        map = {}
        ls = []
        idx = -1

        for e in edges:
            if e[0] in map:
                idx = np.size(map)
                ls.add(""+e[0])
                map.put(e[0], idx)

            if e[1] not in map:
                idx = np.size(map)
                ls.add(""+e[1])
                map.put(e[1], idx)

        nodeNames = []
        ls.toArray(nodeNames)

        for i in range(len(edges)):
            edges[i][0] = map.get(edges[i][0])
            edges[i][1] = map.get(edges[i][1])

        return nodeNames

    '''def getTemporalTimeStampRandomGraphFromTripletEdgesFiles(self, filename):
        #TODO: Make tripletEdges into csv file
        return TemporalTimeStampRandomGraph(tripletEdges)'''
