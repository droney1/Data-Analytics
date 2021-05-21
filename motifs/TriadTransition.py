import numpy as np
import re
import sys
from MotifGraph import *
#from GraphAdjList import *
from StatSubGraphChange import *
#from MathFun import *
#import mathFunctions
sys.path.append("..")
from mathFunctions import *
from graphs import *


class TriadTransition:
    def __init__(self, tmpCensus, tmpEditDistanceDistr, curEditDistanceDistr, allEditDistanceFreq, KLDTriadCensus, KLDTriadEditDisDistr, edgeGraph, dataName, outputDir, time, triadFreq, transitionCnt, motifChains, allStatSubGraph, numNodes):
        self.tmpCensus = tmpCensus
        self.tmpEditDistanceDistr = tmpEditDistanceDistr
        self.curEditDistanceDistr = curEditDistanceDistr
        self.allEditDistanceFreq = allEditDistanceFreq
        self.KLDTriadCensus = KLDTriadCensus
        self.KLDTriadEditDisDistr = KLDTriadEditDisDistr

        self.edgeGraph = edgeGraph
        self.dataName = dataName
        self.outputDir = outputDir
        self.time = time
        self.triadFreq = triadFreq
        self.transitionCnt = transitionCnt
        self.motifChains = motifChains
        self.allStatSubGraph = allStatSubGraph
        self.numNodes = numNodes

    def TraidTransition(self, eg, numNode):
        self.edgeGraph = eg
        self.numNodes = numNode

        if self.edgeGraph is not None:
            self.time = len(self.edgeGraph)
            self.triadFreq = np.matrix([self.time], [16])
            self.transitionCnt = np.matrix([self.time], [16], [16])
            self.motifChains = {}
            self.dataName = ""
            self.outputDir = ""

    def getDynNetFromEdgeFile(self, fileName):
        tt = None
        try:
            br = open(fileName, "r")
            print("\t read: " + fileName)
            p = re.pattern.compile()
            m = None
            numN = 0
            t = 0

            ls = []
            for line in br:
                m = p.matcher(line)
                if m.find():
                    numN = int(m.group)
                if m.find():
                    t = int(m.group)

            br.close()
            edges = np.matrix([t], [], [])
            t = 0
            for line in br:
                m = p.matcher(line)
                while m.find:
                    ls.add(int(m.group))
                edges[t] = np.matrix([np.size(ls)/2], [2])

                for i in range(len(edges[t])):
                    edges[t][i][0] = ls.get(2 * i)
                    edges[t][i][1] = ls.get(2*i+1)
                t += 1
                ls.clear()

            while t < len(edges):
                edges[t+1] = np.matrix([0], [2])
            tt = TriadTransition(edges, numN)
            br.close()

        except ValueError:
            print("Error")

        finally:
            return tt

    def outputTriadCensus(self):
        try:
            triadCensusFile = self.outputDir + self.dataName + "TriadFreqCensus.csv"
            bw = open(triadCensusFile, "r")
            sb = ""
            for freq in traidFreq:
                sb = ""

                for f in freq:
                    sb = sb + f + "\t"
                bw.write(sb + "\n")
            bw.close()
        except ValueError:
            print("Error")

    def outputRandGraphSameAsymDyadTriadFreq(self):
        try:
            randGraphTriadFile = self.outputDir + self.dataName + "randomeGraphSameAsymDyadFreqs.csv"
            bw = open(randGraphTriadFile, "r")
            randGraphTriadDistr = []
            sb = ""
            for graph in self.edgeGraph:
                sb = ""
                mg = MotifGraph(self.numNodes, graph, True)
                randGraphTriadFile = mg.getTriadCountFromRandomGraphWSameAsymDyads()
                for d in randGraphTriadFile:
                    sb = sb + d + "\t"
                bw.write(sb + "\n")
            bw.close()
        except ValueError:
            print("Error")

    def outputRandGraphSameDyadTriadFreq(self):
        try:
            randGraphTriadFile = self.outputDir + self.dataName + "randomGraphSameDyadFreqs.csv"
            bw = open(randGraphTriadFile, "r")
            randGraphTriadDistr = []
            sb = ""
            for graph in self.edgeGraph:
                sb = ""
                mg = MotifGraph(self.numNodes, graph, True)
                randGraphTriadDistr = mg.getTriadCountFromRandomGraphWSameAsymDyads()
                for d in randGraphTriadDistr:
                    sb = sb + d + "\t"
                bw.write(sb + "\n")
            bw.close()

        except ValueError:
            print("Error")
    def outputRandGraphSameDyadTriadDistr(self):
        try:
            randGraphTriadFile = self.outputDir + self.dataName + "randomGraphSameDyadDistrs.csv"
            bw = open(randGraphTriadFile, "r")
            randGraphTriadDistr = []
            sb = ""

            for graph in self.edgeGraph:
                sb = ""
                mg = MotifGraph(self.numNodes, graph, True)
                randGraphTriadDistr = mg.getTriadDistrFromRandomGraphWSameDyads()
                for d in randGraphTriadDistr:
                    sb = sb + d + "\t"
                bw.write(sb + "\n")
            bw.close()

        except ValueError:
            print("Error")

    def outputAllTransitionMatrices(self):
        try:
            tranMtrFile = self.outputDir + self.dataName + "triadTransitionCountMatrix.csv"
            bw = open(tranMtrFile, "r")

            for i in range(1, len(self.transitionCnt)):
                for tran in self.transitionCnt[i]:
                    for n in tran:
                        bw.write(n + "\t")
                    bw.write("\n")

        except ValueError:
            print("Error")

    def outputAllTransitionMatrices(self):
        try:
            tranMtrFile = self.outputDir + self.dataName + "traidTransitionCountMatrix.csv"
            bw = open(tranMtrFile, "r")

            for i in range(1, len(self.transitionCnt)):
                for tran in self.transitionCnt[i]:
                    for n in tran:
                        bw.write(n + "\t")
                bw.write("\n")
            bw.close()

        except ValueError:
            print("Error")

    def outputSplitedGraphs(self, mappings, subgraphSize):
        filenames = []
        bws = []
        try:
            for i in range(len(filenames)):
                filenames[i] = self.outputDir + "subGraph" + i + ".txt"
                if subgraphSize[i] > 10:
                    bws[i] = open(filenames[i], "r")
                    bws[i].write(subgraphSize[i] + "\t" + self.time)
                    bws[i].write("\n")

            for graph in self.edgeGraph:
                for edge in graph:
                    if bws[mappings[edge[0]][0]] is None:
                        continue
                    bws[mappings[edge[0]][0]].write(mappings[edge[0]][1] + "\t")
                    bws[mappings[edge[1]][0]].write(mappings[edge[1]][1] + "\t")
                for i in range(len(bws)):
                    if bws[i] is None:
                        continue
                    bws[i].write("\n")
            for i in range(len(filenames)):
                if bws[i] is None:
                    continue
                bws[i].close()

        except ValueError:
            print("Error")

    def outputKLDivergenceOFTriadCensus(self):
        try:
            tranMtrFile = self.outputDir + self.dataName + "triadCensusKLDivergence.csv"
            bw = open(tranMtrFile, "r")
            for kld in self.KLDTriadCensus:
                bw.write(kld + "\t")
            bw.close()
        except ValueError:
            print("Error")

    def outputKLDDivergenceOFEditDistance(self):
        try:
            file = self.outputDir + self.dataName + "triadEditDistanceKLDivergence.csv"
            bw = open(file, "r")
            for kld in self.KLDTriadEditDisDistr:
                bw.write(kld + "\t")
            bw.close()
        except ValueError:
            print("Error")

    def outputAllEditDistanceDistribution(self):
        try:
            file = self.outputDir + self.dataName + "triadAllEditDistanceFreq.csv"
            bw = open(file, "r")
            for dist in self.allEditDistanceFreq:
                for i in dist:
                    bw.write(i + "\t")
                bw.write("\n")
            bw.close()
        except ValueError:
            print("Error")

    def outputMotifChainAll3NodeSubGraphs(self):
        try:
            subGraphFile = self.outputDir + self.dataName + "3NodeSubgraphMotifChain.csv"
            br = open(subGraphFile, "r")
            ssgc = None
            sb = ""
            for s in self.allStatSubGraph.keys():
                ssgc = self.allStatSubGraph.get(s)
                for i in s:
                    sb = sb + i + "\t"
                sb += ssgc.nonNullTime
                for i in ssgc.editDisDistr:
                    sb = "\t" + i
                br.write(sb + "\n")
            br.close()
        except ValueError:
            print("Error")

    def getStatOfSubgraph(self, ar):
        res = StatSubGraphChange()
        StatSubGraphChange.nonNullBeg = -1
        StatSubGraphChange.nonNullEnd = -1
        pre = None
        for mcn in ar:
            res.calChange(pre, mcn)
            pre = mcn

        if pre is not None and (StatSubGraphChange.nonNullEnd < StatSubGraphChange.nonNullBeg) and kpre.motifType != 0:
            res.nonNullTime += self.time - StatSubGraphChange.nonNullBeg
        return res

    def getAllSubGraphChanges(self):
        res = {}
        StatSubGraphChange.totalTime = self.time
        for key in self.motifChains.keys():
            res.put(key, getStatOfSubgraph(self.motifChains.get(key)))
        self.allStatSubGraph = res  #TODO: Create a self method
        return res

    def initialTmpVar(self):
        if self.KLDTriadCensus is not None:
            self.KLDTriadCensus = []
        else:
            self.KLDTriadCensus = []
        if self.KLDTriadEditDisDistr is not None:
            self.KLDTriadEditDisDistr = []
        else:
            self.KLDTriadEditDisDistr = []

    def countTraids(self, graph, census, time):
        res = {}
        if census is not None or len(census) != 16:
            print("census lenght should be 16 for triads")
            return res

        subgraph = [None] * 3
        iodegrees = [None] * 3
        triadHashKey = -1
        motifType = -1
        subGraphKey = None

        for e in graph.edges:
            edgeKeyToSubgraphArray(e, subgraph, 0, 1)
            for subgraph[2] in range(graph.numNode):
                if subgraph[2] == subgraph[0] or subgraph[2] == subgraph[1]:
                    continue
                subGraphKey = getSubgraphkey(subgraph)

                if subGraphKey in res:
                    continue
                triadHashKey = subGraphToTriadHAshKey(subgraph, graph, iodegrees)
                if traidHashKey not in traidCodeIdx:
                    print("error! no such hashKey found!")
                    return res

                traidChain = []
                res.put(subGraphKey, traidChain)
                motifType = triadCodeIdx.get(triadHashKey)
                motifType = traidCodeIdx.get(traidHashKey)
                triadChain.add(MotifChainNode(time, motifType))
                census[motifType] += 1

        motifType = graph.numNode
        motifType = motifType * (motifType - 1) * (motifType - 2) / 6
        for i in range(1, len(census)):
            motifType -= census[i]
        census[0] = motifType
        return res

    def updateTriadsWNextNetSnapshot(self, preGraph, curGraph, census, curTime, allMotifChain, subgraph,
                                    iodegrees, tranMtr):
        if census is None or len(census) != 16:
            print("census length should be 16 for triads")
            return allMotifChain
        if tranMtr is None:
            print("transition matrix need to be initialized")
            return allMotifChain
        self.tmpCensus = cloneCensus(self.tmpCensus, census)
        if self.curEditDistanceDistr is None:
            self.curEditDistanceDistr = [None] * 7
        else:
            np.zeros(self.curEditDistanceDistr)
        res = {}
        if subgraph is None:
            subgraph = [None] * 3
        if iodegrees is None:
            iodegrees = [None] * 3

        changingEdges = None
        changingEdges = getChaingEdges(preGraph, curGraph, changingEdges)
        subGraphKey = None
        triadChain = None
        for i in range(16):
            tranMtr[i][i] = census[i]
        for e in changingEdges:
            edgeKeyToSubgraphArray(e, subgraph, 0, 1)
            for subgraph[2] in range(curGraph.numNode):
                if subgraph[2] == subgraph[0] or subgraph[2] == subgraph[1]:
                    continue
                subGraphKey = getSubgraphkey(subgraph)
                if triadHashKey not in traidCodeIdx:
                    print("error! no such hashKEy found!")
                    return allMotifChain
                motifType = triadCodeIdx.get(triadHashKey)
                res.put(subGraphKey, MotifChainNode(curTime, motifType))
                census[motifType] += 1

        for subG in res.keys():
            if subG in allMotifChain:
                triadChain = allMotifChain.get(subG)
                motifType = triadChain.get(np.size(triadChain) - 1).motifType
                census[motifType] -= 1
                tranMtr[motifType][motifType] -= 1
                triadChain.add(res.get(subG))
                tranMtr[motifType][res.get(subG).motifType] += 1
                self.curEditDistanceDistr[TRAID_EDIT_DISTANCE[motifType][res.get(subG).motifType]] += 1
            else:
                triadChain = []
                triadChain.add(res.get(subG))
                allMotifChain.put(subG, triadChain)
                census[0] -= 1
                tranMtr[0][0] -= 1
                tranMtr[0][res.get(subG).motifType] += 1
                self.curEditDistanceDistr[TRAID_EDIT_DISTANCE[0][res.get(subG).motifType]] += 1
        motifType = curGraph.numNode
        motifType = motifType * (motifType - 1) * (motifType - 2) / 6
        for i in range(1, len(self.curEditDistanceDistr)):
            motifType -= self.curEditDistanceDistr[i]
        self.curEditDistanceDistr[0] = motifType
        self.KLDTriadCensus.add(KLDiversionFromFreqWithDayesPrior(self.tmpCensus, census))
        if self.tmpEditDistanceDistr is None:
            self.tmpEditDistanceDistr = [None] * 7
        else:
            self.KLDTriadEditDisDistr.add(KLDiversionFromFreqWithDayesPrior(self.tmpEditDistanceDistr, self.curEditDistanceDistr))
        self.tmpEditDistanceDistr = cloneCensus(self.tmpEditDistanceDistr, self.curEditDistanceDistr)
        MathFun.cloneCensus(allEditDistaceFreq[curTime], self.curEditDistanceDistr)
        return allMotifChain

    def updateTriadFreqAtT(self, t, pre, cur, preSubgraphType):
        curSubgraphType = {}
        subgraph = [None] * 3
        iodegrees = [None] * 3
        triadHashKey = -1
        motifType = -1
        preType = -1
        subGraphKey = None
        edgeNums = [np.size(cur.edges()), np.size(pre.edges), 0]
        for e in cur.edges:
            if e in pre.edges:
                pre.edges.remove(e)
            else:
                edgeKeyToSubgraphArray(e, subgraph, 0, 1)
                for subgraph[2] in range(cur.numNode):
                    if subgraph[2] == subgraph[0] or subgraph[2] == subgraph[1]:
                        continue
                    subGraphKey = getSubgraphkey(subgraph)
                    if subGraphKey in curSubgraphType:
                        continue
                    traidHashKey = subGraphToTriadHashKey(subgraph, cur, iodegrees)
                    motifType = traidCodeIdx.get(triadHashKey)
                    triadHashKey = subGraphToTriadHashKey(subgraph, cur, iodegrees)
                    motifType = traidCodeIdx.get(traidHashKey)
                    self.triadFreq[t][motifType] += 1
                    curSubgraphType.put(subGraphKey, motifType)
                    if subGraphKey in preSubgraphType:
                        preType = preSubgraphType.get(subGraphKey)
                        preSubgraphType.remove(subGraphKey)
                    else:
                        preType = 0
                    self.transitionCnt[t][preType][motifType] += 1
                    self.transitionCnt[t][preType][preType] -= 1
        nullSubgraph = []
        edgeNums[2] = np.size(pre.edges)
        edgeNums[1] -= np.size(pre.edges)
        for e in pre.edges:
            edgeKeyToSubgraphArray(e, subgraph, 0, 1)
            for subgraph[2] in range(cur.numNode):
                if subgraph[2] == subgraph[0] or subgraph[2] == subgraph[1]:
                    continue
                subGraphKey = getSubgraphkey(subgraph)
                if subGraphKey in curSubgraphType or subGraphKey in nullSubgraph:
                    continue
                triadHashKey = subGraphToTriadHashKey(subgraph, cur, iodegrees)
                preType = preSubgraphType.get(subGraphKey)
                motifType = triadCodeIdx.get(traidHashKey)
                if motifType != 0:
                    curSubgraphType.put(subGraphKey, motifType)
                else:
                    nullSubgraph.add(subGraphKey)
                preSubgraphType.remove(subGraphKey)
                self.triadFreq[t][motifType] += 1
                self.transitionCnt[t][preType][motifType] += 1
                self.transitionCnt[t][preType][preType] -= 1

        if t > 0:
            for i in range(len(self.triadFreq[t])):
                self.transitionCnt[t][i][i] += self.triadFreq[t-1][i]
        else:
            self.transitionCnt[t][0][0] += int(cur.numNode * (cur.numNode - 1) / 2 * (cur.numNode - 2) / 3)
        motifType = cur.numNode
        motifType = int(cur.numNode * (cur.numNode - 1) / 2 * (cur.numNode - 2) / 3)
        for i in range(1, len(self.triadFreq[t])):
            motifType -= self.triadFreq[t][i]
        self.triadFreq[t][0] = motifType
        curSubgraphType.update(preSubgraphType)
        return curSubgraphType

    def countTriadFreqAtT(self, t, graph, preSubgraphType):
        curSubgraphType = {}
        subgraph = [None] * 3
        iodegrees = [None] * 3
        triadHashKey = -1
        motifType = -1
        preType = -1
        subGraphKey = None
        for e in graph.edges:
            edgeKeyToSubgraphArray(e, subgraph, 0, 1)
            for subgraph[2] in range(graph.numNode):
                if subgraph[2] == subgraph[0] or subgraph[2] == subgraph[1]:
                    continue
                subGraphKey = getSubgraphkey(subgraph)
                if subGraphKey in curSubgraphType:
                    continue

                triadHashKey = traidCodeIdx.get(subgraph, graph, iodegrees)
                motifTYpe = traidCodeIdx.get(triadHashKey)
                curSubgraphType.put(subGraphKey, motifType)
                self.triadFreq[t][motifType] += 1
                if subGraphKey in preSubgraphType:
                    preType = preSubgraphType.get(subGraphKey)
                    preSubgraphType.remove(subGraphKey)
                else:
                    preType = 0
                self.transitionCnt[t][preType][motifType] += 1
                self.transitionCnt[t][preType][preType] -= 1

        for val in preSubgraphType.values():
            self.transitionCnt[t][val][0] += 1
            self.transitionCnt[t][val][val] -= 1

        if t > 0:
            for i in range(len(self.triadFreq[t])):
                self.transitionCnt[t][i][i] += self.triadFreq[t - 1][i]
        else:
            self.transitionCnt[t][0][0] += int(graph.numNode * (graph.numNode - 1) / 2 * (graph.numNode - 2) / 3)
        motifType = graph.numNode
        motifType = motifType * (motifType - 1) * (motifType - 2) / 6
        for i in range(1, len(self.triadFreq[t])):
            motifType -= self.triadFreq[t][i]
        self.triadFreq[t][0] = motifType
        return curSubgraphType

    def main(args):
        print("Working Directory = " + System.getProperty("user.dir"))
        filename = "test.txt"
        self.dataName = ""
        if args is not None and len(args) > 0:
            filename = args[0]
            if len(args) > 1:
                self.dataName = args[1]
        tt = TriadTransition.getDynNetFromEdgeFile(filename)
        tt.dataName = self.dataName
        initialTmpVar()
        TriadTransition.allEditDistanceFreq = np.matrix([tt.time][7])
        initializeTriadCode()
        pre = MotifGraph(tt.numNodes, tt.edgeGraph[0], True)
        cur = None

        tt.motifChains = countTriads(pre, tt.triadFreq[0], 0)
        subgraph = [None] * 3
        iodegrees = [None] * 3

        for t in range(1, len(tt.time)):
            cloneCensus(tt.triadFreq[t], tt.triadFreq[t-1])
            cur = MotifGraph(tt.numNodes, tt.edgeGraph[t], True)
            updateTriadWNextNetSnapshot(pre, cur, tt.triadFreq[t], t, tt.motifGraph,
                                        subgraph, iodegrees, tt.transitionCnt[t])
            pre = cur
        tt.outputAllTransitionMatrices()
        tt.outputKLDivergenceOfTriadCensus()
        tt.outputKLDivergenceOfEditDistance()
        tt.outputAllEditDistanceDistribution()
        print("done")

        return



