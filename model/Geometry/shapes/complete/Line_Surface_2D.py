import numpy as np
from model.Physics.net_charge import *
from model.Geometry.interfaces.boundary_2D import *


class line_surface_2D(Boundary2D):

    def __init__(self, mobileChargeColumbs, mobileChargePackets, x0, y0, x1, y1, fixedChargeColumbs=0,
                 fixedChargePacketOffset=0):
        self.netCharge = mobileChargeColumbs - fixedChargeColumbs
        self.mobileChargeColoumbs = mobileChargeColumbs
        self.fixedChargeColuoumbs = fixedChargeColumbs
        #fCharges : List[NetCharge]
        #mCharges : List[NetCharge]
        self.fixedChargePackets = (mobileChargePackets + fixedChargePacketOffset)
        self.mobileChargePackets = mobileChargePackets
        self.mobileChargeColoumbs = mobileChargeColumbs
        self.dX = x1 - x0
        self.dY = y1 - y0
        self.length = math.sqrt(self.dX ** 2 + self.dY ** 2)
        self.chargesMobile = list() # List[NetCharge]
        self.chargesFixed = list() #List[NetCharge]
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

        #Tangent Vector
        self.i = self.dX / self.length
        self.j = self.dY / self.length

        #normal vectors
        self.normalX = 0
        self.normalY = 0

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

    def initializeChargesFloating(self, startChargeID):
        # Initialize the point charges that can move around
        xIncrement = self.dX / self.mobileChargePackets
        yIncrement = self.dY / self.mobileChargePackets
        xStart = self.x0 + xIncrement / 2
        yStart = self.y0 + yIncrement / 2
        dQMobile = self.mobileChargeColoumbs/ self.mobileChargePackets
        chargeID = startChargeID

        for i in range(0, self.mobileChargePackets):
            newCharge = NetCharge(chargeID, dQMobile, xStart + i * xIncrement, yStart + i * yIncrement, 0, 0)
            self.chargesMobile.append(newCharge)
            chargeID = chargeID + 1


        # Now do the same for the fixed charges
        xIncrement = self.dX / self.fixedChargePackets
        yIncrement = self.dY / self.fixedChargePackets
        xStart = self.x0 + xIncrement / 2
        yStart = self.y0 + yIncrement / 2
        dQFixed = self.fixedChargeColuoumbs / self.fixedChargePackets

        for i in range(0, self.fixedChargePackets):
            newCharge = NetCharge(chargeID, dQFixed * -1, xStart + i * xIncrement, yStart + i * yIncrement, 0, 0)
            newCharge.isFixedToBoundary = True
            self.chargesFixed.append(newCharge)
            chargeID = chargeID + 1

        return (self.chargesMobile, self.chargesFixed)

    def getVectorRejection(self, xInputVector, yInputVector):
        return True

    def defineSurfaceNormal(self, x, y):
        #Get magnitude
        magnitude = math.sqrt(x ** 2 + y ** 2)
        self.normalX = x / magnitude
        self.normalY = y / magnitude

    def calculateVoltage(self, intermediatePoints, includeFixed = False):
        xStart = self.x0
        yStart = self.y0
        xIncrement = self.dX / intermediatePoints
        yIncrement = self.dY / intermediatePoints
        voltages = np.zeros(intermediatePoints)

        for i in range (0, intermediatePoints):
            x = xStart + i * xIncrement
            y = yStart + i * yIncrement

            for charge in self.chargesMobile:
                voltages[i] = voltages[i] + charge.calculatePotentialAtPoint(x, y)

        if (includeFixed == True):
            for i in range(0, intermediatePoints):
                x = xStart + i * xIncrement
                y = yStart + i * yIncrement

                for charge in self.chargesFixed:
                    voltages[i] = voltages[i] + charge.calculatePotentialAtPoint(x, y)

        print(voltages)
        return voltages

    #From Boundary2D
    def getStartingPoint(self):
        return (self.x0, self.y0)

    def getEndingPoint(self):
        return (self.x1, self.y1)

    def getSurfaceNormalVectorAtPointAlongLength(self, x, y):
        return (self.normalX, self.normalY)

    def getSurfaceTangentVectorAtPointAlongLength(self, x, y):
        return (self.i, self.j)

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





