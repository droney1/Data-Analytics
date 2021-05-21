import numpy as np
import math

class MotifAlg:
    def __init__(self):
        self.triadInOutDegs = np.matrix([], [], [], {
            {{0, 0}, {0, 0}, {0, 0}},
            {{0, 1}, {1, 0}, {0, 0}},
            {{1, 1}, {1, 1}, {0, 0}},
            {{0, 2}, {1, 0}, {1, 0}},
            {{2, 0}, {0, 1}, {0, 1}},
            {{1, 1}, {0, 1}, {1, 0}},
            {{0, 1}, {2, 1}, {1, 1}},
            {{1, 0}, {1, 2}, {1, 1}},
            {{2, 0}, {0, 2}, {1, 1}},
            {{1, 1}, {1, 1}, {1, 1}},
            {{1, 1}, {2, 2}, {1, 1}},
            {{0, 2}, {2, 1}, {2, 1}},
            {{2, 0}, {1, 2}, {1, 2}},
            {{1, 1}, {1, 2}, {2, 1}},
            {{2, 1}, {1, 2}, {2, 2}},
            {{2, 2}, {2, 2}, {2, 2}}
        })

        self.triadNodePermutaion = np.matrix([], [], {
            {0},
            {0, 1, 2, 3, 4, 5},
            {0, 3, 4},
            {0, 3, 4},
            {0, 3, 4},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0, 1},
            {0, 3, 4},
            {0, 3, 4},
            {0, 3, 4},
            {0, 1, 2, 3, 4, 5},
            {0, 1, 2, 3, 4, 5},
            {0},
        })

        self.triadPermutation = np.matrix([], [], {
            {0, 1, 2},
            {0, 2, 1},
            {1, 0, 2},
            {1, 2, 0},
            {2, 0, 1},
            {2, 1, 0}
        })

        self.numEdgeInTriads = [], {
            0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6
        }

    def getTriadFreqRandomGraphFromJoinInOutDefFreq(self, iin, out, cnt, size):
        dist, tmpDist = [None] * 16, [None] * 16
        print("\nCalculating traidFreq\n")
        numEdge = 0
        for i in range(len(iin)):
            numEdge += iin[i] * cnt[i]
        #TODO: the logBase might be dependent on the motif type
        logBase = math.log(numEdge)
        logProbFactor = np.matrix([len(iin)], [3], [16])
        setLogProbFactor(logProbFactor, iin, out, numEdge)

        nIDs = [None] * 3
        sumTriadInOutDeg = 0
        alpha, log6, log2 = 0, math.log(6), math.log(2)

        for i in range(len(out)):
            nIDs[0] = i
            for j in range(i, len(out)):
                nIDs[1] = j

                if j == i:
                    if cnt[i] < 2:
                        continue

                for k in range(j, len(out)):
                    nIDs[2] = k
                    if k == i:
                        if cnt[i] < 3:
                            continue
                        alpha = 0
                        for l in range(3):
                            alpha += math.log(cnt[i] - l)
                            alpha -= log6

                    elif (i == j) and (j != k):
                        alpha = math.log(cnt[i]) + math.log(cnt[i] - 1) + math.log(cnt[k]) - log2
                    elif (i != j) and (j == k):
                        if cnt[j] < 2:
                            continue
                        alpha = math.log(cnt[i]) + math.log(cnt[j]) + math.log(cnt[j] - 1) - log2
                    else:
                        alpha = math.log(cnt[i]) + math.log(cnt[j]) + math.log(cnt[k])
                    sumTriadInOutDeg = iin[k] + out[k] + iin[j] + out[j] + iin[i] + out[i]
                    np.zeros(tmpDist)
                    tmp1, tmpSum = 0, 0

                    for t in range(16):
                        if numEdge + self.numEdgeInTriads[t] < sumTriadInOutDeg:
                            continue
                        for p in traidNodePermutation[t]:
                            tmp1 = 0
                            for l in range(3):
                                if logProbFactor[nIDs[l]][traidPermutation[p][l]][t] == -math.inf:
                                    tmp = -math.inf
                                    break
                                tmp1 += logProbFactor[nIDs[l]][self.triadPermutation[p][l]][t]

                            if tmp1 != -math.inf:
                                tmpDist[t] += math.exp(tmp1 - self.numEdgeInTriads[t] * logBase)

                    for v in tmpDist:
                        tmpSum += v
                    print("\n" + iin[i] + out[i] + cnt[i] + iin[j] + out[j] + cnt[j] + iin[k] + out[k] + cnt[k])\

                    for t in range(16):
                        print(tmpDist[t])
                        dist[t] += math.exp(alpha) * tmpDist[t] / tmpSum
                    print("\n")
        return dist

    def setContributionOfNodeAsTriadNodeToLogProbability(self, probMtr, triadType, nIdx, nIn, nOut, size):
        for tnIdx in range(3):
            probMtr[nIdx][tnIdx][triadType] = getLogProbOfInOutTriadWNodeJoinInOutDeg(nIn, nOut, self.triadInOutDegs[triadType][tnIdx][0], self.triadInOutDegs[triadType][tnIdx][1], size)

    def duplicateContribution(probMtr, idx1, idx2):
        for i in range(3):
            for t in range(16):
                probMtr[idx2][i][t] = probMtr[idx1][i][t]

    def getLogProbOfInOutTriadWNodeJoinInOutDeg(self, nIn, nOut, triadIn, triadOut, size):
        res = 0

        if nOut < triadOut or nIn < triadIn:
            return -math.inf

        nullNOut, nullTOut = size - 1 - nOut, 2 - triadOut
        nullNIn, nullTIn = size - 1 - nIn, 2 - triadIn

        if nullNOut < nullTOut or nullNIn < nullTIn:
            return -math.inf

        for i in range(triadOut):
            res += math.log(nOut - i)

        for i in range(triadIn):
            res += math.log(nIn - i)

        for i in range(nullTOut):
            res += math.log(nullNOut - i)

        for i in range(nullTIn):
            res += math.log(nullNIn - i)

        return res

    def getLogProbOfInOutTriadWNodeJoinInOutDeg2(self, nIn, nOut, triadIn, triadOut, numEdge):
        res = 0
        if nOut < triadOut or nIn < triadIn:
            return -math.inf

        for i in range(triadOut):
            res += math.log(nOut - i)

        for i in range(triadIn):
            res += math.log(nIn - i)

        return res

    def setLogProbFactor(self, logProbFactor, iin, out, numEdge):
        for d in range(len(iin)):
            for u in range(3):
                for t in range(16):
                    logProbFactor[d][u][t] = getLogProbOfInOutTriadWNodeJoinInOutDeg2(iin[d], out[d], self.triadInOutDegs[t][u][0], self.triadInOutDegs[t][u][1], numEdge)

    def getTriadFreqFromConfigurationModel(self, iin, out, cnt, size, opt):
        res, tmpDist = [None] * 16, [None] * 16
        numEdge = 0

        for i in range(len(iin)):
            numEdge += iin[i] * cnt[i]

        nIDs = [None] * 3
        cal = None

        if opt == 4:
            cal = CalculatorTriadStructProbConfigModelIncreaseNullEdgeProb()
        elif opt == 1:
            cal = CalculatorTriadStructProbConfigModelNullEdgeProbIsOne()
        elif opt == 2:
            cal = CalculatorTriadStructProbConfigModelNoLoop()
        elif opt == 3:
            cal = CalculatorTriadStructProbConfigModelNoFirstOrderApprox()
        else:
            cal = CalculatorTriadStructProbConfigModel()

        sumTriadInOutDeg = 0
        alpha, distSum, log2, log3, log6, tmpVal = 0, 0, math.log(2), math.log(3), math.log(6), 0

        for i in range(len(iin)):
            nIDs[0] = i
            for j in range(i, len(iin)):
                if j == i and cnt[j] < 2:
                    continue
                nIDs[1] = j
                for k in range(j, len(iin)):
                    if k == i and cnt[i] < 3:
                        continue
                    elif k == j and cnt[j] < 2:
                        continue
                    nIDs[2] = k

                    alpha = math.log(cnt[i])
                    if j == i:
                        alpha += math.log(cnt[i] - 1) - log2
                    else:
                        alpha += math.log(cnt[j])

                    if k == i:
                        alpha += math.log(cnt[i] - 2) - log3
                    elif k == j:
                        alpha += math.log(cnt[j] - 1) - log2
                    else:
                        alpha += math.log(cnt[k])

                    sumTriadInOutDeg = iin[k] + out[k] + iin[j] + out[j] + iin[i] + out[i]
                    np.zeros(tmpDist)

                    for t in range(16):
                        if numEdge + self.numEdgeInTriads < sumTriadInOutDeg:
                            continue
                        tmpDist[t] = TriadStructProbability.getApproxProbConfigModel(nIDs, iin, out, t, numEdge, cal)

                    distSum = 0
                    for d in tmpDist:
                        distSum += d

                    for t in range(16):
                        res[t] += math.exp(alpha) * tmpDist[t]/distSum

        return res





