import abc

class Boundary2D(abc.ABC):

    @abc.abstractmethod
    def getStartingPoint(self):
        pass

    @abc.abstractmethod
    def getEndingPoint(self):
        pass

    @abc.abstractmethod
    def getLeftmostVertex(self):
        pass

    @abc.abstractmethod
    def getRightmostVertex(self):
        pass

    @abc.abstractmethod
    def getTopmostVertex(self):
        pass

    @abc.abstractmethod
    def getBottommostVertex(self):
        pass

    @abc.abstractmethod
    def getBoundingBox(self):
        pass

    @abc.abstractmethod
    def getSurfaceNormalVectorAtPointAlongLength(self, x, y):
        pass

    @abc.abstractmethod
    def getSurfaceTangentVectorAtPointAlongLength(self, x, y):
        pass


