import sys

import numpy as np
import random

class RandGraphGenerator:
    def __init__(self):
        pass

    def generateRandGraph(self, size, avgDeg):
        numEdge = size * avgDeg
        hs = []
        rnd = random.random()
        s, t = 0, 0
        e = 0
        edges = np.zeros((numEdge, 2))
        for i in range(numEdge):
            s = random.random() + 1 #Might need to be rnd.nextint(size)
            t = random.random() + 1 #Might need to be rnd.nextint(size)
            if s == t:
                --i
            else:
                e = s
                e = (int(e) << 32) + t
                if e not in hs:
                    edges[i] = [s, t]
                    hs.append(e)
                else:
                    --i
        return edges

    def saveTemporalRandomGraph(self, fileName, t, size, avgDeg):
        try:
            bw = open(fileName, "w")
            bw.write(str(size) + "\t" + str(t))
            edges = np.matrix([], [])
            sb = ""

            for i in range(t):
                edges = self.generateRandGraph(size, avgDeg)
                for edge in edges:
                    sb = sb + str(edge[0]) + " " + str(edge[1]) + " "
                bw.write('\n')
                bw.write(sb)
            bw.close()
        except ValueError:
            print("error")

    def main(self, args):
        rgg = RandGraphGenerator()
        #rgg.saveTemporalRandomGraph("./dataSets/testData/dynGraph.txt", 4, 50, 5)
        rgg.saveTemporalRandomGraph("dynGraph.txt", 4, 50, 5)

main_var = RandGraphGenerator()
if __name__ == "__main__":
    main_var.main(sys.argv[1:])