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
window_resolution_y = (0, window_height)

window = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("L-System")

turtle_position: tuple = (0, 0)
turtle_direction = np.array([0, 1, 0])

axiom = "X"
rules = {"F": "FF",
         "X": "F+[-F-XF-X][+FF][--XF[+X]][++F-X]"}
draw_step = 6
draw_angle = 25
stack = []
recursive_depth = 5
instructions = ""

def run_rule(run_count):
    global instructions
    instructions = axiom
    for i in range(run_count):
        old_system = instructions
        instructions = ""
        for c in range(0, len(old_system)):
            if old_system[c] in rules:
                instructions += rules[old_system[c]]
            else:
                instructions += old_system[c]

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

def move_to(pos):
    global turtle_position
    turtle_position = (pos[0], pos[1])

def reset_turtle():
    global turtle_position
    global turtle_direction
    turtle_position = (0, 0)
    turtle_direction = np.array([0, 1, 0])

def draw_turtle():
    global turtle_direction
    for c in range(len(instructions)):
        if instructions[c] == "F":
            forward(draw_step)
        elif instructions[c] == "+":
            rotate(draw_angle)
        elif  instructions[c] == "-":
            rotate(-draw_angle)
        elif instructions[c] == "[":
            stack.append((turtle_position, turtle_direction))
        elif instructions[c] == "]":
            current_vector = stack.pop()
            move_to(current_vector[0])
            turtle_direction = current_vector[1]

def forward(step):
    new_x = turtle_position[0] + turtle_direction[0] * step
    new_y = turtle_position[1] + turtle_direction[1] * step
    line_to(new_x, new_y)


def rotate(angle):
    global turtle_direction
    turtle_direction = customutil.z_rotation(turtle_direction, math.radians(angle))

init_ortho()

active = True
glLineWidth(1)
points.append((0,0))
run_rule(recursive_depth)
while active:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_q:
                active = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_element(points=points)
    reset_turtle()
    draw_turtle()

    pygame.display.flip()

pygame.quit()
