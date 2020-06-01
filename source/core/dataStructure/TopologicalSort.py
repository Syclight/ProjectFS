class node:
    def __init__(self):
        self.__inDegrees = list()

    def addIndegree(self, node_):
        self.__inDegrees.append(node_)

    def getSumOfIndegrees(self):
        return len(self.__inDegrees)

    def clearIndegree(self):
        self.__inDegrees.clear()


class AOV:
    def __init__(self):
        self.nodes = list()

    def addNode(self, node_):
        self.nodes.append(node_)

    def addAll(self, lis):
        for n in lis:
            self.addNode(n)

    def size(self):
        return len(self.nodes)

    def getNodeByIndegre(self, inDegree):
        ret = list()
        for n in self.nodes:
            if n.getSumOfIndegrees() == inDegree:
                ret.append(n)
        return ret


def topologicalSort(AOV_):
    while AOV_.size() > 0:
        pass

