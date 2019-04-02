import turtle
from controller.net_charge_controller import *
from typing import List
import threading
from queue import Queue

class FrameData():
    def __init__(self, fixedCharges : List[NetCharge], mobileCharges : List[NetCharge], boundaries : List[line_surface_2D]):
        self.fixed = fixedCharges
        self.mobile = mobileCharges
        self.boundaries = boundaries

class SceneView():
    def __init__(self, xPixelsPerMM : int, yPixelsPerMM : int, widthMM : int, heightMM : int,
                 boundariesQueue : Queue, particlesQueue : Queue[FrameData], dataLock : threading.Lock):
        self.screen = turtle.Screen()
        self.screen.setup(xPixelsPerMM * widthMM, yPixelsPerMM * heightMM)
        self.screen.tracer(0)

        ##initialize pen
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.width(3)
        self.pen.hideturtle()

        #Initialize queues so we are thread-safe
        self.boundaries = boundariesQueue
        self.particles = particlesQueue
        self.drawLock = dataLock

    def start(self):
        while True:
            self.updateScene()
            self.screen.update()

    def draw_square(self):
        for side in range(4):
            self.pen.forward(100)
            self.pen.left(90)

    def updateScene(self):
        with self.drawLock:
            if(self.boundaries.empty() == False):
                pass
            if(self.particles.empty() == False):
                mobileCharges = self.particles.get().mobile
                for charge in mobileCharges:
                    pass
                pass

    def drawChargesMobile(self, charges : List[NetChargeController]):
        pass

    def drawChargesFixed(self, charges : List[NetChargeController]):
        pass

    def drawLineBoundaries(self, boundaries : List[line_surface_2D]):
        pass





#view = SceneView(1, 1, 500, 500, Queue(), Queue(), threading.Lock())

def doStuff():
    while True:
        print('hi')

if __name__ == '__main__':
    if __name__ == '__main__':
        t = threading.Thread(target=doStuff)
        t.start()
        #view.start()