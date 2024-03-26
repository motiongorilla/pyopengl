import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL with Python")

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,0,480)

done = False
init_ortho()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2i(150, 100)
    glVertex2i(200, 120)
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2i(150, 100)
    glVertex2i(160, 230)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2i(150, 100)
    glEnd()
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2i(300, 160)
    glVertex2i(200, 120)
    glVertex2i(350, 340)
    glEnd()
    glPointSize(7)
    glBegin(GL_POINTS)
    glVertex2i(340, 230)
    glVertex2i(160, 230)
    glVertex2i(300, 260)
    glEnd()
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2i(280, 290)
    glVertex2i(310, 350)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
