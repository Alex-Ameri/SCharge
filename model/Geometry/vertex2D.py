from model.Geometry.interfaces.boundary_2D import *


class Vertex2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.boundaries = list()

    def addBoundary(self, boundary : Boundary2D):
        self.boundaries.append(boundary)

    def removeBoundary(self, boundary : Boundary2D):
        self.boundaries.remove(boundary)