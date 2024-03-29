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

def draw_line(draw_element=GL_LINE_STRIP):
    for point_list in ptcache:
        glBegin(draw_element)
        for p in point_list:
            glVertex2f(p[0], p[1])
        glEnd()

def save_canvas():
    with open("canvas.txt", "w") as f:
        f.write(f"{len(ptcache)}\n")
        for cache in ptcache:
            f.write(f"{len(cache)}\n")
            for coord in cache:
                f.write(f"{coord[0]} {coord[1]}\n")
    print("Canvas is saved!")

def load_canvas():
    with open("./canvas.txt", "r") as file:
        global points
        global ptcache
        cache_num = int(file.readline())

        ptcache = []
        for cache in range(cache_num):
            points = []
            ptcache.append(points)
            point_num = int(file.readline())
            for p in range(point_num):
                px, py = [float(value) for value in next(file).split()]
                points.append((px,py))


def plot_graph():
    for px in np.arange(0, 4, 0.005):
        py = math.exp(-px) * math.cos(2*math.pi * px)
        px = customutil.map_value(0,4,ortho_width[0],ortho_width[1],px)
        py = customutil.map_value(-1,1,ortho_height[0],ortho_height[1],py)
        points.append((px,py))
    ptcache.append(points)


done = False
isDown = False

points=[]
ptcache: list[list]= []

init_ortho()
# plot_graph()
glPointSize(5)

while not done:
    p = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_canvas()
            elif event.key == pygame.K_l:
                load_canvas()
            elif event.key == pygame.K_SPACE:
                ptcache.clear()
        elif event.type == MOUSEBUTTONDOWN:
            isDown = True
            points = []
            ptcache.append(points)
        elif event.type == MOUSEBUTTONUP:
            isDown = False
        elif event.type == MOUSEMOTION and isDown:
            p = pygame.mouse.get_pos()
            x = customutil.map_value(0, screen_width, ortho_width[0], ortho_width[1], p[0])
            y = customutil.map_value(screen_height, 0, ortho_height[0], ortho_height[1], p[1])
            points.append((x,y))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_line()

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
