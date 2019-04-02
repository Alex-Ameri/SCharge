import abc

class BEM_2D_Shell(abc.ABC):

    @abc.abstractmethod
    def initializeSurfaceCharges(self, elementCount ):
        pass

    @abc.abstractmethod
    def getElementCount(self) -> int:
        pass

    @abc.abstractmethod
    def updateSurfaceCharges(self):
        pass

    @abc.abstractmethod
    #The voltage at the "surface" is defined at this distance from the actual shell
    def setSurfaceDatumNormalDistance(self, distance_meters):
        pass

    @abc.abstractmethod
    # The voltage at the "surface" is defined at this distance from the actual shell
    def getSurfaceDatumNormalDistance(self) -> float:
        pass