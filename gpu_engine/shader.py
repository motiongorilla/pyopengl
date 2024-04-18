from glapp.PyGLApp import *
from glapp.utils import *
from glapp.GraphicsData import GraphicsData
from glapp.axis import *
from glapp.loadmesh import *
from glapp.transformations import *
from glapp.animated_cube import *

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
        self.axis: Axis = None
        self.mesh = None
        self.anim = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(program_id=self.program_id, w=self.screen_width, h=self.screen_height)
        self.axis = Axis(program_id=self.program_id, translation=pygame.Vector3(0,0,0))
        self.mesh = LoadMesh(program_id=self.program_id, draw_type=GL_TRIANGLES,
                             filename="./geometry/pighead.obj", color_normals=True,
                             scale=pygame.Vector3(1, 1, 1),
                             rotation=Rotation(0, pygame.Vector3(1,0,0)))
        self.anim = AnimatedCube(program_id=self.program_id, location=pygame.Vector3(0,0,2),
                                 move_rotation=Rotation(25/60, pygame.Vector3(0,1,0)))

        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.axis.draw()
        self.anim.draw()
        self.mesh.draw()

Shader().mainloop()
