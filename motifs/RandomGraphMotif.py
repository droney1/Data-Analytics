from abc import ABC, abstractmethod

class RandomGraphMotif(ABC):
    @abstractmethod
    def getMotifFreq(self, motifSize):
        pass

    @abstractmethod
    def getMotifFreqFromSampledGraphs(self, motifSize, numOfGraphs):
        pass
