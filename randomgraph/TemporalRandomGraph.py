from abc import ABC, abstractmethod

class TemporalRandomGraph(ABC):
    @abstractmethod
    def getProperties(self):
        pass

    @abstractmethod
    def getPropertyNames(self):
        pass

    @abstractmethod
    def generateRandomEdges(self):
        pass

    @abstractmethod
    def selfShuffle(self):
        pass

    @abstractmethod
    def saveToFile(self, fileName):
        pass

    @abstractmethod
    def saveRandomGraphs(self, filePrefix, num):
        pass