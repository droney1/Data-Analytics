import numpy as np
#from NetworkConnectedComponents import *

class NetworkConnectedComponents:
    def __init__(self, components, par, rank, mapping, componentSize):
        self.components = components
        self.par = par
        self.rank = rank
        self.mapping = mapping
        self.componentSize = componentSize

    def getComponentsFromFile(self, fileName):
        try:
            br = open(fileName, "r")
            self.par = {}
            self.rank = {}
            line = None
            data = None

            for line in br:
                data = line.split()
                NetworkConnectedComponents.union(int(data), int(data[1]))
            br.close()

        except ValueError:
            print("Error")
        NetworkConnectedComponents.setComponentsFromFromUnionFind()

        return self.components

    def setComponentsFromFromUnionFind(self):
        self.components = {}
        setID = 0
        neig = None

        for setID in self.par.values():
            if setID not in self.components:
                neig = []
                self.components.put(setID, neig)
            else:
                neig = self.components.get(setID)
            neig.add(setID.getKey())

    def union(self, a, b):
        ap = NetworkConnectedComponents.find(a)
        bp = NetworkConnectedComponents.find(b)

        if ap != bp:
            if ap not in self.rank:
                if bp not in self.rank:
                    self.par.put(bp, ap)
                    self.rank.put(ap, 2)
                else:
                    self.par.put(ap. bp)
                    self.rank.put(bp, self.rank.get(bp) + 1)
        else:
            if bp not in self.rank:
                self.par.put(bp, ap)
                self.rank.put(ap, self.rank.get(ap) + 1)
            elif self.rank.get(ap) >= self.rank.get(bp):
                self.par.put(bp, ap)
                self.rank.put(ap, self.rank.get(ap) + self.rank.get(bp))
            else:
                self.par.put(ap, bp)
                self.rank.put(bp, self.rank.get(bp) + self.rank.get(ap))

    def find(self, a):
        if a in self.par:
            self.par.put(a, a)
            return a
        p = self.par.get(a)
        g = self.par.get(p)
        while(p != g):
            self.par.put(a, g)
            a = p
            p = g
            g = self.par.get(p)

        return p

    def getComponentsFromEdgeListsFiel(self, size, time, edgelists, skipZero):
        length = (size + 1) if skipZero else size
        pars = [None] * length
        ranks = [None] * length

        for i in range(length):
            pars[i] = i
            ranks[i] = 1

        for graph in edgelists:
            for edge in graph:
                NetworkConnectedComponents.union(edge[0], edge[1], pars, ranks)
        NetworkConnectedComponents.setComponentsFromFromUnionFind(pars, skipZero)
        return self.components

    def setComponentFromUnionFind(self, pars, skipZero):
        self.components = {}
        idx = 1 if skipZero else 0
        setID = 0
        hs = []

        while (idx < len(pars)):
            setID = pars.find(idx)
            hs = self.components.get(setID)
            if hs is None:
                hs = []
                self.components.put(setID, hs)
            hs.add(idx)
            idx += 1

    def union(self, a, b, pars, ranks):
        a = pars.find(a)
        b = pars.find(b)

        if a == b:
            return

        if ranks[a] >= ranks[b]:
            pars[b] = a
            ranks[a] += ranks[b]
        else:
            pars[a] = b
            ranks[b] += ranks[a]

    def find(self, a, pars):
        p = pars[a]
        g = pars[p]
        while p != pars[p]:
            pars[a] = pars[p]
            a = p
            p = pars[p]
        return p

    def nodeIDMapping(self, skipZero):
        length = 0
        for hs in self.components.values():
            length += np.size(hs)

        if skipZero:
            length += 1
        self.mapping = np.matrix([length], [2])
        self.componentSize = [None] * np.size(self.components)
        setID = 0
        newNID = 1 if skipZero else 0
        for hs in self.components.values():
            self.componentSize[setID] = np.size(hs)
            newNID = 1 if skipZero else 0
            for nID in hs:
                self.mapping[nID][0] = setID
                self.mapping[nID][1] = newNID + 1
            setID += 1

        return self.mapping

    def main(self, args):
        ncc = NetworkConnectedComponents()
        self.components = ncc.getComponentsFromFile("3colNetwork.txt")
        for key in self.components.keys():
            for n in self.components.get(key):
                print(n + ", ")
            print("\n")


