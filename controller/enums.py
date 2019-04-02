import enum

class BoundaryMode(enum.Enum):
    #The particle is not on a boundary
    NONE = 0

    #The boundary the particle is on is defined by its normal vector
    NORMAL_VECTOR = 1

    #The boundary the particle is on is defined by its tangent vector
    TANGENT_VECTOR = 2

class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class SimulationMode(enum.Enum):
    NAIVE = 0
    LEAPFROG = 1
    CRANK_NICHOLS = 2


#PARTICLE STATE
#SHELL SURFACE SIMULATION
class ParticleBoundaryState(enum.Enum):

    #The particle is moving around in the center region of the surface
    FREE_MOVING = 0

    #The particle is locked to an edge vertex
    LOCKED_TO_EDGE = 1