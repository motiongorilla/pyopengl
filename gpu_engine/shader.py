from glapp.PyGLApp import *
from glapp.utils import *
from glapp.GraphicsData import GraphicsData
from glapp.axis import *
from glapp.loadmesh import *
from glapp.transformations import *

import numpy as np


vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;
out vec3 normal;
out vec3 fragpos;
out vec3 light_pos;

void main(){
        light_pos = vec3(model_mat*view_mat*vec4(0,0,0,1));
        gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
        normal = vertex_normal;
        fragpos = vec3(model_mat * vec4(position, 1));
        color = vertex_color;
        }
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 light_pos;

out vec4 frag_color;

void main(){
        vec3 light_color = vec3(1,1,1);
        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_pos-fragpos);
        float diff = max(dot(normal, light_dir), 0);
        vec3 diffuse = diff * light_color;

        frag_color = vec4(color*diffuse,1);
        }
'''


class Shader(PyGLApp):
    def __init__(self) -> None:
        super().__init__(400, 200, 1000, 800)
        self.axis = None
        self.mesh = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(program_id=self.program_id, w=self.screen_width, h=self.screen_height, fov=80)
        self.axis = Axis(program_id=self.program_id, translation=pygame.Vector3(0,0,0))
        self.mesh = LoadMesh(program_id=self.program_id, draw_type=GL_TRIANGLES,
                             filename="./geometry/pighead.obj", color_normals=False,
                             scale=pygame.Vector3(1, 1, 1))

        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.axis.draw()
        self.mesh.draw()

Shader().mainloop()
