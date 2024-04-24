from components.PyGLApp import *
from components.utils import *
from components.GraphicsData import GraphicsData
from components.axis import *
from components.loadmesh import *
from components.transformations import *
from components.light import *

import numpy as np


vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;
in vec2 vertex_uv;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;
out vec3 normal;
out vec3 fragpos;
out vec3 view_pos;
out vec2 uv;

void main(){
        view_pos = vec3(inverse(model_mat)*
                        vec4(view_mat[3][0],view_mat[3][1],view_mat[3][2],1));

        gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
        normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
        fragpos = vec3(model_mat * vec4(position, 1));
        color = vertex_color;
        uv = vertex_uv;
        }
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 view_pos;
in vec2 uv;

uniform sampler2D tex;

out vec4 frag_color;

struct light{
        vec3 position;
        vec3 color;
        };

#define NUM_LIGHTS 2
uniform light light_data[NUM_LIGHTS];


vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 fragpos, vec3 view_dir, vec3 color){
        //ambient
        float ambient_strength = 0.1;
        vec3 ambient_light = ambient_strength * light_color;

        // diffuse
        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_pos-fragpos);
        float diff = max(dot(norm, light_dir), 0);
        vec3 diffuse = diff * light_color * 2.0f;

        // specular
        float specular_strength = 0.8;
        vec3 reflection_dir = normalize(-light_dir - norm);
        float spec = pow(max(dot(view_dir, reflection_dir), 0), 32);
        vec3 specular = specular_strength * spec * light_color;

        return vec4(color * (ambient_light + diffuse + specular),1);
        }

void main(){
        vec3 view_dir = normalize(view_pos-fragpos);
        frag_color = vec4(0,0,0,1);

        for(int i=0; i < NUM_LIGHTS; i++) {
            frag_color += Create_Light(light_data[i].position, light_data[i].color, normal, fragpos, view_dir, color);
        }

        frag_color = frag_color * texture(tex, uv);
}
'''


class Shader(PyGLApp):
    def __init__(self) -> None:
        super().__init__(400, 200, 1000, 800)
        self.axis = None
        self.mesh = None
        self.light = None
        self.light_b = None
        # glEnable(GL_CULL_FACE)

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(program_id=self.program_id, w=self.screen_width, h=self.screen_height, fov=40)
        self.axis = Axis(program_id=self.program_id, translation=pygame.Vector3(0,0,0))
        self.mesh = LoadMesh(program_id=self.program_id, draw_type=GL_TRIANGLES,
                             filename="./geometry/doghouse.obj",
                             texture="./geometry/doghouse_diffuse.png",
                             uv_scale=1)
        self.light = Light(self.program_id, pos=pygame.Vector3(2,1,2), light_id=0)
        self.light_b = Light(self.program_id, pos=pygame.Vector3(-2,1,-5), light_id=1)

        glLineWidth(6)
        glEnable(GL_DEPTH_TEST)
        # opacity
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_COLOR)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.light.update()
        self.light_b.update()
        self.axis.draw()
        self.mesh.draw()

Shader().mainloop()
