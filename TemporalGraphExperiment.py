import numpy as np
import os
import math
'''
from TemporalGraphWEdgeArray import *
from GraphFactory import *
from GraphIO import *
from GraphPropertiesToolBox import *
'''
from StaticGraphExperiment import *
from DataProcessing import *
from graphs import *

class TemporalGraphExperiment:
    def __init__(self):
        pass

    def getTempGraphsFromCfgFiles(self, files):
        tGraphs = TemporalGraphWEdgeArray[len(files)]
        for i in range(len(files)):
            tGraphs[i] = getTemporalGraphWEdgeArrayFromFile(files[i])
        return tGraphs

    def getExperimentsFromCfgFile(self, cfg):
        res = np.matrix([], [])
        ls = []
        try:
            br = open(cfg, "r")
            for line in br:
                if line.startsWith("#") or line.startsWith("//") or line.length() == 0:
                    ls.add(line.split())
            res = np.matrix([np.size(ls)], [])
            idx = 0
            for l in ls:
                res[++idx] = l
            br.close()
        except ValueError:
            print("error")
            res = np.matrix([0], [1])
        return res

    def main(self, args):
        if len(args) < 2:
            print("need two configuration files as input:\n\t1. configfile for data file paths\n\t2. experiments to execute")
            return
        dataFileCfg = args[0]
        expCfg = args[1]
        files = getDataFileNamesFromFileList(dataFileCfg)
        tGraph = None
        commands = getExperimentsFromCfgFile(expCfg)

        if len(commands[0]) < 2 or len(commands[1]) < 2 or commands[0][0] != "expName" or commands[1][0] != "outDir":
            print("experiment configuration file format error:",
                        "\n\tThe first line should be in the format: expName experiment_name",
                        "\n\tThe second line should be in the format: outDir output_folder_for_result")
            return
        expName = commands[0][1]
        outDir = commands[1][1]

        for i in range(len(files)):
            print("processing file[", i, "]: ", files[i], "\n")
            tGraph = getTemporalGraphWEdgeArrayFromFile(files[i])
            for j in range(2, len(commands)):
                if len(commands[j]) > 1 and commands[j][0] == "static" and commands[j][1] == "convertStaticFromSNAPData":
                    folder = os.path.join(outDir + "/" + expName)
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                    sFileName = outDir + "/" + expName + "/" + files[i][files[i].rindex('1/') + 1 : files[i].rindex('.')]
                    convertTemporalNetToStaticNet(files[i], sFileName + "_Static.txt")
                    break
                else:
                    executeCommand(tGraph, commands[j], outDir + "/" + expName, files[i][files[i].rindex('/') + 1 : files[i].rindex('.')])
                    convertTemporalNetToStaticNet(files[i], sFileName + "_Static.txt")
                    break
            else:
                executeCommand(tGraph, commands[j], outDir + "/" + expName, files[i][files[i].rindex('/') + 1 : files[i].rindex('.')])

    def executeCommand(self, g, command, outDir, outFile0):
        if len(command) >= 2 and command[0] == "snapshot":
            snapshotId = int(command[1])
            if snapshotId >= g.time():
                return
            folder = os.path.join(outDir)
            if not os.path.exists(folder):
                os.mkdir(folder)
            low, high = 0, g.time()
            if snapshotId > -1:
                low = snapshotId
                high = snapshotId + 1
            if len(command) > 2 and command[2] == "convertStatic":
                print("\n\t[Operation]: convert to static network \n")
                edges = getStaticEdgesFromFromSnapshots(g.edges, low, high)
                edges.sort()
                outputMatrix(outDir + "/" + outFile0 + "_static.txt", edges)
                return
            for snapshotId in range(low, high):
                graph = g.getSnapshot(snapshotId)
                graph = graph.removeNullNodes()
                outFile = outFile0 + command[0] + snapshotId
                rgm = None
                if command[2] == "joinInOutDegree":
                    if len(command) > 6 and command[len(command) - 1] == "allowLoopAndMultiEdges":
                        rgm = getRandomGraphLoopAndMultiEdgeWSameJointIODegree(graph)
                        outFile += "loopMultiedge"
                    else:
                        rgm = getRandomGraphWSameJointIODegree(graph)
                elif command[2] == "reciprocalInOutDegree":
                    rgm = getRandomGraphReciprocalAndInOutDegreeFromGraphOfEdgeArray(graph)
                elif command[2] == "numNodeEdge":
                    rgm = getRandomGraphWNumNodeEdge(graph)
                elif command[2] == "MANPairModel":
                    rgm = getRandomGraphW_MAN_Pair(graph)
                outFile = outFile0 + command[0] + snapshotId + command[2]
                if len(command) >= 5 and command[3] == "generateRandomGraph":
                    rg = rgm
                    repeat = int(command[4])
                    print("\n\t[Operation]: generate ", repeat, " randon graph ", command[2], " \n")
                    outputM = np.matrix([], [])
                    for i in range(repeat):
                        outputM = rg.generateRandomGraph().edges
                        outputMatrix(outDir + "/" + outFile + "_RandomGraph" + i + ".txt", outputM)
                elif command[3] == "motifCensus":
                    print("\n\t")
                    mSize = int(command[1])
                    if mSize == 3:
                        time = time.time() * math.pow(10, 6)
                        freq = graph.getMotifFreq(mSize)
                        time = (time.time() * math.pow(10, 6)) - time
                        outputM = np.matrix([1], [16])
                        for i in range(16):
                            outputM[0][i] = freq[i]
                        print("[output]: " + outDir + "/" + outFile + "TriadCencus.txt")
                        outputMatrix(outDir+"/"+outFile + "TriadCencus.txt", outputM)
                        outputM[0] = {time}
                        if len(command) > 4 and command[4] == "computeTime":
                            outputMatrix(outDir+"/"+outFile + "TriadCencus_time.txt", outputM)
                    elif command[3] == "ExpectedTriadFreq":
                        expectMotifFreq = rgm.getMtoifFreq(int(command[4]))
                        outputM = np.matrix([1], [])
                        outputM[0] = expectMotifFreq
                        outputMatrix(outDir+"/"+outFile + command[3] + ".txt", outputM)
                    elif command[3] == "SampleGraphMotifFreq":
                        repeat = int(command[5])
                        starttime = time.time() * math.pow(10, 6)
                        outputM = rgm.getMotifFreqFromSampledGraphs(int(command[4]), repeat)
                        time = (time.time() * math.pow(10, 6)) - starttime
                        outputMatrix(outDir+"/"+outFile+"sampleGraphMotifFreq.txt", outputM)
                        outputM = np.matrix([], {repeat, time})
                        outputMatrix(outDir+"/"+outFile+"sampleGraphMotifFreq_time.txt", outputM)
                    elif command[3] == "ExpectedTriadFreqOptTime":
                        repeat = int(max(1, int(command[4])))
                        opt = 0
                        if len(command) > 5:
                            opt = int(command[4])
                        outputM = np.matrix([], [])
                        runTimes = [repeat]
                        starttime = 0
                        outputM = np.matrix([1], [])

                        for i in range(repeat):
                            starttime = time.time() * math.pow(10, 6)
                            outputM[0] = rgm.getMotifFreq(int(command[3]))
                            runTimes[i] = (time.time() * math.pow(10, 6)) - starttime
                        outputMatrix(outDir+"/"+outFile + command[3] +"opt"+ opt+ ".txt", outputM)
                        outputM = np.matrix([1], [])
                        outputM[0] = runTimes
                        outputMatrix(outDir +"/" + outFile + command[3] +"opt"+ opt+ "_time.txt", outputM)
                    elif command[3] == "getRandomGraphInfo":
                        last = "Info.txt"
                        rg = rgm
                        outputM = rg.getGraphInfo()
                        outputMatrix(outDir+"/"+outFile + last, outputM)
                    elif command[3] == "outputConnectComponents" and len(command) > 4:
                        try:
                            f = os.path.join(command[4])
                            if not os.path.exists(f):
                                os.mkdir(f)
                            compSize = int(command[4])
                            tEdges = obtainConnectComponentEdges(graph.edges, compSize)

                            for i in range(len(tEdges)):
                                bw = open(f+"/"+ outFile+"Comp"+i+".txt", "w")
                                bw.write(tEdges[i][0][0] + "\t" + tEdges[i][0][1])

                                for j in range(1, len(tEdges[i])):
                                    bw.newlines()
                                    bw.write(tEdges[i][j][0] + "\t" + tEdges[i][j][1])
                                bw.close()
                        except ValueError:
                            print("error")
        #Make sure else is not needed here