import os
import sys
'''
from TemporalTimeStampRandomGraph import *
from GraphFactory import *
from TemporalTimeStampRandomGraph import *
'''
from ExperimentPipeline import *
from graphs import *
from randomgraph import *

class TemporalTripletEdgeGraphExperiment:
    def __init__(self):
        pass

    def main(self, args):
        if len(args) < 2:
            print("input the filename that store data_file_list and the filename that store operations")
            return

        tmp = getExperimentSettingsFromArgs(args)
        if tmp is None:
            return
        dataFiles = tmp[0][0]
        commands = tmp[1]
        expName = commands[0][1]
        outDir = commands[1][1]
        folder = os.path.join(outDir + "/" + expName)
        if os.path.exists(folder):
            os.mkdir(folder)
        tg = None
        for i in range(len(dataFiles)):
            tg = makeTemporalTripletGraphFromFile(dataFiles[i])

            for j in range(len(commands)):
                if len(commands[j]) == 0:
                    continue
                executeCommands(commands[j], tg.tripletEdges, expName, outDir, dataFiles[i][dataFiles[i].rindex('/') + 1 : dataFiles[i].rindex('.')])

    def executeCommands(self, cmd, edges, expName, outDir, dataFilePrefix):
        if len(cmd) > 2 and cmd[0] == "generateRandomGraph":
            tg = None
            if cmd[1] == "timestamp":
                tg = TemporalTimeStampRandomGraph(edges)
            else:
                pass

            if tg is None:
                print("no support for random graphs type: ", cmd[1])
                return
            num = int(cmd[2])

            tg.saveRandomGraphs(outDir+"/"+expName+"/"+dataFilePrefix, num)
        else:
            pass
main_var = TemporalTripletEdgeGraphExperiment()
if __name__ == "__main__":
        main_var.main(sys.argv[1:])