import numpy as np
import os
import time
import sys
import math
'''
from motifs.TriadTransition import *
from motifs.MotifGraph import *
from graphs.GraphNodePairVal import *
from mathFunctions.MathFun import *
'''
from graphs import *
from mathFunctions import *
from motifs import *
from randomgraph import *

class ExperimentTempNetTriad:
    def __init__(self):
        pass
    def speedTest(self, configFile):
        try:
            br = open(configFile, "r")
            dataFile = br.readline()
            tt = getDynNetFromEdgeFile(dataFile)
            tt.dataName = br.readline()
            print("dataset: ", tt.dataName)
            tt.outputDir = br.readline() + "/" + tt.dataName + "/"
            outDir = os.path.join(tt.outputDir)
            if os.path.exists(outDir):
                os.mkdir(outDir)
                print("\tcreate: ", tt.outputDir)
            curSubgraphType = {}
            graphs = MotifGraph[tt.time]
            for i in range(tt.time):
                graphs[i] = MotifGraphs(tt.numNodes, tt.edgeGraph[i], True)
            begTime = time.time() * math.pow(10, 9)
            for t in range(len(tt.edgeGraph)):
                curSubgraphType = tt.countTriadFreqAtT(t, graphs[t], curSubgraphType)

            elapseTime = (time.time() * math.pow(10, 9)) - begTime
            print("\tbase line: \t\t", elapseTime)
            curSubgraphType = {}
            tt.transitionCnt = np.matrix([tt.time], [16], [16])
            tt.triadFrq = np.matrix([tt.time], [16])
            begTime = time.time() * math.pow(10, 9)
            curSubgraphType = tt.countTriadFreqAtT(0, graphs[0], curSubgraphType)

            for t in range(1, len(tt.edgeGraph)):
                curSubgraphType = tt.updateTriadFreqAtT(t, graphs[t - 1], graphs[t], curSubgraphType)

            elapseTime = (time.time() * math.pow(10, 9)) - begTime
            print("\tfast algorithm\t\t", elapseTime)
            newGraphs = GraphNodePairVal[tt.time]

            for t in range(tt.time):
                newGraphs[t] = GraphNodePairVal(tt.numNodes, True, tt.edgeGraph[t])
            begTime = time.time() * math.pow(10, 9)
            for g in newGraphs:
                g.getMotifFreq(3)
            elapseTime = (time.time() * math.pow(10, 9)) - begTime
            print("\tPinghui algorithm\t", elapseTime)
            br.close()
        except ValueError:
            print("error")

    def getMotifDistributionOfTemporalNetFromFile(self, motifSize, fileName):
        g = None
        numMotif = 0
        if motifSize == 3:
            numMotif = 16
        elif motifSize == 4:
            numMotif = 199
        try:
            br = open(fileName, "r")
            line = br.readline()
            data = line.split()
            num = int(data[0])
            T = num(data[1])
            edgeArray = np.matrix([], [])
            motifDis = np.matrix([T], [numMotif])
            for t in range(T):
                line = br.readline()
                if line is None or len(line) < 2:
                    motifDis[t] = [numMotif]
                    motifDis[t][0] = num
                    motifDis[t][0] = motifDis[t][0] * (motifDis[t][0] - 1) / 2 * (motifDis[t][0] - 2) / 3
                    continue
                data = line.split()
                edgeArray = np.matrix([len(data) / 2], [2])
                for i in range(len(edgeArray)):
                    edgeArray[i][0] = int(data[2 * i])
                    edgeArray[i][1] = int(data[2 * i + 1])
                g = GraphNodePairVal(num, True, edgeArray)
                motifDis[t] = g.getMotifFreq(motifSize)
            br.close()
            return motifDis
        except ValueError:
            print("error")
            return [0][0]

    def runExperiment(self, configFile):
        try:
            br = open(configFile, "r")
            dataFile = br.readline()
            tt = getDynNetFromEdgeFile(dataFile)
            tt.dataName = br.readline()
            tt.outputDir = br.readline() + "/" + tt.dataName + "/"
            outDir = os.path.join(tt.outputDir)
            if not os.path.exists(outDir):
                os.mkdir(outDir)
                print("\tcreate: " + tt.outputDir)
            initializeTriadCode()
            initialTmpVar()
            allEditDistanceFreq = np.matrix([tt.time], [7])
            lines = []
            for line in br:
                lines.add(line)
            computeTask(lines, tt)
            br.close()
        except ValueError:
            print("error")

    def computeTask(self, tasks, tt):
        tmpCensus = [16]
        pre = MotifGraph(tt.numNodes, tt.edgeGraph[0], True)
        cur = None
        tt.motifChains = countTraids(pre, tt.triadFreq[0], 0)
        subgraph = [3]
        iodegrees = [3]
        for t in range(1, tt.time):
            cloneCensus(tt.triadFreq[t], tt.triadFreq[t - 1])
            cur = MotifGraph(tt.numNodes, tt.edgeGraph[t], True)
            updateTriadsWNextNetSnapshot(pre, cur, tt.triadFreq[t], t, tt.motifChains, subgraph,
                                                         iodegrees, tt.transitionCnt[t])
            pre = cur
        for task in tasks:
            if task == "traidTransition":
                print(task)
                tt.outputAllTransitionMatrices()
            elif task == "triadDistribution":
                print("triadDistribution")
                tt.outputTriadCensus()
            elif task == "randomGraphSameDyadDistr":
                print("randomGraphSameDyadDistr")
                tt.outputRandGraphSameDyadTriadDistr()
            elif task == "allTriadTransitionChain":
                print("allTriadTransitionChain")
                if tt.motifChains is not None:
                    tt.getAllSubGraphChanges()
                    tt.outputMotifChainAll3NodeSubGraph()
            elif task == "randomGraphSameDyad":
                print("randomGraphSameDyadFreq")
                tt.outputRandGraphSameDyadTriadFreq()
            elif task == "randomGraphGraphSameAsymDyadFreq":
                print("randomGraphSameAsymDyadFreq")
                tt.outputRandGraphSameAsymDyadTriadFreq()
            elif task == "splitStaticComponent":
                print("splitStaticComponent")

    def defaultOperation(self):
        dataset = {"emailEU"}
        networkName = np.matrix({"emailEUDept2", "emailEUDept4", "emailEUDept1", "emailEUDept3", "emailEUAll"})
        inDir = "/nfs/pantanal/scratch1/kuntu/workspace/netMotif/transitions/experimentConfigs/"
        granName = {"Hour", "Day", "Week", "BiWeek", "FourWeek"}
        configFile = None
        for i in range(len(dataset)):
            for nn in networkName[i]:
                for j in range(1, len(granName)):
                    gn = granName[j]
                    configFile = inDir + nnn + gn + ".cfg"
                    runExperiment(configFile)

    def runSpeedTestsForDataSets(self):
        dataset = {"emailEU"}
        networkName = np.matrix({"emailEUDept2", "emailEUDept4", "emailEUDept1",  "emailEUDept3", "emailEUAll"})
        granName = {"Hour", "Day", "Week", "BiWeek", "FourWeek"}
        configFile = None
        for i in range(len(dataset)):
            for nn in networkName[i]:
                for j in range(1, granName):
                    gn = granName
                    configFile = inDir + nn + gn + ".cfg"
                    speedTest(configFile)

    def splitDataSets(self):
        dataset = {"emailEU", "collegeMsg", "mathoverflow", "askubuntu"}
        networkName = np.matrix({"emailEUDept2", "emailEUDept4", "emailEUDept1",  "emailEUDept3","emailEUAll"},
                                {"collegeMsg"},
                                {"mathoverflowA2Q", "mathoverflowC2Q", "mathoverflowC2A",  "mathoverflowAll"},
                                {"askubuntuAll","askubuntuA2Q","askubuntuC2Q","askubuntuC2A"})
        granName = {"Hour", "Day", "Week", "BiWeek", "FourWeek"}
        configFile = None
        inDir = "/nfs/pantanal/scratch1/kuntu/workspace/netMotif/transitions/experimentConfigs/"
        for i in range(len(dataset)):
            for nn in networkName[i]:
                for j in range(1, len(granName)):
                    gn = granName[j]
                    configFile = inDir + nn + gn + ".cfg"

    def motifTransitionForSetsOfData(self, config):
        try:
            br = open(config, "r")
            line = None
            motifsize = int(br.readline())
            inDir = br.readline()
            outDir = br.readline()
            line = br.readline()
            dataNames = line.split()
            line = br.readline()
            networkNames = np.matrix([len(dataNames)], [])
            tmp = line.split(";")
            for i in range(len(tmp)):
                networkNames[i] = tmp[i].split(",")
            line = br.readline()
            granularities = line.split(",")
            folder = None

            motifDists = np.matrix([], [])
            br.close()
            tmpStr, tmpfile = "", ""
            for networks in networkNames:
                for net in networks:
                    for gran in granularities:
                        folder = os.path.join(inDir + "/" + net + gran)
                        for f in os.walk(folder):
                            if os.path.isfile(f):
                                motifDists = getMotifDistributionOfTemporalNetFromFile(motifsize, folder.getAbsolutePath() + "/" + f.getName())
                                tmpStr = outDir + "/" + net + gran
                                tmpFolder = os.path.join(tmpStr)
                                if os.path.exists(tmpFolder):
                                    os.mkdir(tmpFolder)
                                print("Output Dir: ", tmpFolder.getAbsolutePath())
                                tmpfile = tmpStr + "/" + f.getName()
                                tmpfile = tmpfile.replace(".txt", ".csv")
                                bw = open(tmpfile, "w")
                                for snapshot in motifDists:
                                    for i in range(len(snapshot) - 1):
                                        bw.append(snapshot[i] + "\t")
                                    bw.append(snapshot[len(snapshot) - 1] + "\n")
                                bw.close()
        except ValueError:
            print("error")

    def addAllFiles(self, folder, ls):
        if os.path.isfile(folder):
            ls.add(folder.getName())
        else:
            folderName = folder.getName()
            for f in os.walk(folder):
                if os.path.isfile(f):
                    ls.add(folderName + "/" + f.getName())
                elif os.path.isdir(f):
                    addAllFiles(f, ls)
    def main(self, args):
        initializeTriadCode()
        initialTmpVar()
        configFile = None
        if len(args) > 0:
            configFile = args[0]
            if args[0] == "speedTest":
                if len(args) > 1:
                    speedTest(args[1])
                else:
                    runSpeedTestsForDataSets()
            elif args[0] == "splitDataSets":
                splitDataSets()
            elif args[0] == "motifTransitions":
                if len(args) > 1 and args[1] is not None:
                    motifTransitionForSetsOfData(args[1])
            else:
                runExperiment(configFile)
        else:
            print("config file is not specified, run operation on default data sets")
            triadDis = getMotifDistributionOfTemporalNetFromFile(3, "test.txt")
            for dis in triadDis:
                for i in dis:
                    print(i + "\t")
                    print("\n")

main_var = ExperimentTempNetTriad()
if __name__ == "__main__":
    main_var.main(sys.argv[1:])





