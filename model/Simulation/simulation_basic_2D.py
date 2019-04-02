from controller.net_charge_controller import *
from model.Geometry.shapes.Quad_Volume_2D import *

class Simulation:

    def __init__(self, simulationMode : SimulationMode, timeStep, boundaryMode : BoundaryMode):
        #cM : List[NetChargeController]
        #cF : List[NetChargeController]
        #line_boundaries : List[line_surface_2D]
        self.chargesMobile = list() #List[NetChargeController]
        self.chargesFixed = list() #List[NetChargeController]
        self.lineBoundaries = list() #List[line_surface_2D]
        self.simulationMode = simulationMode
        self.timeStep = timeStep
        self.boundaryMode = boundaryMode

    def addFreeCharge(self, netCharge, initialX, initialY, vX, vY, isFixedToBoundary=False, isFixedInSpace=False) -> NetChargeController:
        newID = len(self.chargesFixed) + len(self.chargesMobile)
        newCharge = NetCharge(newID, netCharge, initialX, initialY, vX, vY, isFixedToBoundary, isFixedInSpace)
        newChargeController = NetChargeController(newCharge, self.simulationMode, self.boundaryMode)

        if(isFixedToBoundary == False):
            self.chargesMobile.append(newChargeController)
        else:
            self.chargesFixed.append(newChargeController)

        return newChargeController

    def removeFreeCharge(self, charge : NetChargeController):
        try:
            self.chargesMobile.remove(charge)
        except:
            pass

        try:
            self.chargesFixed.remove(charge)
        except:
            pass

    def calculatePotential(self, x, y):
        potential = 0
        for q in range(0, len(self.chargesMobile)):
            Q = self.chargesMobile[q]
            potential += Q.netCharge.calculatePotentialAtPoint(x, y)

        return potential

    def calculateNextTimestep(self):
        #First calculate the forces between the mobile charges
        for q1 in range (0, len(self.chargesMobile), 1):
            for q2 in range(0, len(self.chargesMobile), 1):
                if(q1 != q2):
                    charge1 = self.chargesMobile[q1]
                    charge2 = self.chargesMobile[q2]
                    (fX, fY) = charge1.netCharge.calculateColoumbForce(charge2.netCharge.x, charge2.netCharge.y, charge2.netCharge.netCharge)
                    charge1.applyForce(fX, fY)
                    #charge2.applyForce(fX * -1, fY * -1)

        #Now move the particles
        for charge in self.chargesMobile:
            charge.calculateNewPosition(self.timeStep)
