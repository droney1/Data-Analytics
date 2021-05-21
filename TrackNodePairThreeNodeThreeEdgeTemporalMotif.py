import numpy as np
import sys
from graphs import *
#from graphs.GraphIO import *
#from graphs import *

class TrackNodePairThreeNodeThreeEdgeTemporalMotif:
    def __init__(self):
        pass
    def main(self, args):
        inFile, outFile = None, "outFile.txt"
        delta = 1
        for str in args:
            if str.startsWith("-i:"):
                inFile = str[3:]
            elif str.startsWith("-delta:"):
                delta = str[7:]
            elif str.startsWith("-o:"):
                outFile = str[3:]
        if inFile is None:
            print("[Error]: no infile: use '-i:input_file_path' to indicate inputfile")
        else:
            print("\tinput File = " + inFile)
            print("\toutput File = " + outFile)
            print("\ttime interval = " + str(delta))
        tg = getTemporalGraphWithTimeStampFromFile(inFile)
        trackedNodePairs = tg.trackNodePairThreeEdgeMotif(delta)
        matrix = np.matrix([np.size(trackedNodePairs)], [])
        idx = 0
        for nodePair in trackedNodePairs:
            matrix[idx] = nodePair
            ++idx
        outputMatrix(outFile, matrix)

main_var = TrackNodePairThreeNodeThreeEdgeTemporalMotif()
if __name__ == "__main__":
        main_var.main(sys.argv[1:])
