import customutil
import numpy as np
import math

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

window_width = 1000
window_height = 1000

resolution_x = (-window_width/2, window_width/2)
resolution_y = (0, window_height)

pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("IFS")

active = True

draw_step = 20
draw_angle = 90
stack = []
iter_depth = 5
instructions = ""
rules = {"F": "F[+F]F"}
axiom = "F"

points = []
x = 0
y = 0

curr_position = (0, 0)
curr_direction = np.array([0, 1, 0])

def set_rules(num_iter):
    global instructions
    instructions = axiom

    for i in range(num_iter):
        old_system = instructions
        instructions = ""
        for char in old_system:
            if char in rules:
                instructions += rules[char]
            else:
                instructions += char

def line_to(x, y):
    global curr_position
    glBegin(GL_LINE_STRIP)
    glVertex2f(curr_position[0], curr_position[1])
    glVertex2f(x, y)
    curr_position = (x, y)
    glEnd()


def move_to(pos):
    global curr_position
    curr_position = (pos[0], pos[1])

def rotate(angle):
    global curr_direction
    curr_direction = customutil.z_rotation(curr_direction, math.radians(angle))

def forward(step):
    new_x = curr_position[0] + curr_direction[0]*step
    new_y = curr_position[1] + curr_direction[1]*step
    line_to(new_x, new_y)

def reset_turtle():
    global curr_direction
    global curr_position
    curr_position = (0, 0)
    curr_direction = np.array([0, 1, 0])

def draw_points(points):
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def draw_turtle(points):
    global x, y
    r = np.random.rand()
    if r < 0.1:
        x ,y = 0.00 * x + 0.00 * y, 0.00 * x + 0.16 * y + 0.0
    elif r < 0.86:
        x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        x, y = 0.2 *x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
    else:
        x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

    points.append((x, y))


def ortho_space():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(resolution_x[0], resolution_x[1],
               resolution_y[0], resolution_y[1])

ortho_space()
glPointSize(1)
glColor3f(0, 1, 0)

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                active = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScaled(80, 80, 1)

    reset_turtle()
    draw_turtle(points)
    draw_points(points)

    pygame.display.flip()
    pygame.time.wait(1)

pygame.quit()
