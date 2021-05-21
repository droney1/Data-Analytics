import numpy as np
from MotifGraph import *

class StatSubGraphChange:
    def __init__(self, totalTime, nonNullBeg, nonNullEnd, editDisDistr, nonNullTime):
        self.totalTime = totalTime
        self.nonNullBeg = nonNullBeg
        self.nonNullEnd = nonNullEnd
        self.editDisDistr = editDisDistr
        self.nonNullTime = nonNullTime

    def StatSubGraphChange(self):
        self.editDisDistr = [None] * 7

    def calChange(self, pre, cur):
        if cur.timeStep == 0:
            self.nonNullBeg = 0
            return

        editDis = 0
        if pre is None or pre.motifType == 0:
            editDis = TRIAD_EDIT_DISTANCE[0][cur.motifType]
            nonNullDeg = cur.timeStep
        else:
            editDis = TRIAD_EDIT_DISTANCE[pre.motifType][cur.motifType]
            self.editDisDistr[0] += cur.timeStep - 1 - pre.timeStep

        self.editDisDistr[editDis] += 1
        if cur.motifType == 0:
            self.nonNullTime += cur.timeStep - self.nonNullBeg
            self.nonNullBeg = -1

    def toString(self):
        res = self.nonNullTime + ":"
        sumdis = 0
        for i in range(1, len(self.editDisDistr)):
            sumdis += i * self.editDisDistr[i]

        return res + sumdis
