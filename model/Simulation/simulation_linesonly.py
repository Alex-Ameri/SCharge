from controller.net_charge_controller import *
from model.Geometry.shapes.Quad_Volume_2D import *
from model.Simulation.simulation_basic_2D import *

class Simulation_Lines(Simulation):

    def __init__(self, simulationMode : SimulationMode, timeStep, boundaryMode : BoundaryMode):
        super().__init__(simulationMode, timeStep, boundaryMode)
        self.lineBoundaries = list() #List[line_surface_2D]

    def addQuadGeometry(self, x, y, width, height):
        return Quad_2D(x, y, width, height)

    def addLineGeometry(self, lineSurface : line_surface_2D):
        startID = len(self.chargesFixed) + len(self.chargesMobile)
        newCharges = lineSurface.initializeChargesFloating(startID)
        newMobileCharges = newCharges[0]
        newFixedCharges = newCharges[1]

        for charge in newMobileCharges:
            newChargeController = NetChargeController(charge, self.simulationMode, self.boundaryMode)
            newChargeController.attachChargeToBoundary(lineSurface)
            self.chargesMobile.append(newChargeController)

        for charge in newFixedCharges:
            newChargeController = NetChargeController(charge, self.simulationMode, self.boundaryMode)
            newChargeController.attachChargeToBoundary(lineSurface)
            newChargeController.netCharge.isFixedToBoundary = True
            self.chargesFixed.append(newChargeController)

        self.lineBoundaries.append(lineSurface)
