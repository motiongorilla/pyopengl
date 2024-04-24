from OpenGL import *

from .transformations import *

from .uniform import *
from .GraphicsData import *
from .texture import *

import pygame
import numpy as np

class Mesh:
    def __init__(self, vertices, texture=None, vertex_colors=None,
                 normals=None, uv=None, draw_type=GL_TRIANGLES,
                 translation=pygame.Vector3(0,0,0),
                 rotation=Rotation(0, pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 animated=False, material=None)->None:
        self.material = material
        self.vertices = vertices
        self.draw_type = draw_type
        self.vertex_normal = normals
        self.vertex_color = vertex_colors
        self.uv = uv
        self.animated = animated
        self.texture = None
        if texture is not None:
            self.image = Texture(filename=texture)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)

        position = GraphicsData("vec3", self.vertices)
        position.create_variable(self.material.program_id, "position")

        if self.vertex_color is not None:
            colors = GraphicsData(data_type="vec3", data=self.vertex_color)
            colors.create_variable(self.material.program_id, "vertex_color")

        if self.vertex_normal is not None:
            vertex_normal = GraphicsData("vec3", self.vertex_normal)
            vertex_normal.create_variable(self.material.program_id, "vertex_normal")

        if self.uv is not None:
            vt_uv = GraphicsData("vec2", self.uv)
            vt_uv.create_variable(self.material.program_id, "vertex_uv")

        self.transformation_matrix = identity_matrix()
        self.transformation_matrix = rotate_complex(self.transformation_matrix,
                                                    angle=rotation.angle, axis=rotation.axis)
        self.transformation_matrix = translate(self.transformation_matrix,
                                               translation.x, translation.y, translation.z)
        self.transformation_matrix = scale_non_uniform(self.transformation_matrix, scale.x, scale.y, scale.z)

        self.transformation = Uniform("mat4", self.transformation_matrix)
        self.transformation.find_variable(program_id=self.material.program_id, variable_name="model_mat")

    def draw(self, animate_rotation=False, animate_position=False, animate_scale=False,
             anim_pos=pygame.Vector3(0,0,0),
             anim_rot=Rotation(0,pygame.Vector3(0,1,0)),
             anim_scale=pygame.Vector3(1,1,1),
             camera=None, lights=None) -> None:

        self.material.use()
        camera.update(self.material.program_id)
        if lights is not None:
            for light in lights:
                light.update(self.material.program_id)

        if self.texture is not None:
            self.texture.find_variable(self.material.program_id, "tex")
            self.texture.load()

        if self.animated:
            if animate_rotation:
                self.transformation_matrix = rotate_complex(self.transformation_matrix,
                                                            angle=anim_rot.angle,
                                                            axis=anim_rot.axis)
            if animate_position:
                self.transformation_matrix = translate(self.transformation_matrix,
                                                       anim_pos.x,
                                                       anim_pos.y,
                                                       anim_pos.z)
            if animate_scale:
                self.transformation_matrix = scale_non_uniform(self.transformation_matrix,
                                                               anim_scale.x,
                                                               anim_scale.y,
                                                               anim_scale.z)
            self.transformation = Uniform("mat4", self.transformation_matrix)
            self.transformation.find_variable(program_id=self.material.program_id,
                                              variable_name="model_mat")
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
