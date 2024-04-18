from OpenGL import *

from .transformations import *

from .uniform import *
from .GraphicsData import *

import pygame
import numpy as np

class AnimatedMesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type,
                 translation=pygame.Vector3(0,0,0),
                 rotation=Rotation(0, pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 move_rotation=Rotation(0, pygame.Vector3(0,1,0))) -> None:
        self.vertices = vertices
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(program_id, "position")
        colors = GraphicsData("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")
        self.transformation_matrix = identity_matrix()

        self.transformation_matrix = rotate_complex(self.transformation_matrix,
                                                    angle=rotation.angle, axis=rotation.axis)
        self.transformation_matrix = translate(self.transformation_matrix,
                                               translation.x, translation.y, translation.z)
        self.transformation_matrix = scale_non_uniform(self.transformation_matrix, scale.x, scale.y, scale.z)

        self.transformation = Uniform("mat4", self.transformation_matrix)
        self.transformation.find_variable(program_id=program_id, variable_name="model_mat")

        self.move_rotation = move_rotation
        self.program_id = program_id

    def draw(self)->None:
        self.transformation_matrix = rotate_complex(self.transformation_matrix,
                                                    angle=self.move_rotation.angle,
                                                    axis=self.move_rotation.axis)
        self.transformation = Uniform("mat4", self.transformation_matrix)
        self.transformation.find_variable(program_id=self.program_id, variable_name="model_mat")
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
