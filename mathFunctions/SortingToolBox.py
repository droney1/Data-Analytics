import numpy as np

class SortingToolBox:
    def __init__(self):
        pass
    def sortMatrixColumnInplace(self, m, cpIdx, desc):
        if len(m) == 0 or m[0] == 0:
            return
        r = len(m)
        c = len(m[0])
        mtr = np.matrix([c], [r])

        for i in range(0, r):
            for j in range(0, c):
                mtr[j][i] = m[i][j]
        mtr.sort() #TODO: Figure out how to sort this properly
        for i in range(0, r):
            for j in range(0, c):
                m[i][j] = mtr[j][i]
