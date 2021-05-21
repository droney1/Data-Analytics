from BasicGraph import *

class GraphAdjList(BasicGraph):
    def __init__(self, directed, size):
        self.directed = directed
        self.size = size
        self.nodes = {}

    def GraphAdjList(self, s, dir, edges):
        self.size = s
        self.directed = dir
        self.nodes = {}
        tmpSet = set()

        for edge in edges:
            if edge[0] in self.nodes:
                self.nodes.get(edge[0]).add(edge[1])
            else:
                tmpSet = set()
                tmpSet.add(edge[1])
                self.nodes.put(edge[0], tmpSet)

        if not self.directed:
            for edge in edges:
                if edge[1] in self.nodes:
                    self.nodes.get(edge[1]).add(edge[0])
                else:
                    tmpSet = set()
                    tmpSet.add(edge[0])
                    self.nodes.put(edge[1], tmpSet)

        if self.size == -1:
            self.size = self.size(self.nodes)

    def getMotifFreq(self, dir, numNode):
        self.directed = dir
        if numNode == 3:
            if self.directed:
                return triadFreq()
        return None

    def triadFreq(self):
        triadFreq = []
        for node in self.nodes.keys():
            for u in self.nodes.get(node):
                for v in self.nodes.get(node):
                    if v <= u or (u in self.nodes and self.nodes.get(u).contains(v)) or (v in self.nodes and self.nodes.get(v).contains(u)) and node > v:
                        continue;
                    else:
                        #TODO: Count triads
                        pass

                    return triadFreq

    def getNodeMotifFreq(self, motifSize):
        #TODO: Auto-generated method stub
        return None

