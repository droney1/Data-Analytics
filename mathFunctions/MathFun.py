import math
from random import random
from random import seed
import numpy as np

class MathFun:
    def __init__(self):
        pass

    def cloneCensus(self, copy, org):
        if copy is None or len(copy) != len(org):
            copy = []
        for i in range(len(org)):
            copy[i] = org[i]

        return copy

    def KLDiverseFromFreqWithBayesPrior(self, preStep, curStep):
        res = 0
        sum1, sum2 = 0, 0
        prior = 0
        bs = False

        if len(preStep) != len(curStep):
            print("Distribution size not matched")
            return 1

        for i in range(len(preStep)):
            sum1 += preStep[i]
            sum2 += curStep[i]
            if preStep[i] == 0 or curStep[i] == 0:
                bs = True

        if bs:
            prior = 1
            sum1 += len(preStep)
            sum2 += len(curStep)

        for i in range(len(preStep)):
            p1 = (preStep[i] + prior) / sum1
            res += p1 * (math.log(p1) - math.log((curStep[i] + prior) / sum2))

        return res

    def KLDiversionFromNonZeroFreq(self, preStep, curStep):
        res = 0
        sum1, sum2 = 0, 0

        if len(preStep) != len(curStep):
            print("Distribution size not matched")
            return 1

        for i in range(len(preStep)):
            sum1 += preStep[i]
            sum2 += curStep[i]

        for i in range(len(preStep)):
            p1 = preStep[i] / sum1
            res += p1 * (math.log(p1) - math.log(curStep[i] / sum2))

        return res

    def durstenfeldShuffle(self, array, length):
        randNum = random()
        length = min(len(array), length)

        for i in range(len(length)):
            seed(len(array) - 1)
            idx = i + next(randNum)
            tmp = array[i]
            array[i] = array[idx];
            array[idx] = tmp

    def durstenfeldShuffleMatrixColumn(self, m, col, length):
        length = min(length, len(m))
        randNum = random()

        for i in range(len(length)):
            seed(len(m) - 1)
            idx = i + next(randNum)
            tmp = m[idx][col]
            m[idx][col] = m[i][col]
            m[i][col] = tmp

    def durstenfeldShuffleMatrixMultiColumn(self, m, colIdx, length):
        tmp = []
        randNum = random()

        if length > len(m):
            length = len(m)

        for i in range(len(length)):
            seed(length - i)
            idx = next(randNum)

            for j in range(len(colIdx)):
                tmp[j] = m[idx][colIdx]
                m[i][colIdx[j]] = m[idx][colIdx[j]]
                m[idx][colIdx[j]] = tmp[j]

    def resorvoirSampling(self, totalNum, k):
        if k > totalNum:
            k = totalNum
        res = []
        idx = 0
        randNum = random()

        while idx < k:
            res[idx] = idx
            idx += 1

        if totalNum >= (1 << 31):
            l = idx
            while l < totalNum:
                seed(l + 1)
                tmp = next(randNum)
                if tmp < k:
                    res[tmp] = 1
                    l += 1

            return res

        while idx < totalNum:
            seed(idx + 1)
            pos = next(randNum)
            if pos < k:
                res[pos] = idx
            idx += 1

    def nextLong(self, rng, n):

        #Figure out if do while loop needs to be implemented another way

        seed(rng)
        randNum = random()
        while True:
            bits = (next(randNum) << 1) >> 1
            val = bits % n

        return val

    def AChaoWeightedResorviorSampling(self, weight, k):
        res = []
        randNum = random()

        if k >= len(weight):
            k = len(weight)

        idx = 0
        sum = 0

        while idx < k:
            sum += weight[idx]/k
            res[idx + 1] = idx + 1

        while idx < len(weight):
            sum += weight[idx] / k
            if next(randNum) < (weight[idx] / sum):
                seed(k)
                res[next(randNum)] = idx + 1

            idx += 1

        return res

    def AChaoWeightedResorviorSampling(self, elements, weight, num):
        res = []

        idx = 0
        length = np.size(elements)
        sum = 0

        while idx < num:
            res[idx] = idx
            sum += weight.get(idx) / num
            idx += 1

        randNum = random()

        while idx < length:
            w = weight.get(idx)
            sum += w / num
            if next(randNum) < (w / sum):
                res[next(randNum)] = idx

        res.sort()

        for i in range(len(res) - 1, 0):
            if weight.get(res[i]) == 1:
                weight.remove(res[i])
            else:
                weight.set(res[i], weight.get(res[i]) - 1)
            res[i] = elements.get(res[i])

        return res

    def sampleKIntfromN_withNoReplacement(self, n, k):
        if k > n:
            res = []
            for i in range(0, n):
                res[i] = i
            return res

        res = []
        randNum = random()
        map = {}    #TODO: Figure out if this needs to be filled

        for i in range(0, k):
            if i in map:
                map.get(i)
            else:
                curVal = i
            res[i] = i + next(randNum)
            if res[i] in map:
                tmp = map.get(res[i])
                map.put(res[i], curVal)
                res[i] = tmp
            else:
                map.put(res[i], curVal)
            n -= 1

        return res
