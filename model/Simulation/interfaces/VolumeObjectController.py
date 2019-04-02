import abc
from model.Geometry.interfaces.boundary_2D import *
from model.Simulation.interfaces.VolumeObjectSimulator import *

class VolumeObjectController(VolumeObjectSimulator, abc.ABC):

    @abc.abstractmethod
    def isPointOnBoundary(self, x, y):
        pass

    @abc.abstractmethod
    def getBoundaryNearPoint(self, x, y):
        pass

    @abc.abstractmethod
    def addBoundary(self, boundary : Boundary2D):
        pass

    @abc.abstractmethod
    def removeBoundary(self, boundary : Boundary2D):
        pass

    @abc.abstractmethod
    def doesLineIntersectBoundary(self, x0, y0, x1, y1):
        pass

    @abc.abstractmethod
    def getBoundariesIntersectedByLine(self, x0, y0, x1, y1):
        pass

    @abc.abstractmethod
    def getFirstBoundaryIntersectedByLine(self, x0, y0, x1, y1):
        pass

    @abc.abstractmethod
    def getLineBoundaryImpactArea(self, x0, y0, x1, y1):
        pass



