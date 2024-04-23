from OpenGL import *

from .transformations import *

from .uniform import *
from .GraphicsData import *
from .texture import *

import pygame
import numpy as np

class Mesh:
    def __init__(self, program_id, texture, vertices, vertex_colors, normals, uv, draw_type,
                 translation=pygame.Vector3(0,0,0),
                 rotation=Rotation(0, pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 animated=False)->None:
        self.vertices = vertices
        self.draw_type = draw_type
        self.vertex_normal = normals
        self.vertex_color = vertex_colors
        self.uv = uv
        self.program_id = program_id
        self.animated = animated
        self.texfile = texture
        if self.texfile is not None:
            self.image = Texture(filename=self.texfile)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])
            self.texture.find_variable(self.program_id, "tex")

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)

        position = GraphicsData("vec3", self.vertices)
        position.create_variable(self.program_id, "position")

        colors = GraphicsData(data_type="vec3", data=self.vertex_color)
        colors.create_variable(self.program_id, "vertex_color")

        vertex_normal = GraphicsData("vec3", self.vertex_normal)
        vertex_normal.create_variable(self.program_id, "vertex_normal")

        vt_uv = GraphicsData("vec2", self.uv)
        vt_uv.create_variable(self.program_id, "vertex_uv")

        self.transformation_matrix = identity_matrix()
        self.transformation_matrix = rotate_complex(self.transformation_matrix,
                                                    angle=rotation.angle, axis=rotation.axis)
        self.transformation_matrix = translate(self.transformation_matrix,
                                               translation.x, translation.y, translation.z)
        self.transformation_matrix = scale_non_uniform(self.transformation_matrix, scale.x, scale.y, scale.z)

        self.transformation = Uniform("mat4", self.transformation_matrix)
        self.transformation.find_variable(program_id=program_id, variable_name="model_mat")

    def draw(self, animate_rotation=False, animate_position=False, animate_scale=False,
             anim_pos=pygame.Vector3(0,0,0),
             anim_rot=Rotation(0,pygame.Vector3(0,1,0)),
             anim_scale=pygame.Vector3(1,1,1)) -> None:
        if self.texfile is not None:
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
            self.transformation.find_variable(program_id=self.program_id,
                                              variable_name="model_mat")
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
