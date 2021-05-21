class ArrayLongComparator:
    def __init__(self, cpIdx, desc):
        self.cpIdx = cpIdx
        self.desc = desc

    def ArrayLongComparator(self, idxs, descending):
        self.cpIdx = idxs
        self.desc = descending

    def compare(self, a, b):
        if len(a) < len(self.cpIdx) or len(b) < len(self.cpIdx):
            return 0

        for i in self.cpIdx:
            if a[i] == b[i]:
                continue
            else:
                return 1 if ((b[i] - a[i]) if self.desc else a[i] - b[i]) > 0 else -1

            return 0
