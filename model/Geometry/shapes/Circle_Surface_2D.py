from model.Geometry.interfaces.boundary_2D import *

class circle_surface_2D(Boundary2D):

    def __init__(self, centerX, centerY, radius):
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        return True;

    def getStartingPoint(self):
        pass

    def getEndingPoint(self):
        pass

    def getSurfaceNormalVectorAtPointAlongLength(self, x, y):
        pass

    def getSurfaceTangentVectorAtPointAlongLength(self, x, y):
        pass

    def getLeftmostVertex(self):
        pass

    def getRightmostVertex(self):
        pass

    def getTopmostVertex(self):
        pass

    def getBottommostVertex(self):
        pass

    def getBoundingBox(self):
        pass



