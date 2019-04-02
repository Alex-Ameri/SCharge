from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = 0  # glut window number
width, height = 500, 400  # window size


def init():
    # initialization
    glutInit()  # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)  # set window size
    glutInitWindowPosition(0, 0)  # set window position
    window = glutCreateWindow("Simulator")  # create window with title
    glutDisplayFunc(draw)  # set draw function callback
    glutIdleFunc(draw)  # draw all the time
    glutMainLoop()  # start everything

def draw():  # ondraw is called all the time
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d(width, height)

    #Draw rectangle
    glColor3f(0.0, 0.0, 1.0)  # set color to blue
    draw_rect(10, 10, 200, 100)  # rect at (10, 10) with width 200, height 100

    glutSwapBuffers()  # important for double buffering

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

if __name__ == "__main__":
    init()