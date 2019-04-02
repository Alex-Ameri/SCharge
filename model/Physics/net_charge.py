import math
import numpy
from model.Geometry.interfaces.boundary_2D import *
from controller.enums import *


class NetCharge:

    def __init__(self, id, netCharge, initialX, initialY, vX, vY, isFixedToBoundary=False, isFixedInSpace=False):
        self.id = id
        self.netCharge = netCharge
        self.x = initialX
        self.y = initialY
        #TODO: FOR NOW IT IS ASSUMED THESE ARE PACKETS OF ELECTRONS
        self.mass = (abs(netCharge) / (1.6 * 10 ** -19)) * 9.1 * 10 ** -31
        self.vX = vX
        self.vY = vY
        self.isFixedToBoundary = isFixedToBoundary
        self.isFixedInSpace = isFixedInSpace

        #For Leapfrog
        self.vX_nextHalf = 0
        self.vY_nextHalf = 0

        #Accelerations
        self.aX = 0
        self.aY = 0

        #Used for net force calculation during simulations
        #These are a running tally of the forces on this particle
        self.totalFX = 0
        self.totalFY = 0

        #For boundaries
        self.boundary : Boundary2D = None
        self.BoundaryConstraintState : ParticleBoundaryState = ParticleBoundaryState.FREE_MOVING

        #If we are ever locked onto an edge, use this as our boundary vector
        self.vertexLockI = 0
        self.vertexLockJ = 0

    def calculatePotentialAtPoint(self, x, y):
        radius = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        radius = max(radius, 0.0000000000001)
        k = 8.98 * 10 ** 9
        return (k * self.netCharge / radius)

    def calculateColoumbForce(self, otherX, otherY, otherNetCharge):
        k = 8.99 * 10 ** 9
        q = otherNetCharge
        deltaX = otherX - self.x
        deltaY = otherY - self.y
        squaredDistance = max((deltaX ** 2 + deltaY ** 2), 0.0000001)
        distance = math.sqrt(squaredDistance)
        magnitude = abs(k * q * self.netCharge / squaredDistance)
        cosine = deltaX / distance
        sine = deltaY / distance

        #THIS WILL RETURN A FORCE VECTOR WHICH REPRESENTS THE FORCE ON THIS LOCAL PARTICLE!!!!
        #POTENTIAL BUG: IF TWO OPPOSITE PARTICLES ARE CLOSE THERE'S A HUGE FORCE BETWEEN THEM
        chargedSigns = numpy.sign([q, self.netCharge])
        a = chargedSigns[0]
        b = chargedSigns[1]
        attractionRepulsion = 0
        if(int(a) == int(b)):
            attractionRepulsion = -1

        else:
            attractionRepulsion = 1

        forceX = magnitude * cosine * attractionRepulsion
        forceY = magnitude * sine * attractionRepulsion
        return (forceX, forceY)