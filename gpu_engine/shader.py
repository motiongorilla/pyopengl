from glapp.PyGLApp import *
from glapp.utils import *
from glapp.GraphicsData import GraphicsData
from glapp.square import *
from glapp.triangle import *
from glapp.axis import *
from glapp.cube import *

import numpy as np


vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;

void main(){
        gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
        color = vertex_color;
        }
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
out vec4 frag_color;

void main(){
        frag_color = vec4(color,1);
        }
'''


class Shader(PyGLApp):
    def __init__(self) -> None:
        super().__init__(400, 200, 1000, 800)
        self.square: Square = None
        self.triangle: Triangle = None
        self.axis: Axis = None
        self.cube = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(program_id=self.program_id, w=self.screen_width, h=self.screen_height)

        self.square = Square(self.program_id, pygame.Vector3(-0.5, 0.5, 0))
        self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0))
        self.cube = Cube(self.program_id, pygame.Vector3(0,0,0))
        self.axis = Axis(self.program_id, pygame.Vector3(0,0,0))
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.axis.draw()
        self.square.draw()
        self.cube.draw()
        self.triangle.draw()

Shader().mainloop()
