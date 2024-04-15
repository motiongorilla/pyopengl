from glapp.PyGLApp import *
from glapp.utils import *
from glapp.GraphicsData import GraphicsData
from glapp.square import *
from glapp.triangle import *

import numpy as np


vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform vec3 translation;
out vec3 color;

void main(){
        vec3 pos = position + translation;
        gl_Position = vec4(pos, 1);
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
        self.square = None
        self.triangle = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.square = Square(self.program_id, pygame.Vector3(-0.5, 0.5, 0))
        self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0))

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.square.draw()
        self.triangle.draw()

Shader().mainloop()
