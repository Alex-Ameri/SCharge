from model.Geometry.shapes.complete.Line_Surface_2D import *
from model.Geometry.interfaces.boundary_2D import *
from controller.enums import *
from model.Simulation.interfaces.VolumeObjectSimulator import *

vertexThresholdMeters = .0005

class NetChargeController:

    def __init__(self, netCharge : NetCharge, simMode : SimulationMode,
                 boundaryMode : BoundaryMode = BoundaryMode.NONE, boundarySimulator : VolumeObjectSimulator = None):
        self.netCharge : NetCharge = netCharge
        self.boundaryMode : BoundaryMode = boundaryMode
        self.simulationMode : SimulationMode = simMode

        #Variables for keeping track of boundary
        self.isOnBoundary = False
        self.boundaryMode : BoundaryMode = boundaryMode

        if(boundaryMode == BoundaryMode.NORMAL_VECTOR):
            self.boundarySimulator = boundarySimulator

        else:
            self.boundarySimulator = None

        #Keep track of leapfrog state
        self.hasLeapfrogStarted = False

    #PUBLIC METHODS

    def attachChargeToBoundary(self, boundary : Boundary2D):
        self.isOnBoundary = True
        self.netCharge.boundary = boundary

    def removeChargeFromBoundary(self):
        self.isOnBoundary = False
        self.netCharge.boundary = None
        self.netCharge.isFixedToBoundary = False

    def clearForces(self):
        self.netCharge.totalFX = 0
        self.netCharge.totalFY = 0
        self.netCharge.aX = 0
        self.netCharge.aY = 0

    def calculateNewPosition(self, deltaT):
        #Determine if on vertex
        #self.__applyVertexConstraints()

        #Move the particle
        if(self.netCharge.isFixedToBoundary == False and self.netCharge.isFixedInSpace == False):
            if (self.simulationMode == SimulationMode.NAIVE):
                self.__calculateNewPositionNaive(deltaT)

            elif(self.simulationMode == SimulationMode.LEAPFROG):
                self.__calculateNewPositionLeapfrog(deltaT)

    def applyForce(self, fX, fY):
        self.netCharge.totalFX += fX
        self.netCharge.totalFY += fY

    #PRIVATE METHODS
    def __getBoundaryDirection(self, vx_original, vy_original):
        #Tangent Vector
        if(self.boundaryMode == BoundaryMode.TANGENT_VECTOR):
            return self.netCharge.boundary.getSurfaceTangentVectorAtPointAlongLength(self.netCharge.x, self.netCharge.y)

        #Normal Vector
        elif(self.boundaryMode == BoundaryMode.NORMAL_VECTOR):
            return self.netCharge.boundary.getSurfaceNormalVectorAtPointAlongLength(self.netCharge.x, self.netCharge.y)

        else:
            return [vx_original, vy_original]

    def __calculateAcceleration(self):
        self.netCharge.aX = self.netCharge.totalFX / self.netCharge.mass
        self.netCharge.aY = self.netCharge.totalFY / self.netCharge.mass

    # This is the velocity calculation which is not using leapfrog
    def __calculateVelocityNaive(self, deltaT):
        if(self.isOnBoundary == False):
            self.netCharge.vX = self.netCharge.vX + (self.netCharge.aX * deltaT)
            self.netCharge.vY = self.netCharge.vY + (self.netCharge.aY * deltaT)
        else:
            # Take the dot product of the velocity with the vector defining the boundary
            #Find magnitdue first
            m_vX = self.netCharge.vX + (self.netCharge.aX * deltaT)
            m_vY = self.netCharge.vY + (self.netCharge.aY * deltaT)
            vMagnitude = math.sqrt(m_vX ** 2 + m_vY ** 2)

            #Get Boundary Direction
            boundaryUnitVector = self.__getBoundaryDirection(m_vX / vMagnitude, m_vY / vMagnitude)
            boundaryI = boundaryUnitVector[0]
            boundaryJ = boundaryUnitVector[1]

            #Find direction using the dot product
            direction = numpy.sign([m_vX * boundaryI, m_vY * boundaryJ])

            #Apply
            self.netCharge.vX = vMagnitude * direction[0] * boundaryI
            self.netCharge.vY = vMagnitude * direction[1] * boundaryJ

    def __calculateVelocityHalfstep(self, deltaT):
        if (self.isOnBoundary == False):
            self.netCharge.vX_nextHalf = self.netCharge.vX + 0.5 * deltaT * self.netCharge.aX
            self.netCharge.vY_nextHalf = self.netCharge.vY + 0.5 * deltaT * self.netCharge.aY

        else:
            # Take the dot product of the velocity with the vector defining the boundary
            # Find magnitdue first
            m_vX = self.netCharge.vX + 0.5 * deltaT * self.netCharge.aX
            m_vY = self.netCharge.vY + 0.5 * deltaT * self.netCharge.aY
            x = math.sqrt(m_vX ** 2 + m_vY ** 2)
            vMagnitude = math.sqrt(m_vX ** 2 + m_vY ** 2)

            # Get Boundary Direction
            boundaryUnitVector = self.__getBoundaryDirection(m_vX / vMagnitude, m_vY / vMagnitude)
            boundaryI = boundaryUnitVector[0]
            boundaryJ = boundaryUnitVector[1]

            # Find direction using the dot product
            direction = numpy.sign([m_vX * boundaryI, m_vY * boundaryJ])

            # Apply
            self.netCharge.vX_nextHalf = vMagnitude * direction[0] * boundaryI
            self.netCharge.vY_nextHalf = vMagnitude * direction[1] * boundaryJ

    def __calculateVelocityLeapfrog(self, deltaT):
        if (self.isOnBoundary == False):
            self.netCharge.vX = self.netCharge.vX_nextHalf + 0.5 * deltaT * self.netCharge.aX
            self.netCharge.vY = self.netCharge.vY_nextHalf + 0.5 * deltaT * self.netCharge.aY

        else:
            # Take the dot product of the velocity with the vector defining the boundary
            # Find magnitdue first
            m_vX = self.netCharge.vX_nextHalf + 0.5 * deltaT * self.netCharge.aX
            m_vY = self.netCharge.vY_nextHalf + 0.5 * deltaT * self.netCharge.aY
            vMagnitude = math.sqrt(m_vX ** 2 + m_vY ** 2)

            # Get Boundary Direction
            boundaryUnitVector = self.__getBoundaryDirection(m_vX / vMagnitude, m_vY / vMagnitude)
            boundaryI = boundaryUnitVector[0]
            boundaryJ = boundaryUnitVector[1]

            # Find direction using the dot product
            direction = numpy.sign([m_vX * boundaryI, m_vY * boundaryJ])

            # Apply
            self.netCharge.vX = vMagnitude * direction[0] * boundaryI
            self.netCharge.vY = vMagnitude * direction[1] * boundaryJ

    def __calculatePositionNaive(self, deltaT):
        #Calculate new position
        newX = self.netCharge.x + self.netCharge.vX * deltaT
        newY = self.netCharge.y + self.netCharge.vY * deltaT

        #Check to see if we are constrained by a boundary
        if(self.isOnBoundary == True):
            bound = self.netCharge.boundary

            if (newX < bound.getLeftmostVertex()):
                newX = bound.getLeftmostVertex()

            elif (newX > bound.getRightmostVertex()):
                newX = bound.getRightmostVertex()

            if(newY > bound.getTopmostVertex()):
                newY = bound.getTopmostVertex()

            if(newY < bound.getBottommostVertex()):
                newY = bound.getBottommostVertex()

        #Apply
        self.netCharge.x = newX
        self.netCharge.y = newY


    def __calculateNewPositionNaive(self, deltaT):
        self.__calculateAcceleration()
        self.__calculateVelocityNaive(deltaT)
        self.__calculatePositionNaive(deltaT)
        self.clearForces()


    def __updatePositionLeapfrog(self, newX, newY):
        #Check to see if we are constrained by a boundary
        if(self.isOnBoundary == True):
            bound = self.netCharge.boundary

            if (newX < bound.getLeftmostVertex()):
                newX = bound.getLeftmostVertex()

            elif (newX > bound.getRightmostVertex()):
                newX = bound.getRightmostVertex()

            if(newY > bound.getTopmostVertex()):
                newY = bound.getTopmostVertex()

            if(newY < bound.getBottommostVertex()):
                newY = bound.getBottommostVertex()

        #Apply
        self.netCharge.x = newX
        self.netCharge.y = newY

    def __calculateNewPositionLeapfrog(self, deltaT):
        self.__calculateAcceleration()

        if(self.hasLeapfrogStarted == False):
            #Velocity half-step
            self.__calculateVelocityHalfstep(deltaT)

            #Position full-step
            newX = self.netCharge.x + deltaT * self.netCharge.vX_nextHalf
            newY = self.netCharge.y + deltaT * self.netCharge.vY_nextHalf
            self.__updatePositionLeapfrog(newX, newY)
            self.hasLeapfrogStarted = True
        else:
            #velocity full-step
            self.__calculateVelocityLeapfrog(deltaT)

            # Velocity half-step
            self.__calculateVelocityHalfstep(deltaT)

            # Position full-step
            newX = self.netCharge.x + deltaT * self.netCharge.vX_nextHalf
            newY = self.netCharge.y + deltaT * self.netCharge.vY_nextHalf
            self.__updatePositionLeapfrog(newX, newY)

        self.clearForces()

    def __determineIfNearVertex(self):
        vertex1 = self.netCharge.boundary.getStartingPoint()
        vertex2 = self.netCharge.boundary.getEndingPoint()

        #check vertex 1
        if (abs(self.netCharge.x - vertex1[0]) < vertexThresholdMeters):
            if (abs(self.netCharge.y - vertex1[1]) < vertexThresholdMeters):
                return (True, vertex1, (vertex2[0] - vertex1[0]), (vertex2[1] - vertex1[1]))

        #check vertex 2
        elif (abs(self.netCharge.x - vertex2[0]) < vertexThresholdMeters):
            if (abs(self.netCharge.y - vertex2[1]) < vertexThresholdMeters):
                return (True, vertex2, (vertex1[0] - vertex2[0]), (vertex1[1] - vertex2[1]))
        else:
            return False