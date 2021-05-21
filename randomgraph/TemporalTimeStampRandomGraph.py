import sys
from TemporalRandomGraphToolBox import *
from TemporalRandomGraph import *
sys.path.append("..")
from graphs import *
#from GraphIO import *

class TemporalTimeStampRandomGraph(TemporalRandomGraph):
    def __init__(self, tripletEdges, backupEdges):
        self.tripletEdges = tripletEdges
        self.backupEdges = backupEdges

    def TemporalTimeStampRandomGraph(self, triEdges):
        self.tripletEdges = triEdges

    def getProperties(self):
        return None

    def getPropertyNames(self):
        return None

    def generateRandomEdges(self):
        if self.backupEdges is None:
            if len(self.tripletEdges) == 0 or len(self.tripletEdges[0]) == 0:
                return [0][0]
        shuffleTripletEdgeTimeStamp(self.backupEdges)
        return self.backupEdges

    def selfShuffle(self):
        shuffleTripletEdgeTimeStamp(self.tripletEdges)

    def saveToFile(self, fileName):
        #TODO: Auto-generated method stub
        return

    def saveRandomGraphs(self, filePrefix, num):
        tmpEdges = self.backupEdges
        if tmpEdges is None:
            tmpEdges = self.tripletEdges
        for i in range(num):
            shuffleTripletEdgeTimeStamp(tmpEdges)
            outputMatrix(filePrefix + i + ".txt", tmpEdges)

