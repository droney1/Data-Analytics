from abc import ABC, abstractmethod

class RandomGraphModel(ABC):
    @abstractmethod
    def generateRandomGraph(self):
        pass

    @abstractmethod
    def getGraphInfo(self):
        pass
