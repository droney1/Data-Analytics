import numpy as np
import sys
sys.path.append("..")
from randomgraph import *

class GraphIO:
    def __init__(self):
        pass
    def getDataFileNamesFromConfig(self, dataCfgFile):
        files = []
        try:
            br = open(dataCfgFile, "r")
            line = []
            lineComp = []
            nameComponents = []
            inDir = ""
            numFile = 1

            for line in br:
                if line.startswith("//") or line.startswith("#") or not line:
                    continue
                lineComp = line.split()
                if lineComp[0] == "inDir" and lineComp.length > 1:
                    inDir = lineComp[1]
                else:
                    nameComponents.add(lineComp)
                    numFile *= len(lineComp)

            idx = 0
            files = []
            files.fill(inDir + "/")
            outRepeat = 1
            inRepeat = numFile
            for comps in nameComponents:
                idx = 0
                inRepeat /= len(comps)
                for i in range(outRepeat):
                    for s in comps:
                        for j in range(inRepeat):
                            files[idx+1] += s

                outRepeat *= len(comps)

            br.close()
        except:
            print("Error")
        return files

    def getDataFileNamesFromFileList(self, fileList):
        files = []
        try:
            br = open(fileList, "r")
            ls = []
            line = []
            for line in br:
                if len(line) == 0 or line.startswith("#") or line.startswith("//"):
                    continue
                ls.append(line)
            idx = 0

            for s in ls:
                files[idx+1] = s
            br.close()
        except:
            print("Error")
        return files

    def getExperimentCommandsFromCfgFile(self, cfg):
        res = np.matrix([], [])
        ls = []
        try:
            br = open(cfg, "r")
            for line in br:
                if line.startswith("//") or line.startswith("#") or len(line) == 0:
                    continue
                ls.append(line.split())
            res = np.matrix([np.size(ls)], [])
            idx = 0
            for l in ls:
                res[idx+1] = 1
            br.close()
        except:
            print("Error")
            res = np.matrix([], [])

        return res

    def getAdjacencyMatrixFromFile(self, filename):
        m = np.matrix([], [])
        try:
            br = open(filename, "r")
            N = -1
            node = 0
            for line in br:
                if line.startswith("#") or line.startswith("//") or len(line) == 0:
                    continue
                data = line.split()
                if N == -1:
                    N = len(data)
                    m = np.matrix([N], [N])
                for i in range(N):
                    m[node][i] = int(data[i])
                node += 1
            br.close()
        except:
            print("Error")
        return m

    def getMatrixFromFile(self, filename):
        m = np.matrix([], [])
        edgeList = []
        edge = []
        try:
            br = open(filename, "r")
            for line in br:
                if line.startswith("#") or line.startswith("//") or len(line) == 0:
                    continue
                data = line.split()
                edge = []
                for i in range(len(data)):
                    edge[i] = int(data[i])
                edgeList.append(edge)
            br.close()
            m = np.matrix([np.size(edgeList)], [])
            idx = 0
            for e in edgeList:
                m[idx] = e
                idx += 1

        except:
            print("Error")

        return m

    def convertAdjacentMatrixToEdgeList(self, m):
        numEdge = 0
        for row in m:
            for i in row:
                if i == 1:
                    numEdge += 1

        edges = np.matrix([numEdge], [2])
        numEdge = 0
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] > 0 and i != j:
                    edges[numEdge][0] = i
                    edges[numEdge][1] = j
                    numEdge += 1

        return edges

    def outputMatrix(self, filename, m):
        try:
            bw = open(filename, "r")
            sb = [] #TODO: Determine how to use StringBuilder in Python
            for r in range(len(m)):
                for d in m[r]:
                    sb.append(d + "\t")
                sb.pop()
                bw.append(sb)
                sb.clear()
                if r < len(m):
                    bw.append("\n")

            bw.close()
        except:
            print("Error")

    def outputMatrix(self, filename, m):  #TODO: Determine if this function is needed
        try:
            bw = open(filename, "r")
            sb = []
        except:
            print("Error")

    def convertAdjMatFileToEdgeList(self, filename):
        m = getAdjacencyMatrixFromFile(filename)
        edges = convertAdjacentMatrixToEdgeList(m)
        adj = filename.find("_adj")
        filename = filename[0:adj] + "EdgeList.txt"
        outputMatrix(filename, edges)

    def convertStrIDToIntInFile(self, filename, isEgo):
        try:
            br = open(filename, "r")
            idx = filename.rindex('.')
            outfile = filename[0:idx] + ("Ego" if isEgo else "") + "Formated.txt"
            bw = open(outifle, "r")
            map = []
            s, t = 0, 0
            for line in br:
                if line.startswith("#") or line.startswith("//") or len(line) == 0:
                    continue
                data = line.split()
                if data[0] in map:
                    s = map.get(data[0])
                else:
                    s = np.size(map) + 1
                    map.put(data[0], s)
                if data[1] in map:
                    t = map.get(data[1])
                else:
                    t = np.size(map) + 1
                    map.put(data[1], t)
                bw.write(s + "\t" + t + "\n")

            if isEgo:
                s = np.size(map) + 1
                for i in range(map):
                    bw.write(s + "\t" + i + "\n")
            br.close()
            bw.close()
        except:
            print("Error")

    def getStaticGraphEdgesFromTemporalEdges(self, tEdges):
        edgeSet = []
        map = []
        edgeCode = -1
        for e in tEdges:
            if e[0] not in map:
                map.put(e[0], np.size(map))
            if e[1] not in map:
                map.put(e[1], np.size(map))
            edgeCode = getEdgeKey(map.get(e[0]), map.get(e[1]));
            edgeSet.add(edgeCode);

        T = np.size(edgeSet)
        edges = np.matrix([T], [])
        t = 0
        for l in edgeSet:
            edges[t] = []   #TODO: Determine what this means, probably not correct
            getEdgeFromKey(1, edges[t])
            t += 1

        return edges

    def getStaticEdgesFromEdgesFromSnapShots(self, tEdges, beg, end):
        edgeSet = []
        map = []
        edgeCode = -1
        edges = []
        for i in range(beg, end):
            edges = tEdges[i]
            for e in edges:
                if e[0] in map:
                    map.put(e[0], np.size(map))
                if e[1] in map:
                    map.put(e[1], np.size(map))
                edgeCode = getEdgeKey(map.get(e[0]), map.get(e[1]))
                edgeSet.add(edgeCode)

        T = np.size(edgeSet)
        edges = np.matrix([T], [])
        t = 0
        for l in edgeSet:
            edges[t] = []
            getEdgeFromKey(l, edges[t])
            t += 1

        return edges

    def convertTemporalNetToStaticNet(self, tFileName, sFileName):
        tempGraph = getMatrixFromFile(tFileName)
        staticGraph = getStaticGraphEdgesFromTemporalEdges(tempGraph)
        staticGraph.sort()
        print("\toutput file: " + sFileName)
        outputMatrix(sFileName, staticGraph)

    def edgesToNodeList(edges):
        res = []
        idx = 0
        for e in edges:
            res[idx] = e[0]
            idx += 1
            res[idx] = e[1]
            idx += 1

        return res

    def getDataListFromCSV(self, filename):
        res = []
        try:
            br = open(filename, "r")
            data = []
            line = ""
            for line in br:
                if line.startswith("#") or line.startswith("//") or len(line) == 0:
                    continue
                data = line.split()
                if data is None or len(data) == 0 or len(data[0]) == 0:
                    continue
                res.add(data)

            br.close()
        except:
            print("Error")

        return res

    def convertCSVFileFormatLong(self, input):
        ls = getDataListFromCSV(input)
        res = np.matrix([np.size(ls)], [])
        idx, idx2 = 0, 0
        for strs in ls: #TODO: Determine how to use a string to go through a for loop
            tmp = []
            idx2 = 0
            for s in strs:
                temp[idx2] = int(s)
                idx2 += 1
            res[idx] = tmp
            idx += 1

        return res
