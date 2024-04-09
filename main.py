import math
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import customutil

pygame.init()

screen_width = 1000
screen_height = 800
ortho_width = (0,500)
ortho_height = (0,400)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL with Python")

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_width[0], ortho_width[1], ortho_height[0], ortho_height[1])

def draw_line(points, draw_element=GL_LINE_STRIP, color=[1,1,1]):
    glBegin(draw_element)
    glColor3f(color[0], color[1], color[2])
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()


done = False


init_ortho()
glPointSize(5)
glLineWidth(5)

while not done:
    p = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                customutil.save_canvas()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
