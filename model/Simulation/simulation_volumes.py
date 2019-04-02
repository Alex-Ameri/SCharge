from controller.net_charge_controller import *
from model.Geometry.shapes.Quad_Volume_2D import *
from model.Simulation.simulation_basic_2D import *
from model.Simulation.interfaces.VolumeObjectSimulator import *
from model.Simulation.volume_controller.GridVolumeController import *


class Simulation_Volumes(Simulation, VolumeObjectController):

    def __init__(self, simulationMode : SimulationMode, timeStep, boundaryMode : BoundaryMode, width, height, xCells, yCells):
        super().__init__(simulationMode, timeStep, boundaryMode)
        self.grid = GridVolumeController(width, height, xCells, yCells)

    def addBoundary(self, boundary: Boundary2D):
        pass

    def removeBoundary(self, boundary: Boundary2D):
        pass

    def isPointOnBoundary(self, x, y):
        pass

    def getBoundaryNearPoint(self, x, y):
        pass

    def doesLineIntersectBoundary(self, x0, y0, x1, y1):
        pass

    def getBoundariesIntersectedByLine(self, x0, y0, x1, y1):
        pass

    def getFirstBoundaryIntersectedByLine(self, x0, y0, x1, y1):
        pass

    def getLineBoundaryImpactArea(self, x0, y0, x1, y1):
        pass




