import sys

import numpy as np
import os
import math
'''
from graphs.GraphFactory import *
from graphs.GraphIO import *
from graphs.GraphPropertiesToolBox import *
'''
import time
from graphs import *
from randomgraph import *

class StaticGraphExperiment:
    def __init__(self):
        pass
    def getExperimentsFromCfgFile(self, cfg):
        res = np.matrix([], [])
        ls = []
        try:
            br = open(cfg, "r")
            for line in br:
                if line.startswith("//") or line.startswith("#") or len(line) == 0:
                    continue
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

    def executeCommand(self, graph, command, outDir, outFile, fIdx):
        folder = os.path.join(outDir)

        if not os.path.exists(folder):
            os.mkdir(folder)
        fType = ".txt"
        if fIdx > 0:
            fType += fIdx
        if command[0] == "conversion":
            if len(command) > 1 and command[1] == "nodeList":
                output = np.matrix([1], [])
                output[0] = edgesToNodeList(graph.edges)
                print("\toutput:" + outDir + "/" + outFile + "NodeList" + fType)
                outputMatrix(outDir + "/" + outFile + "NodeList" + fType, output)
        elif len(command) >= 3 and command[1] == "generateRandomGraph":
            rg = None
            if command[0] == "MANPairModel":
                rg = getRandomGraphW_MAN_Pair(graph)
            elif command[0] == "numNodeEdge":
                rg = getRandomGraphWNumNodeEdge(graph)
            elif command[0] == "reciprocalInOutDegree":
                rg = getRandomGraphReciprocalAndInOutDegreeFromGraphOfEdgeArray(graph)
            elif command[0] == "jointInOutDegree":
                rg = getRandomGraphWSameJointIODegree(graph)
            elif command[0] == "cfgModel":
                rg = getRandomGraphLoopAndMultiEdgeWSameJointIODegree(graph)
            repeat = int(command[2])
            print("\n\t[Operation]: generate ", repeat, " randpm graph ", command[0], " \n")
            outputM = np.matrix([], [])
            for i in range(repeat):
                outputM = rg.generateRandomGraph().edges
                print("\n\t***", outDir, "/", outFile, "_RandomGraph" + i + "" + fType)
                outputMatrix(outDir + "/" + outFile + "_" + command[0] + "_RandomGraph" + i + "" + fType, outputM)
        elif command[0] == "motifCensus" and len(command) > 1:
            print("\n\t")
            mSize = int(command[1])
            if mSize == 3:
                time = time.time() * math.pow(10, 6)
                freq = graph.getMotifFreq(mSize)
                time = (time.time() * math.pow(10, 6)) - time
                outputM = np.matrix([1], [16])
                for i in range(16):
                    outputM[0][i] = freq[i]
                print("[output]: " + outDir + "/" + outFile + "TriadCensus", fType)
                outputM[0] = {time}
                outputMatrix(outDir + "/" + outFile + "TriadCensus_time" + fType, outputM)
            elif mSize == -3:
                freq = graph.getMotifFreq(mSize)
                outputM = np.matrix([1], [len(freq)])
                for i in range(len(freq)):
                    outputM[0][i] = freq[i]
                print("[output]: ", outDir, "/", outFile, "TriadCensus", fType)
                outputMatrix(outDir + "/" + outFile + "TriadCensus" + fType, outputM)
        elif command[0] == "motifNodeCensus" and len(command) > 1:
            print("\n\t")
            mSize = int(command[1])
            if mSize == 3:
                time = time.time() * math.pow(10, 6)
                freq = graph.getNodeMotifFreq(mSize)
                time = (time.time() * math.pow(10, 6)) - time
                outputM = np.matrix([len(freq)], [17])
                for i in range(len(outputM)):
                    for j in range(len(outputM[0])):
                        outputM[i][j] = freq[i][j]
                print("[output]: ", outDir, "/", outFile, "Node_TriadCencus", fType)
                outputMatrix(outDir+"/"+outFile + "Node_TriadCencus"+fType, outputM)
                timeM = np.matrix([1], [1])
                timeM[0][0] = time
                outputMatrix(outDir+"/"+outFile + "Node_TriadCencus_time"+fType, timeM)
        elif command[0] == "jointInOutDegree":
            if command[1] == "ExpectedTriadFreqOptTime" and len(command) >= 4:
                print("\n\t[Operation]:Analogical computation random graph and count motif frequency")
                motifSize = int(command[2])
                opt = 0
                if len(command) >= 5:
                    opt = int(command[4])
                repeat = int(command[3])
                runTimes = [repeat]
                outputM = None
                starttime = 0
                rgjoid = getRandomGraphWSameJointIODegree(graph)
                outputM = np.matrix([1], [])
                for i in range(repeat):
                    starttime = time.time() * math.pow(10, 6)
                    outputM[0] = rgjoid.getMotifFreq(motifSize, opt)
                    runTimes[i] = (time.time() * math.pow(10, 6)) - starttime
                outputMatrix(outDir+"/"+outFile + command[1] +"opt"+ opt+ ""+fType, outputM)
                outputM[0] = runTimes
                outputMatrix(outDir +"/" + outFile + command[1] +"opt"+ opt+ "_time"+fType, outputM)
        elif command[1] == "sampleGraphMotifFreq" and len(command) >= 4:
            print("\n\t[Operation]:Simulation to generate multiple random graph and count motif frequency")
            rgjiod = None
            if len(command) >= 5 and command[4] == "allowLoopAndMultiEdges":
                rgjiod = getRandomGraphLoopAndMultiEdgeWSameJointIODegree(graph)
                outFile += "loopMultiedge"
            else:
                rgjiod = getRandomGraphWSameJointIODegree(graph)
                repeat = int(command[3])
                motifSize = int(command[2])
                starttime = time.time() * math.pow(10, 6)
                outputM = rgjiod.getMotifFreqFromSampledGraphs(motifSize, repeat)
                time = (time.time() * math.pow(10, 6)) - starttime
                outputMatrix(outDir+"/"+outFile+"sampleGraphMotifFreq"+fType, outputM)
                outputM = np.matrix([], {repeat, time})
                outputMatrix(outDir+"/"+outFile+"sampleGraphMotifFreq_time"+fType, outputM)
        elif command[1] == "getRandomGraphInfo":
            print("\n\t[Operation]:Output Graph Info")
            last = "Info" + fType
            if len(command) >= 3 and command[2] == "removeNullNode":
                print("\n reduce network size")
                graph = graph.removeNullNodes()
                last = "NoNullNode" + last
            outputM = np.matrix([], [])
            rgjiod = getRandomGraphWSameJointIODegree(graph)
            outputM = rgjiod.getGraphInfo()
            outputMatrix(outDir+"/"+outFile + last, outputM)
        elif command[1] == "outputConnectComponents" and len(command) > 3:
            print("\t\t[Operation]: obtain Larges Components")
            try:
                f = os.path.join(command[2])
                if not os.path.exists(f):
                    os.mkdir(f)
                compSize = int(command[3])
                tEdges = obtainConnectComponentEdges(graph.edges, compSize)
                for i in range(len(tEdges)):
                    bw = open(f+"/"+ outFile+"Comp"+i+""+fType, "w")
                    print("output file: ", f, "/", outFile, "Comp", i, "", fType)
                    bw.write(tEdges[i][0][0], "/t", tEdges[i][0][1])
                    for j in range(1, len(tEdges[i])):
                        bw.newlines()
                        bw.write(tEdges[i][j][0], "\t", tEdges[i][j][1])
                    bw.close()
            except ValueError:
                print("error")
        elif command[1] == "ExpectedTriadFreq" and len(command) >= 3:
            print("\n\t[Operation]:Analogical computation random graph with joint in/out degree and count motif frequency")
            motifSize = int(command[2])
            opt = 0
            repeat = int(command[3])
            runTimes = [repeat]
            outputM = np.matrix([], [])
            starttime = 0
            rgjiod = getRandomGraphWSameJointIODegree(graph)
            outputM = np.matrix([1], [])
            for i in range(repeat):
                starttime = time.time() * math.pow(10, 6)
                outputM[0] = rgjiod.getMotifFreq(motifSize, opt)
                runTimes[i] = (time.time() * math.pow(10, 6)) - starttime
            outputMatrix(outDir+"/"+outFile + command[1] +"opt"+ opt+ ""+fType, outputM)
            outputM[0] = runTimes
            outputMatrix(outDir +"/" + outFile + command[1] +"opt"+ opt+ "_time"+fType, outputM)
        elif command[0] == "reciprocalInOutDegree":
            if command[1] == "sampleGraphMotifFreq" and len(command) >= 4:
                print("\n\t[Operation]:Simulation to generate multiple random graph and count motif frequency")
                rgriod = None
                loop = False
                if len(command) >= 5 and command[4] == "allowLoopAndMultiEdges":
                    rgriod = getRandomGraphReciprocalAndInOutDegreeFromGraphOfEdgeArray(graph)
                    loop = True
                else:
                    rgriod = getRandomGraphReciprocalAndInOutDegreeFromGraphOfEdgeArray(graph)
                repeat = int(command[3])
                motifSize = int(command[2])
                starttime = (time.time() * math.pow(10, 6))
                outputM = rgriod.getMotifFreqFromSampledGraphs(motifSize, repeat)
                time = (time.time() * math.pow(10, 6)) - starttime
                tmp = "sampleReciprocalInOutDegreeGraphMotifFreq"
                if loop:
                    tmp += "loopMultiedges"
                outputMatrix(outDir+"/"+outFile+tmp+""+fType, outputM)
                outputM = np.matrix([], {repeat, time})
                outputMatrix(outDir+"/"+outFile+tmp+""+fType, outputM)
        elif command[0] == "numNodeEdge":
            if command[1] == "sampleGraphMotifFreq" and len(command) >= 4:
                print("\n\t[Operation]:Simulation to generate multiple random graph with same numNode and numEdge and count motif frequency")
                rgne = None
                rgne = getRandomGraphWNumNodeEdge(graph)
                repeat = int(command[3])
                motifSize = int(command[2])
                starttime = time.time() * math.pow(10, 6)
                outputM = rgne.getMotifFreqFromSampledGraphs(motifSize, repeat)
                time = (time.time() * math.pow(10, 6)) - starttime
                outputMatrix(outDir+"/"+outFile+"sampleWNumNodeEdgeGraphMotifFreq"+fType, outputM)
                outputM = np.matrix([], {repeat, time})
                outputMatrix(outDir+"/"+outFile+"sampleWNumNodeEdgeGraphMotifFreq_time"+fType, outputM)
        elif command[1] == "ExpectedTriadFreq" and len(command) >= 4:
            motifSize = int(command[2])
            repeat = int(command[3])
            runTimes = [repeat]
            outputM = None
            starttime = 0
            rgne = getRandomGraphWNumNodeEdge(graph)
            outputM = np.matrix([1], [])
            for i in range(repeat):
                starttime = time.time() * math.pow(10, 6)
                outputM[0] = rgne.getMotifFreq(motifSize)
                runTimes[i] = (time.time() * math.pow(10, 6)) - starttime
            outputMatrix(outDir+"/"+outFile + command[1] +"WNumNodeEdge"+ ""+fType, outputM)
            outputM[0] = runTimes
            outputMatrix(outDir +"/" + outFile + command[1] +"WNumNodeEdg"+ "_time"+fType, outputM)
        elif command[0] == "MANPairModel":
            if command[1] == "sampleGraphMotifFreq" and len(command) >= 4:
                print("\n\t[Operation]:Simulation to generate multiple random graph with same MAN pair and count motif frequency")
                rgMAN = None
                rgMAN = getRandomGraphW_MAN_Pair(graph)
                repeat = int(command[3])
                motifSize = int(command[2])
                starttime = time.time() * math.pow(10, 6)
                outputM = rgMAN.getMotifFreqFromSampledGraphs(motifSize, repeat)
                outputM = np.matrix([1], [])
                for i in range(repeat):
                    starttime = time.time() * math.pow(10, 6)
                    outputM[0] = rgMAN.getMotifFreq(motifSize)
                    runTimes[i] = (time.time() * math.pow(10, 6)) - starttime
                outputMatrix(outDir+"/"+outFile + command[1] +"WMANPair"+ ""+fType, outputM)
                outputM = runTimes
                outputMatrix(outDir +"/" + outFile + command[1] +"WMANPair"+ "_time"+fType, outputM)
        elif command[1] == "getRandomGraphInfo":
            print("\n\t[Operation]:Output Graph Info")
            last = "_MANPair_Info" + fType
            if len(command) >= 3 and command[2] == "removeNullNode":
                print("\n reduce network size")
                graph = graph.removeNullNodes()
                last = "NoNullNode" + last
            outputM = np.matrix([], [])
            rgMAN = getRandomGraphW_MAN_Pair(graph)
            outputM = rgMAN.getGraphInfo()
            outputMatrix(outDir+"/"+outFile + last, outputM)

    def main(self, args):
        if len(args) < 2:
            print("need two configuration files as input:\n\t1. configfile for data file paths\n\t2. experiments to execute")
            return
        fidx = -1
        if len(args) > 2 and args[2] == "-i":
            fidx = 1
        dataFileCfg = args[0]
        expCfg = args[1]
        files = getDataFileNamesFromFileList(dataFileCfg)
        graph = None
        commands = getExperimentsFromCfgFile(expCfg)
        if len(commands) < 2 or len(commands[1]) < 2 or commands[0][0] != "expName" or commands[1][0] != "outDir":
            print("experiment configuration file format error:",
                        "\n\tThe first line should be in the format: expName experiment_name",
                        "\n\tThe second line should be in the format: outDir output_folder_for_result")
            return
        expName = commands[0][1]
        outDir = commands[1][1]
        for i in range(len(files)):
            print("Process file[", i, "]: ", files[i], "\n")
            graph = makeEdgeFraphFromFileOfEdgeList(files[i])
            for j in range(2, len(commands)):
                executeCommand(graph, commands[j],outDir+"/"+expName,
                            files[i].substring(files[i].lastIndexOf('/')+1, files[i].lastIndexOf('.')), (i+1) * fidx)

main_var = StaticGraphExperiment()
if __name__ == "__main__":
    main_var.main(sys.argv[1:])


