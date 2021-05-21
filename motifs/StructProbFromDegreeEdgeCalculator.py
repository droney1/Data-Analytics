from abc import ABC, abstractmethod

class StructProbFromDegreeEdgeCalculator(ABC):
    @abstractmethod
    def computeProbForStruct(self, deg, numEdge, t):
        pass
