from view.scene_view_gl import *
from queue import Queue
from model.Simulation.simulation_basic_2D import *
from model.Simulation.simulation_linesonly import *
from controller.enums import *
from controller.net_charge_controller import *

class SimulationController():

    def __init__(self):
        #UI stuff
        particlesQueue = Queue()
        dataLock = threading.Lock()
        view = SceneView(1, 1, 800, 800, particlesQueue, dataLock)
        simulationThread = threading.Thread(target=self.start, args=(particlesQueue, dataLock,))
        print("doing")
        simulationThread.start()
        view.start()

    def start(self, particles : Queue, dataLock : threading.Lock):
        self.particlesQueue = particles
        self.dataLock = dataLock
        self.simulation = Simulation_Lines(SimulationMode.LEAPFROG, 0.0000000000005, BoundaryMode.NONE)

        #Free charges

        #a =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.26, 0.27, 0, 0)
        #b =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.26, 0.24, 0, 0)
        #c =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.25, 0.21, 0, 0)
        #d =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.26, 0.18, 0, 0)
        #e =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.24, 0.21, 0, 0)
        #f =self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.19, 0.17, 0, 0)
        #g = self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.25, 0.21, 0, 0)
        #h = self.simulation.addFreeCharge(1.6 * 10 ** -14, 0.2, 0.17, 0, 0)


        #for i in range (0, 4):
        #    for j in range(0, 4):
        #        self.simulation.addFreeCharge(-1.6 * 10 ** -12, 0.201 + i * .01, 0.201 + j * .01, 0, 0)

        #for i in range (0, 3):
        #    for j in range(0, 3):
        #        self.simulation.addFreeCharge(-1.6 * 10 ** -6, 0.231 + i * .001, 0.231 + j * .001, 0, 0)

        self.simulation.addFreeCharge(-1.6 * 10 ** -5, 0.05, 0.5, 0, 0, isFixedToBoundary=False, isFixedInSpace=True)


        #charges on surface
        #surface = line_surface_2D(10 ** -12, 5, .1, .5, .9, .5)
        #self.simulation.addLineGeometry(surface)
        #Quad = self.simulation.addQuadGeometry(.2, .2, .1, .1)

        #for charge in self.simulation.chargesMobile:
        #    charge.attachChargeToBoundary(Quad)

        print("starting")
        i = 0
        charges = list()

        beamCurrent = .001
        unitCharge = -1.6 * 10 ** -8
        period = abs(unitCharge / beamCurrent)
        print(period)

        while True:
            self.simulation.calculateNextTimestep()
            #surface.calculateVoltage(100)
            self.drawData()
            i += 1
            lastTime = 0
            total = 0
            totalCharge = 0
            #if(i % 1000 == 0):

            currentTime = self.simulation.timeStep * i
            elapsedTime = currentTime - lastTime
            #print(elapsedTime)
            if(elapsedTime > period):
                charge = self.simulation.addFreeCharge(-1.6 * 10 ** -10, 0.35, 0.5, 0, 0, isFixedToBoundary=False,
                                              isFixedInSpace=False)
                charges.append(charge)
                lastTime = currentTime

                for chargeF in charges:
                    if (chargeF.netCharge.x > 0.7):
                        self.simulation.removeFreeCharge(chargeF)
                        charges.remove(chargeF)



    def drawData(self):
        #Tell the view to draw something
        with self.dataLock:
            #pass data about particles
            dataPacket = FrameData(self.simulation.chargesFixed, self.simulation.chargesMobile, self.simulation.lineBoundaries)
            self.particlesQueue.put(dataPacket)





if __name__ == '__main__':
    SimulationController()