from abc import ABC, abstractmethod

class Motif(ABC):
    @abstractmethod
    def getMotifFreq(self, motifSize):
        pass

    @abstractmethod
    def getNodeMotifFreq(self, motifSize):
        pass
