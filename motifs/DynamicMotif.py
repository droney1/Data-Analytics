from abc import ABC, abstractmethod

class DynamicMotif(ABC):
    @abstractmethod
    def getMotifFreq(self):
        pass

    @abstractmethod
    def getMotifTransition(self, motifSize):
        pass

    @abstractmethod
    def getAvgMotifFreq(self, motifSize):
        pass
