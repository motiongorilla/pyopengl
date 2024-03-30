import math
import customutil
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

points = []
ptbuffer = []

window_width = 700
window_height = 700

window_resolution_x = (-window_width/2, window_width/2)
window_resolution_y = (-window_height/2, window_height/2)

window = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Custom Turtle in OpenGL")

turtle_position = (0, 0)

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(window_resolution_x[0], window_resolution_x[1],
               window_resolution_y[0], window_resolution_y[1])

def draw_element(to_draw=GL_POINTS, points=points, color=(1,1,1)):
    glBegin(to_draw)
    glColor3f(color[0], color[1], color[2])
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def line_to(x, y):
    global turtle_position
    glBegin(GL_LINE_STRIP)
    glVertex2f(turtle_position[0], turtle_position[1])
    glVertex2f(x,y)
    turtle_position = (x, y)
    glEnd()


init_ortho()

active = True
glLineWidth(1)
points.append((0,0))
while active:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_q:
                active = False
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            # Center based coord system
            px = customutil.map_value(window_width/2, 0,
                                      window_resolution_x[1], window_resolution_x[0],
                                      p[0])
            py = customutil.map_value(window_height/2, 0,
                                      window_resolution_y[0], window_resolution_y[1],
                                      p[1])
            points.append((px, py))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_element(points=points)

    pygame.display.flip()

pygame.quit()
