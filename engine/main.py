import Mesh
import Cube
import loadmesh
import camera

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')

# camera settings
camera_origin = [0, 0, 0]
camera_target = [0, 0, 0]
up_vector = [0, 1, 0]

mesh = loadmesh.LoadMesh("./geo/cube.obj", GL_LINE_LOOP)
cube = Cube.CubeMesh(GL_LINE_LOOP)
camera = camera.Camera()

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)

def camera_init():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(speed=0.05, w=screen.get_width(), h=screen.get_height())

def draw_world_axis():
    glLineWidth(3)
    glBegin(GL_LINES)
    # X Axis
    glColor3f(1, 0, 0)
    glVertex3d(-100, 0, 0)
    glVertex3d(100, 0, 0)
    #X arrow
    glVertex3d(2, 0, 0)
    glVertex3d(1.75, 0, 0.25)
    glVertex3d(2, 0, 0)
    glVertex3d(1.75, 0, -0.25)
    # Y Axis
    glColor3f(0, 1, 0)
    glVertex3d(0, -100, 0)
    glVertex3d(0, 100, 0)
    #Y arrow
    glVertex3d(0, 2, 0)
    glVertex3d(0.25, 1.75, 0)
    glVertex3d(0, 2, 0)
    glVertex3d(-0.25, 1.75, 0)
    # Z Axis
    glColor3f(0, 0, 1)
    glVertex3d(0, 0, -100)
    glVertex3d(0, 0, 100)
    # Z arrow
    glVertex3d(0.25, 0, 1.75)
    glVertex3d(0, 0, 2)
    glVertex3d(-0.25, 0, 1.75)
    glVertex3d(0, 0, 2)
    glEnd()

    # X pos sphere
    # sphere = gluNewQuadric()
    # glColor3f(1,0,0)
    # glPushMatrix()
    # glTranslated(0,0,1)
    # gluSphere(sphere, 0.05, 10, 10)
    # glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    draw_world_axis()
    for x in range(12):
        step = (2*math.pi)/12
        pos_x = math.sin(step*x)*5
        pos_z = math.cos(step*x)*5
        mesh.draw(l_color=(0.3,1,0.6), translate=pygame.Vector3(pos_x, 0, pos_z))


done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                done = True

    display()
    pygame.display.flip()
    # pygame.time.wait(50)

pygame.quit()

