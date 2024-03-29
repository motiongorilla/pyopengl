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

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL with Python")

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,500,0,400)

def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def draw_line():
    glBegin(GL_LINE_STRIP)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

done = False
init_ortho()
glPointSize(5)
points=[]
isDown = False
while not done:
    p = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            isDown = True
        elif event.type == MOUSEBUTTONUP:
            isDown = False
        elif event.type == MOUSEMOTION and isDown:
            p = pygame.mouse.get_pos()
            x = customutil.map_value(0, 1000, 0, 500, p[0])
            y = customutil.map_value(800, 0, 0, 400, p[1])
            points.append((x,y))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    plot_point()
    draw_line()

    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
