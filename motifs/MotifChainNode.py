import numpy as np

class MotifChainNode:
    def __init__(self, timeStep, motifType):
        self.timeStep = timeStep
        self.motifType = motifType

    def MotifChainNode(self, t, type):
        self.timeStep = t
        self.motifType = type

    def toString(self):
        return self.timeStep + ":" + self.motifType + " "

    def compareTo(self, b):
        return self.timeStep + b.timeStep
