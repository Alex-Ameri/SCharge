from model.Simulation.interfaces.VolumeObjectSimulator import *
from model.Simulation.interfaces.VolumeObjectController import *
import numpy as np
import math

class GridVolumeController(VolumeObjectController):

    def __init__(self, width, height, xCells, yCells):
        self.width = width
        self.height = height
        self.xCells = xCells
        self.yCells = yCells
        self.grid = np.zeros((yCells, xCells))
        self.gridPointers = np.zeros((yCells, xCells))
        self.boundaries = list()
        self.cellXSize = width / xCells
        self.cellYSize = height / yCells
        self.jumpSize = math.sqrt(self.cellXSize ** 2 + self.cellYSize ** 2)


    def isPointOnBoundary(self, x, y):
        xGrid = int(x / self.cellXSize)
        yGrid = int(y / self.cellYSize)

        if(self.grid[yGrid][xGrid] == 0):
            return False

        else:
            return True

    def getBoundaryNearPoint(self, x, y) -> Boundary2D:
        xGrid = int(x / self.cellXSize)
        yGrid = int(y / self.cellYSize)
        return self.gridPointers[yGrid][xGrid]

    def addBoundary(self, boundary: Boundary2D):
        self.boundaries.append(boundary)
        xStart = boundary.x0
        yStart = boundary.y0
        xEnd = boundary.x1
        yEnd = boundary.y1

        #Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        #dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        #mark the grid
        for i in range (0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY
            self.grid[yIndex][xIndex] = 1

            if(self.gridPointers[yIndex][xIndex] == 0):
                self.gridPointers[yIndex][xIndex] = list()

            self.gridPointers[yIndex][xIndex].append(boundary)


    def removeBoundary(self, boundary: Boundary2D):
        self.boundaries.remove(boundary)
        xStart = boundary.x0
        yStart = boundary.y0
        xEnd = boundary.x1
        yEnd = boundary.y1

        #Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        #dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        #mark the grid
        for i in range (0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY
            self.grid[yIndex] [xIndex] = 0

            try :
                self.gridPointers[yIndex][xIndex].remove(boundary)
                if(len(self.gridPointers[yIndex][xIndex]) == 0):
                    self.gridPointers[yIndex][xIndex] = 0

            except:
                pass

    def doesLineIntersectBoundary(self, x0, y0, x1, y1):
        xStart = x0
        yStart = y0
        xEnd = x1
        yEnd = y1

        # Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        # dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        # mark the grid
        for i in range(0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY

            if(self.grid[yIndex][xIndex] == 1):
                return True

        return False

    def getBoundariesIntersectedByLine(self, x0, y0, x1, y1):
        answers = list()
        xStart = x0
        yStart = y0
        xEnd = x1
        yEnd = y1

        # Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        # dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        # mark the grid
        for i in range(0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY

            if (self.grid[yIndex][xIndex] == 1):
                data = self.gridPointers[yIndex][xIndex]
                for boundary in data:
                    answers.append(boundary)

        return answers

    def getFirstBoundaryIntersectedByLine(self, x0, y0, x1, y1):
        answers = list()
        xStart = x0
        yStart = y0
        xEnd = x1
        yEnd = y1

        # Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        # dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        # mark the grid
        for i in range(0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY

            if (self.grid[yIndex][xIndex] == 1):
                data = self.gridPointers[yIndex][xIndex]
                for boundary in data:
                    answers.append(boundary)

                return answers

    def getLineBoundaryImpactArea(self, x0, y0, x1, y1):
        answers = list()
        xStart = x0
        yStart = y0
        xEnd = x1
        yEnd = y1

        # Grid equivalent points
        x0_grid = int(xStart / self.cellXSize)
        x1_grid = int(xEnd / self.cellXSize)
        y0_grid = int(yStart / self.cellYSize)
        y1_grid = int(yEnd / self.cellYSize)

        # dx, dy in grid domain
        dX = x1_grid - x0_grid
        dY = y1_grid - y0_grid
        magnitude = math.sqrt(dX ** 2 + dY ** 2)
        jumpDistance = self.jumpSize / 20
        intervals = int(magnitude / jumpDistance)
        sine = (dX / magnitude)
        cosine = (dY / magnitude)
        xDistance = cosine * jumpDistance
        yDistance = sine * jumpDistance

        # mark the grid
        for i in range(0, intervals, 1):
            progressX = xDistance * i
            progressY = yDistance * i
            xIndex = x0_grid + progressX
            yIndex = y0_grid + progressY

            if (self.grid[yIndex][xIndex] == 1):
                pass



