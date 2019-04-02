from model.Simulation.interfaces.VolumeObjectSimulator import *
from model.Simulation.interfaces.VolumeObjectController import *
import numpy as np
import math

class TreeVolumeController(VolumeObjectController):

    def __init__(self):
        pass

    def isPointOnBoundary(self, x, y):
        pass

    def getBoundaryNearPoint(self, x, y):
        pass

    def addBoundary(self, boundary: Boundary2D):
        pass

    def removeBoundary(self, boundary: Boundary2D):
        pass

    def doesLineIntersectBoundary(self, x0, y0, x1, y1):
        pass

    def getBoundariesIntersectedByLine(self, x0, y0, x1, y1):
        pass

    def getFirstBoundaryIntersectedByLine(self, x0, y0, x1, y1):
        pass

    def getLineBoundaryImpactArea(self, x0, y0, x1, y1):
        pass


