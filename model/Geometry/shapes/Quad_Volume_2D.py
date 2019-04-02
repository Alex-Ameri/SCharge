import numpy as np
from model.Physics.net_charge import *
from model.Geometry.interfaces.boundary_2D import *


class Quad_2D(Boundary2D):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getStartingPoint(self):
        pass

    def getEndingPoint(self):
        pass

    def getLeftmostVertex(self):
        return self.x

    def getRightmostVertex(self):
        return self.x + self.width

    def getTopmostVertex(self):
        return self.y + self.height

    def getBottommostVertex(self):
        return self.y

    def getBoundingBox(self):
        return (self.x, self.y, self.width, self.height)

    def getSurfaceNormalVectorAtPointAlongLength(self, x, y):
        pass

    def getSurfaceTangentVectorAtPointAlongLength(self, x, y):
        pass

