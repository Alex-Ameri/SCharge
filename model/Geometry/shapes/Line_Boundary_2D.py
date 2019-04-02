import numpy as np
from model.Physics.net_charge import *
from model.Geometry.interfaces.boundary_2D import *
from controller.enums import *

class LineBoundary_2D(Boundary2D):

    def __init__(self, x0, y0, x1, y1, NormalDirection : Direction):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.dX = x1 - x0
        self.dY = y1 - y0
        self.distance = math.sqrt(self.dX ** 2 + self.dY ** 2)

        #tangent vector
        self.I = self.dX / self.distance
        self.J = self.dY / self.distance

        #calculate surface normal
        if (NormalDirection == Direction.RIGHT) :
            #Slope of normal is the negative reciprocal of slope of tangent
            normalSlope = self.I / self.J * -1
            x = 1
            y = normalSlope
            magnitude = math.sqrt(x ** 2 + y ** 2)
            self.normalI = x / magnitude
            self.normalJ = y / magnitude
        else:
            normalSlope = self.I / self.J
            x = 1
            y = normalSlope
            magnitude = math.sqrt(x ** 2 + y ** 2)
            self.normalI = x / magnitude
            self.normalJ = y / magnitude

        #Calculate bounding box
        self.widthBB = abs(self.dX)
        self.heightBB = abs(self.dY)

        #Determine left and rightmost vertices
        if(self.x0 > self.x1):
            self.rightMostVertex = self.x0
            self.leftMostVertex = self.x1

        else:
            self.rightMostVertex = self.x1
            self.leftMostVertex = self.x0

        #Determin top and bottom-most vertices
        if (self.y0 > self.y1):
            self.topMostVertex = self.y0
            self.bottomMostVertex = self.y1

        else:
            self.topMostVertex = self.y1
            self.bottomMostVertex = self.y0


    #FROM BOUNDARY2D
    def getSurfaceTangentVectorAtPointAlongLength(self, x, y):
        return (self.I, self.J)

    def getSurfaceNormalVectorAtPointAlongLength(self, x, y):
        return (self.normalI, self.normalJ)

    def getLeftmostVertex(self):
        return self.leftMostVertex

    def getRightmostVertex(self):
        return self.rightMostVertex

    def getTopmostVertex(self):
        return self.topMostVertex

    def getBottommostVertex(self):
        return self.bottomMostVertex

    def getBoundingBox(self):
        return (self.leftMostVertex, self.bottomMostVertex, self.widthBB, self.heightBB)

    def getStartingPoint(self):
        return (self.x0, self.y0)

    def getEndingPoint(self):
        return (self.x1, self.y1)




