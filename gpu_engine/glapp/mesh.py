from OpenGL import *

from .transformations import *

from .uniform import *
from .GraphicsData import *

import pygame
import numpy as np

class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type, translation=pygame.Vector3(0,0,0)) -> None:
        self.vertices = vertices
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(program_id, "position")
        colors = GraphicsData("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")
        self.transformation_matrix = identity_matrix()
        self.transformation = Uniform("mat4", self.transformation_matrix)
        self.transformation.find_variable(program_id=program_id, variable_name="model_mat")

    def draw(self)->None:
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
