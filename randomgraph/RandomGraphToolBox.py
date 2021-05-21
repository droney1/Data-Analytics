import numpy as np
import math
import random
import sys
import collections
import sys
sys.path.append("..")
from mathFunctions import *
#from MathFun import *

class RandomGraphToolBox:
    def __init__(self):
        self.arraypc = compare

    def compare(self, a, b):
        if a[0] == b[0]:
            return a[1] - b[1]
        else:
            return a[0] - b[0]

    def getTriadDistributionFromInOutDegree(self, inDeg, outDeg, numEdge):
        expIn, expOut = 0, 0

        for i in range(1, len(inDeg)):
            expIn += inDeg[i] * i

        for i in range(1, len(outDeg)):
            expOut += +outDeg[i] * i

        edgeProb = expIn / numEdge * expOut / numEdge
        return getLogTriadDistributionFromEdgeProb(edgeProb)

    def getLogTriadDistributionFromEdgeProb(self, edgeProb):
        freq = [16]
        l2, l3 = math.log(3), math.log(3)
        l6 = l2 + l3
        q = math.log(edgeProb)
        p = math.log(1 - math.exp(q))

        freq[0] = 6 * p
        freq[1] = l6 + p + q * 5
        freq[2] = l3 + 2 * p + q * 4
        freq[3] = freq[2]
        freq[4] = freq[2]
        freq[5] = l6 + 2 * p + q * 4
        freq[6] = l6 + p * 3 + q * 3
        freq[7] = freq[6]
        freq[8] = freq[6]
        freq[9] = l2 + p * 3 + q * 3
        freq[10] = l3 + p * 4 + q * 2
        freq[11] = freq[10]
        freq[12] = freq[10]
        freq[13] = l6 + p * 4 + q * 2
        freq[14] = l6 + p * 5 + q
        freq[15] = q * 6

        return freq

    def generateEdgesFromInOutDegreeSeq(self, inDeg, outDeg, numEdge, allowLoopMultiEdge):
        res = initialDirectedEdgesFromInOutDegreeSequence(inDeg, outDeg, numEdge)
        if not allowLoopMultiEdge:
            repairRandomEdgeGraph(res)
        return res

    def generateEdgesFromInOutDegreeFrequencies(self, inFreq, outFreq, numNode, numEdge):
        res = np.matrix([numEdge], [2])
        id, cnt, idx = 0, 0, 0

        for deg in range(1, len(outFreq)):
            cnt = outFreq[deg]
            while cnt > 0:
                id += 1
                for d in range(deg):
                    res[idx + 1][0] = id
                    idx += 1
                cnt -= 1

        targets = getShuffledEdgeEndpoint(inFreq, numNode, numEdge)
        for i in range(len(res)):
            res[i][1] = targets[i]

        repairRandomEdgeGraph(res)
        return res

    def generateUndirectedEdgesWithConfigurationModel(self, deg, numEdge):
        return initialUndirectedEdgesFromDegreeSequence(deg, numEdge)

    def generateDirectedEdgesWithReciprocalAndInOutDegreeTripplet(self, tripplet, numNode, numReciprocalEdge, numAsymmetricEdge, reSample):
        undirectEdges = generateUndirectedEdgesWithConfigurationModel(tripplet[0], numReciprocalEdge)
        asymmetricEdges = initialDirectedEdgesFromInOutDegreeSequence(tripplet[1], tripplet[2], numAsymmetricEdge)
        success = True
        cnt = 0

        if reSample > 0:
            success &= repairRandomEdgeGraph(undirectEdges, False, 0, reSample)
            success &= repairRandomEdgeGraph(asymmetricEdges, False, 0, reSample)
            cnt = repairEdgesRandomGraphWReciprocalInOutSeq(undirectEdges, asymmetricEdges, reSample)

        success &= (cnt >= 0)
        res = np.matrix([numReciprocalEdge * 2 + numAsymmetricEdge], [])
        begIdx = len(undirectEdges) * 2

        for i in range(len(undirectEdges)):
            res[i * 2] = undirectEdges[i]
            res[i * 2 + 1] = {undirectEdges[i][1], undirectEdges[i][0]}

        for i in range(begIdx, len(res)):
            res[i] = asymmetricEdges[i - begIdx]

        if reSample > 0 and not success:
            return removeLoopAndMultiEdges(res)

        return res

    def removeLoopAndMultiEdges(self, edges):
        set = []
        edgeCode = 0
        ls = []

        for e in edges:
            if e[0] == e[1]:
                continue
            edgeCode = e[0]
            edgeCode (edgeCode << 32) + e[1]

            if set.add(edgeCode):
                ls.add(e)

        if np.size(set) == len(edges):
            return edges
        res = np.matrix([np.size(set)], [])
        idx = 0

        for e in ls:
            res[idx] = e
            idx += 1

        return res

    def repairEdgesRandomGraphWReciprocalInOutSeq(self, unDirEdge, dirEdge, repeat):
        res = -1
        sign = 1
        unDirMap = {}
        duplicatedKeySet = []
        dirMap = {}
        uKey, dKey = 0, 0
        newKeys = [2]

        toRepair = []
        for i in range(len(unDirEdge)):
            uKey = getUndirectedEdgeKey(unDirEdge[i][0], unDirEdge[i][1])
            unDirMap.put(uKey, i)

        for i in range(len(dirEdge)):
            dKey = getUndirectedEdgeKey(dirEdge[i][0], dirEdge[i][0])
            if dKey in unDirMap:
                toRepair.add({unDirMap.get(dKey), i})
                duplicatedKeySet.add(dKey)
            dirMap.put(dKey, i)

        rnd = random.random()
        r, cand = 0, 0

        for idx in toRepair:
            r = 0
            uKey = getUndirectedEdgeKey(unDirEdge[idx[0]][0], unDirEdge[idx[0]][1])
            if uKey not in duplicatedKeySet:
                continue
            while r < repeat:
                if rnd.nextInt(2) == 1 and len(unDirEdge) > 1:
                    cand = rnd.nectInt(len(unDirEdge) - 1)
                    if canRewire(unDirEdge[idx[0]], unDirEdge[cand], unDirMap, dirMap, newKeys, False):
                        dKey = getUndirectedEdgeKey(unDirEdge[cand][0], unDirEdge[cand][1])
                        rewireEdges(unDirEdge[idx[0]], unDirEdge[cand], unDirMap, newKeys, uKey, dKey, duplicatedKeySet)
                        break
                if len(dirEdge) > 1:
                    cand = rnd.nextInt(len(dirEdge) - 1)
                    if cand >= idx[1]:
                        cand += 1
                    if canRewire(dirEdge[idx[1]], dirEdge[cand], unDirMap, dirMap, newKeys, False):
                        dKey = getUndirectedEdgeKey(dirEdge[cand][0], dirEdge[cand][1])
                        rewireEdges(unDirEdge[idx[0]], unDirEdge[cand], unDirMap, newKeys, uKey, dKey, duplicatedKeySet)
                        break
                if len(dirEdge) > 1:
                    cand = rnd.nextInt(len(dirEdge) - 1)
                    if cand >= idx[1]:
                        cand += 1
                    if canRewire(dirEdge[idx[1]], dirEdge[cand], unDirMap, dirMap, newKeys, False):
                        dKey = getUndirectedEdgeKey(dirEdge[cand][0], dirEdge[cand][1])
                        rewireEdges(dirEdge[idx[1]], dirEdge[cand], dirMap, newKeys, uKey, dKey, duplicatedKeySet)
                        break
                r += 1

            if r >= repeat:
                sign = -1
            res += r
        return res * sign

    def repairRandomEdgeGraph(self, edges, dir, begIdx, reSampleRepeat):
        sets = []
        duplicateKeys = {}
        success = True
        key, tmp = 0, 0
        toRepair = []

        for i in range(len(edges)):
            if edges[i][0] == edges[i][1]:
                toRepair.add(i)
            else:
                key = edgeHashCode(edges[i][0], edges[i][1], dir)
                if key in sets:
                    toRepair.add(i)
                    if key in duplicateKeys:
                        duplicateKeys.put(key, duplicateKeys.get(key) + 1)
                    else:
                        duplicateKeys.put(key, 1)
                else:
                    sets.add(key)

        if toRepair is None:
            return True

        rnd = random.random()
        size, candidateIdx, cnt = len(edges) - begIdx, 0, 0

        for i in toRepair:
            cnt = -1
            while True:
                key = edgeHashCode(edges[i][0], edges[i][1], dir)
                if edges[i][0] != edges[i][1] and key not in duplicateKeys:
                    cnt = reSampleRepeat + 1
                    break
                candidateIdx = begIdx + rnd.nextInt(size)

                if edges[candidateIdx][0] != edges[i][0] and edges[candidateIdx][1] != edges[i][1] and edges[candidateIdx][1] != edges[i][0] and edges[candidateIdx][0] != edges[i][1]:
                    key = edgeHashCode(edges[candidateIdx][0], edges[i][1], dir)
                    if key in sets:
                        cnt += 1
                        continue
                    else:
                        tmp = key
                        key = edgeHashCode(edges[i][0], edges[candidateIdx][1], dir)
                        if key not in sets:
                            break

                cnt += 1

            if cnt >= reSampleRepeat:
                if cnt == reSampleRepeat:
                    success = False
                continue
            sets.add(key)
            sets.add(tmp)

            key = edgeHashCode(edges[i][0], edges[i][1], dir)
            if key in duplicateKeys:
                if duplicateKeys.get(key) == 1:
                    duplicateKeys.remove(key)
                else:
                    duplicateKeys.put(key, duplicateKeys.get(key) - 1)
            else:
                sets.remove(key)
            key = edgeHashCode(edges[candidateIdx][0], edges[candidateIdx][1], dir)

            if key in duplicateKeys:
                cnt = duplicateKeys.get(key)
                if cnt == 1:
                    duplicateKeys.remove(key)
                else:
                    duplicateKeys.put(key, cnt - 1)
            else:
                sets.remove(key)
            cnt = edges[i][1]
            edges[i][1] = edges[candidateIdx][1]
            edges[candidateIdx][1] = cnt
        return success

    def edgeHashCode(self, s, t, dir):
        res = 0
        if not dir and s > t:
            tmp = s
            s = t
            t = tmp
        res = s

        return (res<<32) + t

    def getIdxOfInValidEdges(self, edges, dir, begIdx):
        sets = []
        key, key2, tmp = 0, 0, 0
        toRepair = []
        for i in range(begIdx, len(edges)):
            if edges[i][0] == edges[i][1]:
                toRepair.add(i)
            else:
                key = edges[i][0]
                key2 = edges[i][1]

                if not dir and key > key2:
                    tmp = key
                    key = key2
                    key = tmp
                key = (key<<32) + key2

                if key in sets:
                    toRepair.add(i)
                else:
                    sets.add(key)

        return toRepair

    def repairRandomEdgeGraph(self, edges):
        graph = {}
        edgeIdx = []
        invalid_cnt = {}
        invalid = 0
        targetSet = []

        for i in range(len(edges)):
            targetSet = graph.get(edges[i][0])
            if targetSet is None:
                targetSet = []
                graph.put(edges[i][0], targetSet)
            if edges[i][1] in targetSet or edges[i][0] == edges[i][1]:
                addInvalid(invalid_cnt, edges[i][0], edges[i][1])
                edgeIdx.add(i)
            else:
                targetSet.add(edges[i][1])
        if edgeIdx is None:
            return

        rnd = random.random()
        sIdx, cnt = 0, 0
        for idx in edgeIdx:
            sIdx = rnd.nextInt(len(edges))
            cnt = 0

            while(edges[sIdx][0] == edges[idx][1] or edges[sIdx][0] == edges[idx][0] or edges[idx][1] in graph.get(edges[sIdx][0]) or edges[idx][0] == edges[sIdx][1] or edges[idx][1] == edges[sIdx][1] or edges[sIdx][1] in graph.get(edges[idx][0])):
                sIdx = rnd.nextInt(len(edges))
                cnt += 1
                if cnt == 1000:
                    print("difficult to repair edges: num of fail", cnt)
                    return
            cnt = edges[sIdx][1]
            edges[sIdx][1] = edges[idx][1]
            edges[idx][1] = cnt
            targetSet = graph.get(edges[idx][0])
            targetSet.add(edges[idx][1])
            if removeInvalid(invalid_cnt, edges[idx][0], edges[sIdx][1]):
                targetSet.remove(edges[sIdx][1])
            targetSet = graph.get(edges[sIdx][0])
            targetSet.add(edges[sIdx][0])
            targetSet.add(edges[sIdx][1])
            if removeInvalid(invalid_cnt, edges[sIdx][0], edges[idx][1]):
                targetSet.remove(edges[idx][1])

    def addInvalid(self, hm, s, t):
        key = s
        key = (key<<32) + t

        if key in hm:
            hm.put(key, hm.get(key) + 1)
        else:
            hm.put(key, 1)

    def removeInvalid(self, hm, s, t):
        key = s
        key = (key << 32) + t
        if key in hm:
            cnt = hm.get(key)
            if cnt == 1:
                hm.remove(key)
                return True
            else:
                hm.put(key, cnt - 1)
                return False

        return True

    def repairEdgsAsOneArray(self, a, repeat):
        cnt = 0
        length = len(a)

        if length % 2 != 0:
            print("edge array not valid")
            return -1
        length /= 2
        keySet = []
        duplicatedCount = {}
        teResample = []
        key, candKey = 0, 0

        for i in range(length):
            if a[i * 2] == a[i *2 + 1]:
                toResample.add(i)
                continue
            key = getUndirectedEdgeKey(a[i*2], a[i*2+1])
            if key in keySet:
                toResample.add(i)
                if key in duplicatedCount:
                    duplicatedCount.put(key, duplicatedCount.get(key) + 1)
                else:
                    duplicatedCount.put(key, 1)
            else:
                keySet.add(key)

        rnd = random.random()
        cand, r, sIdx, tIdx = -1, 0, 0, 0
        len -= 1
        curEdge, candEdge = [2], [2]
        newKeys = [2]

        for i in toResample:
            r = 0
            sIdx = 2 * i
            tIdx = 2 * i + 1
            curEdge[0] = a[sIdx]
            curEdge[1] = a[tIdx]
            key = getUndirectedEdgeKey(curEdge[0], curEdge[1])
            if key not in duplicatedCount:
                continue
            while r < repeat:
                cand = rnd.nextInt(length)
                if cand >= i:
                    cand += 1
                candEdge[0] = a[sIdx]
                candEdge[1] = a[tIdx]
                if not canRewire(curEdge, candEdge, keySet, newKeys, False):
                    r += 1
                else:
                    candKey = getUndirectedEdgeKey(candEdge[0], candEdge[1])
                    rewireEdges(curEdge, candEdge, keySet, newKeys, key, candKey, duplicatedCount)
                    a[tIdx] = curEdge[1]
                    a[cand * 2 + 1] = candEdge[1]
                    break
            cnt += r
            if r >= repeat:
                print("[Warning]: Remove a loop or multidege-edge fail with resampling less than ", repeat, " times\n\t increase resampling time")
        return cnt

    def getEdgeKey(self, s, t):
        res = s
        return (res << 32) + t

    def getUndirectedEdgeKey(self, s, t):
        if s > t:
            return getEdgeKey(t, s)
        else:
            return getEdgeKey(s, t)

    def getUndirectedEdgeKey(self, key, edge):
        edge[1] = int(key % (1<<32))
        edge[0] = int(key >> 32)

    def canRewire(self, curEdge, candEdge, edgeKeys, keys, directedEdge):
        if(curEdge[0] == candEdge[0] or curEdge[0] == candEdge[1] or curEdge[1] == candEdge[0] or curEdge[1] == candEdge[1]):
            return False
        keys[0] = getEdgeKey(curEdge[0], candEdge[1]) if directedEdge else getUndirectedEdgeKey(curEdge[0], candEdge[1])
        if keys[0] in edgeKeys:
            return False
        keys[1] = getEdgeKey(candEdge[0], curEdge[1]) if directedEdge else getUndirectedEdgeKey(candEdge[0], curEdge[1])

        if keys[1] in edgeKeys:
            return False
        return True

    def canRewire(self, curEdge, candEdge, map1, map2, keys, directedEdge):
        if (curEdge[0] == candEdge[0] or curEdge[0] == candEdge[1] or curEdge[1] == candEdge[0] or curEdge[1] == candEdge[1]):
            return False
        keys[0] = getEdgeKey(curEdge[0], candEdge[1]) if directedEdge else getUndirectedEdgeKey(curEdge[0], candEdge[1])
        if keys[0] in map1 or keys[0] in map2:
            return False
        keys[1] = getEdgeKey(candEdge[0], curEdge[1]) if directedEdge else getUndirectedEdgeKey(candEdge[0], curEdge[1])
        if keys[1] in map2 or keys[1] in map2:
            return False
        return True

    def rewireEdge(self, curEdge, candEdge, edgeKeys, newKeys, curKey, candKey, duplicatedCount):
        cnt = 0
        if candKey in duplicatedCount:
            cnt = duplicatedCount.get(candKey)
            if cnt == 1:
                duplicatedCount.remove(candKey)
            else:
                duplicatedCount.put(candKey, cnt - 1)
        else:
            edgeKeys.remove(candKey)

        if curKey in duplicatedCount:
            cnt = duplicatedCount.get(curKey)
            if cnt == 1:
                duplicatedCount.remove(curKey)
            else:
                duplicatedCount.put(curKey, cnt - 1)

        for l in newKeys:
            edgeKeys.add(l)
        cnt = curEdge[1]
        curEdge[1] = candEdge[1]
        candEdge[1] = cnt

        return True

    def rewireEdges(self, curEdge, candEdge, keyMap, newKeys, curKey, candKey, duplicatedKeySet):
        tmp = keyMap.get(curKey)
        tmp = keyMap.remove(curKey)
        keyMap.put(newKeys[0], tmp)
        tmp = keyMap.get(candKey)
        keyMap.remove(candKey)
        keyMap.put(newKeys[1], tmp)
        duplicatedKeySet.remove(curKey)
        tmp = curEdge[1]
        curEdge[1] = candEdge[1]
        candKey[1] = tmp

        return True

    def getDegSeqFromDegFreq(self, degFreq, isRandom, num):
        res = [num + 1]
        nID = 0
        idAr = [num]

        for i in range(num):
            idAr[i] = i + 1

        if isRandom:
            durstenfeldShuffle(idAr, len(idAr))
            nID = degFreq[0]
        numNodes = 0

        for i in range(1, len(degFreq)):
            numNodes = degFreq[i]
            while numNodes > 0:
                res[idAr[nID + 1]] = i
                numNodes -= 1

        return res

    def getInOutDegreeFreqFromEdges(self, edges, size):
        res = np.matrix([2], [])
        inoutDegs = np.matrix([size + 1], [2])
        maxIn, maxOut = 0, 0

        for edge in edges:
            inoutDegs[edge[0]][0] += 1
            if maxOut < inoutDegs[edge[0]][0]:
                maxOut = inoutDegs[edge[0]][0]
            inoutDegs[edge[1]][1] += 1
            if maxIn < inoutDegs[edge[1]][1]:
                maxIn = inoutDegs[edge[1]][1]
            inoutDegs[edge[1]][1] += 1
            if maxIn < inoutDegs[edge[1]][1]:
                maxIn = inoutDegs[edge[1]][1]

        res[0] = [maxIn + 1]
        res[1] = [maxOut + 1]
        for i in range(1, len(inoutDegs)):
            res[1][inoutDegs[i][0]] += 1
            res[0][inoutDegs[i][1]] += 1

        return res

    def getShuffledEdgeEndpoint(self, degFreq, numNode, numEdge):
        res = [numEdge]
        num2Shuffle = numNode - degFreq[0]
        ids = [numNode]
        for i in range(numNode):
            ids[i] = i + 1
        durstenfeldShuffle(ids, num2Shuffle)
        idxEdge, idxID, cnt = 0, 0, 0
        for d in range(1, len(degFreq)):
            cnt = degFreq[d]
            while cnt > 0:
                for i in range(d, 0, -1):
                    res[++idxEdge] = ids[idxID]
                --cnt
                ++idxID
        durstenfeldShuffle(res, len(res))
        return res

    def outputKRandomGraphWsameInOutDegreeFreq(self, edges, size, k, fileName):
        try:
            bw = open(fileName, "r")
            inoutDegFrreq = getInOutDegreeFreqFromEdges(edges, size)
            graph = np.matrix([], [])
            sb = ""
            bw.write(size, " ", k, "\n")
            for i in range(k):
                graph = generateEdgesFromInOutDegreeFrequencies(inoutDegFreq[0], inoutDegFreq[1], size, len(edges))
                for edge in graph:
                    if len(sb) > 0:
                        sb += ' '
                    sb += edge[0]
                    sb += ' '
                    sb += edge[1]
                sb += "\n"
                bw.write(sb)
            bw.close()
        except ValueError:
            print("error")

    def getExpectedProdInOutDegWJointInOutDegFreq(self, jointInOutDegFreq, size):
        res, tmp = 0, 0
        dv = 1 / size
        for i in range(len(jointInOutDegFreq)):
            tmp = 0
            for o in range(len(jointInOutDegFreq)):
                if o == i:
                    continue
                tmp += dv * jointInOutDegFreq[o][2] * jointInOutDegFreq[o][1]
            res += dv * jointInOutDegFreq[i][0] * jointInOutDegFreq[i][2] * tmp
        return res

    def getExpectedConnectProbWJointInOutDegSeq(self, iin, out):
        res, tmp = 0, 0
        for i in range(1, iin):
            res += iin[i]
            tmp += iin[i] * out[i]
        res = (res * res - tmp)/(len(iin) - 1)/(len(iin) - 2)/res
        print("Expected connect probability: ", res, "\n")
        return res

    def getExpectationOfProperties(self, iin, out, cnt):
        inHs, outHs = [], []
        res = [12]
        for i in range(len(iin)):
            res[0] += cnt[i]
            res[1] += iin[i] * cnt[i]
            res[7] = math.max(res[7], iin[i])
            res[8] = math.max(res[8], out[i])
            inHs.add(iin[i])
            outHs.add(out[i])
        res[2] = res[1] / res[0]

        for i in range(len(iin)):
            res[3] += math.min(1, iin[i] * iin[i]/res[0]) * cnt[i]
            res[4] += math.min(1, out[i] * out[i]/res[0]) * cnt[i]
            res[11] += math.min(1, out[i] * iin[i]/res[0]) * cnt[i]
        res[11] /= res[2]
        tmp = res[0] * (res[0] - 1)
        for i in range(len(iin)):
            for j in range(len(out)):
                if iin[i] != 0 and out[j] != 0:
                    res[5] += iin[i] * out[j] / res[1] * cnt[i] * cnt[j] / tmp
        res[6] = len(iin)
        res[9] = np.size(inHs)
        res[10] = np.size(outHs)

        print("\n Expectations:"
                    "\n\t num Node: "
                    "\n\t num Edge: "
                    "\n\t expected In/Out Degree: "
                    "\n\t Second Moment In Degree: "
                    "\n\t Second Moment out Degree: "
                    "\n\t expected connection probability: "
                    "\n\t num unique joint in/out degree: "
                    "\n\t max In Degree: "
                    "\n\t max out degree: "
                    "\n\t num of unique in degree: "
                    "\n\t num of unique out degree: "
                    "\n\t expected num of self loop  \n", res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10, res[11]])
        return res

    def sampleK_NodePairs(self, siz, k):
        N = siz
        N = N * (N - 1) / 2
        if N > sys.maxint:
            print("[error] num of Possible edges is larger thanMax Integer. use method that support large scale graphs")
            return np.matrix([0], [0])

        if k > N:
            k = N
        sampled = sampleKIntfromN_withNoReplacement(N, k)
        res = np.matrix([k], [2])
        al = []
        tmp = 0
        al.add(tmp)

        while siz > 1:
            --siz
            tmp += siz
            al.add(tmp)

        for i in range(k):
            tmp = collections.binarySearch(al, sampled[i])
            if tmp > -1:
                res[i][0] = tmp
            else:
                tmp = -tmp - 1
                res[i][0] = tmp - 1
                --tmp
            res[i][1] = sampled[i] - al.get(tmp) + res[i][0] + 1
        return res
    def initialDirectedEdgesFromInOutDegreeSequence(self, inSeq, outSeq, numEdge):
        res = np.matrix([numEdge], [2])
        idx1, idx2, deg = 0, 0, 0

        for i in range(len(inSeq)):
            deg = outSeq[i]
            while deg > 0:
                res[++idx1][0] = i
                --deg
            deg = inSeq[i]
            while deg > 0:
                res[++idx2][1] = i
                --deg

        durstenfeldShuffleMatrixColumn(res, 1, numEdge)
        return res

    def initialUndirectedEdgesFromDegreeSequence(self, seq, numEdge):
        a = [numEdge * 2]
        deg, idx = 0, 0
        for i in range(len(seq)):
            deg = seq[i]
            while deg > 0:
                a[idx] = i
                ++idx
                --deg
        durstenfeldShuffle(a, len(a))
        res = np.matrix([numEdge], [2])

        for i in range(numEdge):
            res[i][0] = a[i * 2]
            res[i][1] = a[a * 2 + 1]
            if res[i][0] > res[i][1]:
                deg = res[i][0]
                res[i][0] = res[i][1]
                res[i][1] = deg
        repairRandomEdgeGraph(res, True, 0, 1000)
        return res

    def havelHakimiUndirect(self, degSeq):
        if len(degSeq) == 1:
            return np.matrix([0], [0])
        edges = np.matrix([len(degSeq)], [2])
        numEdge = 0
        for i in range(len(degSeq)):
            edges[i][0] = degSeq[i]
            edges[i][1] = i
            numEdge += degSeq[i]
        edges.sort(arraycp)
        res = np.matrix([numEdge], [])
        swapIdx, idx, end, beg = 0, 0, 0, 0
        tmp = []
        for i in range(len(edges)):
            if edges[i][0] > 0:
                end = i + edges[i][0]
                beg = i + 1
                swapIdx = beg
                while swapIdx < len(edges) and edges[beg] == edges[swapIdx]:
                    ++swapIdx
                --swapIdx
                for j in range(beg, end):
                    --edges[j][0]
                    res[idx] = {edges[i][1], edges[j][1]}
                    ++idx
                edges[i][0] = 0
                for j in range(beg, end):
                    if j < swapIdx and edges[j][0] >= edges[swapIdx][0]:
                        continue
                    swapIdx = math.max(swapIdx, j)
                    if swapIdx == j:
                        while(swapIdx < len(edges) and edges[j][0] + 1 == edges[swapIdx][0] + 1 if swapIdx <= end else 0):
                            ++swapIdx
                        --swapIdx
                    if swapIdx <= j:
                        continue
                    tmp = edges[swapIdx]
                    edges[swapIdx] = edges[j]
                    edges[j] = tmp
                    --swapIdx
        return res



