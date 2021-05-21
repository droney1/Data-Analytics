from abc import ABC, abstractmethod

class GraphProperty(ABC):
    @abstractmethod
    def getDegreeSeq(self):
        pass

    @abstractmethod
    def getDegreeFreq(self):
        pass
