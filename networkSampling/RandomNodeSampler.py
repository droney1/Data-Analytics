import numpy as np
import random
#from RandomNodeSampler import *

class RandomNodeSampler:
    def __init__(self, ls, id2Idx, freq, rnd, lastIdx):
        self.ls = ls
        self.id2Idx = id2Idx
        self.freq = freq
        self.rnd = rnd
        self.lastIdx = lastIdx

    def RandomNodeSampler(self, f):
        self.ls = []
        self.id2Idx = {}
        self.freq = f
        for i in range(1, len(self.freq)):
            if self.freq[i] > 0:
                self.ls.add(i)
                self.id2Idx.put(i, np.size(self.ls) - 1)
        self.lastIdx = np.size(self.ls) - 1
        self.rnd = random.random()

    def sampleTargetNodesForSourceNode(self, sID, num):
        length = self.lastIdx + 1
        if sID in self.id2Idx and self.id2Idx.get(sID) <= self.lastIdx:
            length -= 1
            RandomNodeSampler.swapNodeToIdx(sID, self.lastIdx)

        if length < num:
            num = length

        res = [None] * num
        if sID < 0 or sID >= len(self.freq):
            sID = 0
        idx, ii = 0, 0
        for i in range(num):
            if i >= length:
                break
            idx = i + random.uniform(0, length - 1)
            res[ii] = self.ls.get(idx)
            self.id2Idx[i].append(res[ii])
            self.id2Idx[idx].append(self.ls.get(i))
            self.ls.set(idx, self.ls.get(i))
            self.ls.set(i, res[ii])
            if self.freq[res[ii]] == 0:
                print("error")
            if (self.freq[res[ii]] - 1) == 0:
                RandomNodeSampler.swapNodeToIdx(res[ii], self.lastIdx)
                self.lastIdx -= 1
                i -= 1
            num -= 1
            length -= 1
            if length == self.lastIdx:
                RandomNodeSampler.swapNodeToIdx(sID, self.lastIdx)
            if length > (self.lastIdx + 1):
                print("error length")

            ii += 1

        return res

    def swapNodeToIdx(self, nID, idx):
        nIdx = self.id2Idx.get(nID)
        targetID = self.ls.get(idx)
        self.ls.set(nIdx, targetID)
        self.ls.set(idx, nID)
        self.id2Idx.put(nID, idx)
        self.id2Idx.put(targetID, nIdx)

    