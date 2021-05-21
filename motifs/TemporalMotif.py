from abc import ABC, abstractmethod

class TemporalMotif(ABC):
    @abstractmethod
    def getMotifFreq(self):
        pass
