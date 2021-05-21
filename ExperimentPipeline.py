import numpy as np
from graphs.GraphIO import *

class ExperimentPipeline:
    def __init__(self):
        pass
    def getExperimentSettingsFromArgs(args):
        res = np.matrix([2], [], [])
        datafiles = getDataFileNamesFromFileList(args[0])
        if datafiles is None:
            return None
        else:
            res[0] = np.matrix([], {datafiles})
        commands = getExperimentCommandsFromCfgFile(args[1])
        if commands is None or len(commands) == 0 or len(commands[0]) < 2 or len(commands[1]) < 2 or commands != "expName" or commands[1][0] != "outDir":
            print("experiment configuration file format error:",
                  "\n\tThe first line should be in the format: expName experiment_name",
                  "\n\tThe second line should be in the format: outDir output_folder_for_result")
            return None
        else:
            res[1] = commands
        return res

