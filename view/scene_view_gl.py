from controller.net_charge_controller import *
from typing import List
import threading
from queue import Queue
from OpenGL.GL import *
from OpenGL.GLUT import *


class FrameData():
    def __init__(self, fixedCharges : List[NetChargeController], mobileCharges : List[NetChargeController], boundaries : List[line_surface_2D]):
        self.fixed = fixedCharges
        self.mobile = mobileCharges
        self.boundaries = boundaries

class SceneView():
    def __init__(self, xPixelsPerMM : int, yPixelsPerMM : int, widthMM : int, heightMM : int,
                 dataQueue : Queue, dataLock : threading.Lock):


        #Initialize queues so we are thread-safe
        self.particles = dataQueue
        self.drawLock = dataLock

        #determine window size
        self.width = widthMM * xPixelsPerMM
        self.height = heightMM * yPixelsPerMM
        self.xRatio = 1000 / xPixelsPerMM
        self.yRatio = 1000 / yPixelsPerMM

    def start(self):
        # initialization
        glutInit()  # initialize glut
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)  # set window size
        glutInitWindowPosition(0, 0)  # set window position
        window = glutCreateWindow("Simulator")  # create window with title
        glutDisplayFunc(self.draw)  # set draw function callback
        glutIdleFunc(self.draw)  # draw all the time
        glutMainLoop()  # start everything

    def draw(self):
        #Setup
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
        glLoadIdentity()  # reset position
        self.refresh2d(self.width, self.height)

        # Draw Stuff
        self.updateScene()

        #Cleanup
        glutSwapBuffers()  # important for double buffering

    def refresh2d(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def updateScene(self):
        with self.drawLock:
            if(self.particles.empty() == False):
                data = self.particles.get()

                mobileCharges = data.mobile
                fixedCharges = data.fixed
                boundaries = data.boundaries

                #Boundaries
                for bound in boundaries:
                    self.drawLineBoundaries(boundaries)

                # Fixed
                for charge in fixedCharges:
                    self.drawChargesFixed(fixedCharges)
                    pass

                #Mobile
                for charge in mobileCharges:
                    self.drawChargesMobile(mobileCharges)



    def drawChargesMobile(self, charges : List[NetChargeController]):
        glColor3f(0.0, 0.0, 1.0)  # set color to blue
        width = 1
        height = 1
        for charge in charges:
            chargeModel = charge.netCharge
            x = chargeModel.x * self.xRatio
            y = chargeModel.y * self.yRatio
            glBegin(GL_QUADS)
            glVertex2f(x - width, y - height)
            glVertex2f(x + width, y - height)
            glVertex2f(x + width, y + height)
            glVertex2f(x - width, y + height)
            glEnd()

        glFlush()

    def drawChargesFixed(self, charges : List[NetChargeController]):
        glColor3f(1.0, 0.0, 0.0)  # set color to red
        width = 2
        height = 2
        for charge in charges:
            chargeModel = charge.netCharge
            x = chargeModel.x * self.xRatio
            y = chargeModel.y * self.yRatio
            glBegin(GL_QUADS)
            glVertex2f(x - width, y - height)
            glVertex2f(x + width, y - height)
            glVertex2f(x + width, y + height)
            glVertex2f(x - width, y + height)
            glEnd()

        glFlush()

    def drawLineBoundaries(self, boundaries : List[line_surface_2D]):
        glColor3f(0.0, 0.0, 0.0)  # set color to black
        for surface in boundaries:
            xStart = surface.x0 * self.xRatio
            yStart = surface.y0 * self.yRatio
            xEnd = surface.x1 * self.xRatio
            yEnd = surface.y1 * self.yRatio
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex2f(xStart, yStart)
            glVertex2f(xEnd, yEnd)
            glEnd()


